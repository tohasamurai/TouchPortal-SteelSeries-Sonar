# -*- coding: utf-8 -*-
"""SteelSeries Sonar plugin for Touch Portal.

Talks to the SteelSeries GG / Sonar local HTTP API and exposes audio
controls (mode, per-channel volume/mute, redirection device switching)
to Touch Portal. Pure standard library, no third-party dependencies.
"""
import json
import logging
import os
import socket
import ssl
import sys
import tempfile
import threading
import time
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import defs as D

LOG_PATH = os.path.join(tempfile.gettempdir(), "SteelSeriesSonarPlugin.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8"),
              logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("sonar")

TP_HOST = "127.0.0.1"
TP_PORT = 12136

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE


# =========================================================================
#  Sonar API client
# =========================================================================
class SonarClient:
    def __init__(self):
        self.base = None          # e.g. http://127.0.0.1:51606
        self.lock = threading.Lock()

    # ---- discovery ------------------------------------------------------
    def _core_props_path(self):
        pd = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
        return os.path.join(pd, "SteelSeries", "GG", "coreProps.json")

    def discover(self):
        """Locate the Sonar sub-app web server address. Returns base url or None."""
        try:
            with open(self._core_props_path(), "r", encoding="utf-8") as f:
                gg = json.load(f)["ggEncryptedAddress"]
        except Exception as e:
            log.warning("coreProps not readable: %s", e)
            self.base = None
            return None
        try:
            sub = self._http("GET", "https://%s/subApps" % gg)
            sonar = sub["subApps"]["sonar"]
            if not (sonar.get("isEnabled") and sonar.get("isReady") and sonar.get("isRunning")):
                log.warning("Sonar sub-app not ready: %s",
                            {k: sonar.get(k) for k in ("isEnabled", "isReady", "isRunning")})
                self.base = None
                return None
            self.base = sonar["metadata"]["webServerAddress"].rstrip("/")
            log.info("Sonar discovered at %s", self.base)
            return self.base
        except Exception as e:
            log.warning("subApps discovery failed: %s", e)
            self.base = None
            return None

    def ensure(self):
        if not self.base:
            self.discover()
        return self.base

    # ---- low level ------------------------------------------------------
    def _http(self, method, url, retries=0):
        ctx = _SSL_CTX if url.lower().startswith("https") else None
        req = urllib.request.Request(url, method=method)
        if method in ("PUT", "POST"):
            req.data = b""
        with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
            raw = resp.read()
        if not raw:
            return None
        try:
            return json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            return raw.decode("utf-8", "replace")

    def _api(self, method, path):
        """Call the Sonar web server, re-discovering once on failure."""
        base = self.ensure()
        if not base:
            raise RuntimeError("Sonar not available")
        url = "%s/%s" % (base, path)
        try:
            return self._http(method, url)
        except Exception as e:
            log.info("request failed (%s), re-discovering: %s", path, e)
            self.base = None
            base = self.discover()
            if not base:
                raise
            return self._http(method, "%s/%s" % (base, path))

    def get(self, path):
        return self._api("GET", path)

    def put(self, path):
        return self._api("PUT", path)

    # ---- high level -----------------------------------------------------
    def get_mode(self):
        m = self.get("mode")
        return m if isinstance(m, str) else str(m)

    def set_mode(self, mode_key):
        return self.put("mode/%s" % mode_key)

    def get_devices(self):
        """Return (render, capture, id_to_name). Lists of (name, id)."""
        data = self.get("audioDevices")
        render, capture, id2name = [], [], {}
        if isinstance(data, list):
            for d in data:
                name = d.get("friendlyName") or d.get("name") or ""
                did = d.get("id")
                flow = (d.get("dataFlow") or "").lower()
                if not did or not name:
                    continue
                id2name[did] = name
                if flow == "render":
                    render.append((name, did))
                elif flow == "capture" and not d.get("isVad", False):
                    # Master input must be a real physical microphone, not a
                    # Sonar virtual endpoint (which causes a feedback route).
                    capture.append((name, did))
        render.sort(key=lambda x: x[0].lower())
        capture.sort(key=lambda x: x[0].lower())
        return render, capture, id2name

    def get_stream_redirections(self):
        data = self.get("streamRedirections")
        out = {}
        arr = data.get("value") if isinstance(data, dict) else data
        if isinstance(arr, list):
            for item in arr:
                rid = item.get("streamRedirectionId")
                if rid:
                    out[rid] = item.get("deviceId")
        return out

    def get_classic_redirections(self):
        data = self.get("classicRedirections")
        out = {}
        arr = data.get("value") if isinstance(data, dict) else data
        if isinstance(arr, list):
            for item in arr:
                rid = item.get("classicRedirectionId") or item.get("id")
                if rid:
                    out[rid] = item.get("deviceId")
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict) and "deviceId" in v:
                    out[k] = v["deviceId"]
        return out

    def set_stream_redirect(self, redirect_key, device_id):
        return self.put("streamRedirections/%s/deviceId/%s"
                        % (redirect_key, urllib.parse.quote(device_id, safe="")))

    def set_classic_redirect(self, role_key, device_id):
        return self.put("classicRedirections/%s/deviceId/%s"
                        % (role_key, urllib.parse.quote(device_id, safe="")))

    def set_master_microphone(self, device_id):
        """Set the Master-panel microphone input for both Sonar modes.

        The GG UI displays the active Streamer-mode value in Master, while
        retaining a separate Classic value. Writing both keeps the dropdown
        in sync when the user changes Sonar mode.
        """
        self.set_stream_redirect("mic", device_id)
        try:
            self.set_classic_redirect("mic", device_id)
        except Exception as exc:
            # Streamer mode is the active target. Older GG builds can reject
            # a Classic write while Streamer is active, so don't undo it.
            log.info("Classic Master mic sync skipped: %s", exc)

    def set_stream_monitoring(self, enabled):
        return self.put("streamRedirections/isStreamMonitoringEnabled/%s"
                        % ("true" if enabled else "false"))

    def get_volume_settings(self):
        return self.get("volumeSettings/streamer")

    @staticmethod
    def _fmt_vol(percent):
        percent = max(0, min(100, int(round(percent))))
        return "%g" % (percent / 100.0)

    def set_volume(self, mix_key, channel_key, percent):
        v = self._fmt_vol(percent)
        if mix_key == D.MIX_CLASSIC:
            path = "volumeSettings/classic/%s/Volume/%s" % (channel_key, v)
        else:
            path = "volumeSettings/streamer/%s/%s/volume/%s" % (mix_key, channel_key, v)
        return self.put(path)

    def set_mute(self, mix_key, channel_key, muted):
        val = "true" if muted else "false"
        if mix_key == D.MIX_CLASSIC:
            path = "volumeSettings/classic/%s/Mute/%s" % (channel_key, val)
        else:
            path = "volumeSettings/streamer/%s/%s/isMuted/%s" % (mix_key, channel_key, val)
        return self.put(path)


# =========================================================================
#  Touch Portal client
# =========================================================================
class TPClient:
    def __init__(self, plugin):
        self.plugin = plugin
        self.sock = None
        self.rfile = None
        self.wlock = threading.Lock()
        self.connected = False

    def connect(self):
        self.sock = socket.create_connection((TP_HOST, TP_PORT), timeout=10)
        self.sock.settimeout(None)
        self.rfile = self.sock.makefile("rb")
        self.connected = True
        self.send({"type": "pair", "id": D.PLUGIN_ID})
        log.info("Paired with Touch Portal")

    def send(self, obj):
        """Best-effort send. Returns False (and marks disconnected) on failure."""
        if not self.connected or self.sock is None:
            return False
        data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        try:
            with self.wlock:
                self.sock.sendall(data)
            return True
        except OSError as e:
            if self.connected:
                log.info("send failed, connection lost: %s", e)
            self.connected = False
            return False

    # convenience senders
    def state_update(self, sid, value):
        self.send({"type": "stateUpdate", "id": sid, "value": str(value)})

    def choice_update(self, data_id, values, instance_id=None):
        msg = {"type": "choiceUpdate", "id": data_id, "value": values}
        if instance_id:
            msg["instanceId"] = instance_id
        self.send(msg)

    def connector_update_long(self, connector_id, data_pairs, value):
        cid = "pc_%s_%s" % (D.PLUGIN_ID, connector_id)
        for k, v in data_pairs:
            cid += "|%s=%s" % (k, v)
        self.send({"type": "connectorUpdate", "connectorId": cid,
                   "value": max(0, min(100, int(value)))})

    def loop(self):
        """Blocks reading messages until the socket closes or errors."""
        buf = self.rfile
        try:
            while self.connected:
                line = buf.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line.decode("utf-8", "replace"))
                except Exception as e:
                    log.warning("bad message: %s", e)
                    continue
                try:
                    self.plugin.on_message(msg)
                except Exception:
                    log.exception("error handling message %s", msg.get("type"))
        except OSError as e:
            log.info("read loop ended: %s", e)
        finally:
            self.connected = False

    def close(self):
        self.connected = False
        try:
            self.sock.close()
        except Exception:
            pass


# =========================================================================
#  Plugin glue
# =========================================================================
class Plugin:
    def __init__(self):
        self.sonar = SonarClient()
        self.tp = TPClient(self)
        self.render = []          # [(name, id)]
        self.capture = []
        self.id2name = {}
        self.name2id = {}         # unique dropdown label -> device id
        self.render_choices = []
        self.capture_choices = []
        self._device_fingerprint = None
        self._last_device_refresh = 0.0
        self.muted_label = "muted"
        self.unmuted_label = "unmuted"
        self.stop = threading.Event()          # set only on quit (closePlugin)

    # ---- lifecycle ------------------------------------------------------
    def serve(self):
        """Run forever: (re)connect to Touch Portal and survive drops.

        Touch Portal launches the plugin process only once (at TP startup or
        on import) and does not resurrect it, so the process must keep itself
        alive across socket drops / Sonar & TP restarts. It exits only when
        TP explicitly asks it to (closePlugin) or the machine is shutting the
        process down.
        """
        poller = threading.Thread(target=self.poll_loop, daemon=True)
        poller.start()
        backoff = 2
        while not self.stop.is_set():
            try:
                self.tp.connect()
                backoff = 2
                self.tp.loop()               # blocks until disconnect
            except (ConnectionRefusedError, OSError) as e:
                log.info("TP not reachable: %s", e)
            except Exception:
                log.exception("unexpected error in TP session")
            finally:
                self.tp.connected = False
            if self.stop.is_set():
                break
            log.info("Disconnected from TP; reconnecting in %ss", backoff)
            self.stop.wait(backoff)
            backoff = min(backoff * 2, 15)     # capped exponential backoff
        log.info("Plugin shutting down (closePlugin)")

    # ---- device lists ---------------------------------------------------
    def refresh_devices(self):
        try:
            self.render, self.capture, self.id2name = self.sonar.get_devices()
        except Exception as e:
            log.warning("device refresh failed: %s", e)
            return
        self.name2id = {}
        self.render_choices = self._make_device_choices(self.render)
        self.capture_choices = self._make_device_choices(self.capture)
        render_names = self.render_choices or ["<no output devices>"]
        capture_names = self.capture_choices or ["<no input devices>"]
        self.tp.choice_update(D.D_MONITORING_DEVICE, render_names)
        self.tp.choice_update(D.D_STREAMING_DEVICE, render_names)
        self.tp.choice_update(D.D_MIC_DEVICE, capture_names)
        self.tp.choice_update(D.D_DEVICE, render_names)
        self.tp.choice_update(D.D_DEVICE_CLASSIC, render_names)
        self._device_fingerprint = tuple(sorted(did for _, did in self.render + self.capture))
        self._last_device_refresh = time.monotonic()
        log.info("Loaded %d output / %d input devices", len(self.render), len(self.capture))

    def _make_device_choices(self, devices):
        """Create stable, unique dropdown labels even for duplicate friendly names."""
        totals = {}
        for name, _ in devices:
            totals[name] = totals.get(name, 0) + 1
        seen = {}
        labels = []
        for name, did in devices:
            seen[name] = seen.get(name, 0) + 1
            label = "%s [%d]" % (name, seen[name]) if totals[name] > 1 else name
            labels.append(label)
            self.name2id[label] = did
        return labels

    def device_id(self, name):
        return self.name2id.get(name)

    # ---- incoming messages ---------------------------------------------
    def on_message(self, msg):
        t = msg.get("type")
        if t == "info":
            self.apply_settings(msg.get("settings", []))
            self.tp.state_update(D.S_CONNECTED, "1")
            # (re)populate device dropdowns and push fresh state on every
            # (re)connect, since TP may have restarted and lost runtime data.
            self.refresh_devices()
            self.poll_once()
        elif t == "settings":
            self.apply_settings(msg.get("values", []))
        elif t == "closePlugin":
            log.info("Received closePlugin from TP")
            self.stop.set()
            self.tp.close()
        elif t == "action":
            self.on_action(msg.get("actionId"), self.data_map(msg.get("data", [])))
        elif t == "connectorChange":
            self.on_connector(msg)
        elif t == "listChange":
            self.on_list_change(msg)

    @staticmethod
    def data_map(data):
        return {d.get("id"): d.get("value") for d in data}

    def apply_settings(self, values):
        for item in values:
            if D.SET_MUTED_LABEL in item:
                self.muted_label = item[D.SET_MUTED_LABEL] or "muted"
            if D.SET_UNMUTED_LABEL in item:
                self.unmuted_label = item[D.SET_UNMUTED_LABEL] or "unmuted"

    # ---- dependent dropdowns -------------------------------------------
    def on_list_change(self, msg):
        list_id = msg.get("listId")
        instance = msg.get("instanceId")
        value = msg.get("value")
        if not instance:
            return
        render_names = self.render_choices or ["<no output devices>"]
        capture_names = self.capture_choices or ["<no input devices>"]
        if list_id == D.D_STREAM_REDIRECT:
            flow = D.STREAM_REDIRECT_FLOW_BY_LABEL.get(value, "render")
            self.tp.choice_update(D.D_DEVICE,
                                  capture_names if flow == "capture" else render_names, instance)
        elif list_id == D.D_CLASSIC_REDIRECT:
            flow = D.CLASSIC_REDIRECT_FLOW_BY_LABEL.get(value, "render")
            self.tp.choice_update(D.D_DEVICE_CLASSIC,
                                  capture_names if flow == "capture" else render_names, instance)

    # ---- actions --------------------------------------------------------
    def on_action(self, action_id, dm):
        log.info("TP action received: %s data=%s", action_id, dm)
        try:
            self._dispatch(action_id, dm)
        except Exception:
            log.exception("action %s failed", action_id)
        # push fresh state shortly after
        threading.Timer(0.25, self.poll_once).start()

    def _dispatch(self, action_id, dm):
        if action_id == D.ACT_SET_MODE:
            mode = "classic" if dm.get(D.D_MODE, "").lower().startswith("c") else "stream"
            self.sonar.set_mode(mode)

        elif action_id == D.ACT_TOGGLE_MODE:
            cur = self.sonar.get_mode()
            self.sonar.set_mode("classic" if "stream" in cur.lower() else "stream")

        elif action_id == D.ACT_SET_MONITORING_SRC:
            self._redirect_by_name("monitoring", dm.get(D.D_MONITORING_DEVICE))
        elif action_id == D.ACT_SET_STREAMING_SRC:
            self._redirect_by_name("streaming", dm.get(D.D_STREAMING_DEVICE))
        elif action_id == D.ACT_SET_MIC_SRC:
            self._set_master_microphone_by_name(dm.get(D.D_MIC_DEVICE))
        elif action_id == D.ACT_NEXT_MIC_SRC:
            self._select_next_microphone()
        elif action_id == D.ACT_REFRESH_DEVICES:
            self.refresh_devices()

        elif action_id == D.ACT_STREAM_REDIRECT:
            key = D.STREAM_REDIRECT_KEY_BY_LABEL.get(dm.get(D.D_STREAM_REDIRECT))
            self._redirect_by_name(key, dm.get(D.D_DEVICE))

        elif action_id == D.ACT_CLASSIC_REDIRECT:
            key = D.CLASSIC_REDIRECT_KEY_BY_LABEL.get(dm.get(D.D_CLASSIC_REDIRECT))
            did = self.device_id(dm.get(D.D_DEVICE_CLASSIC))
            if key and did:
                self.sonar.set_classic_redirect(key, did)

        elif action_id == D.ACT_SET_VOLUME:
            mix = D.MIX_KEY_BY_LABEL.get(dm.get(D.D_MIX))
            ch = D.CHANNEL_KEY_BY_LABEL.get(dm.get(D.D_CHANNEL))
            pct = self._to_int(dm.get(D.D_VOLUME), 50)
            if mix and ch:
                self.sonar.set_volume(mix, ch, pct)

        elif action_id == D.ACT_ADJ_VOLUME:
            mix = D.MIX_KEY_BY_LABEL.get(dm.get(D.D_MIX))
            ch = D.CHANNEL_KEY_BY_LABEL.get(dm.get(D.D_CHANNEL))
            delta = self._to_int(dm.get(D.D_VOL_DELTA), 0)
            if mix and ch:
                cur = self._current_volume(mix, ch)
                self.sonar.set_volume(mix, ch, max(0, min(100, cur + delta)))

        elif action_id == D.ACT_MUTE:
            mix = D.MIX_KEY_BY_LABEL.get(dm.get(D.D_MIX))
            ch = D.CHANNEL_KEY_BY_LABEL.get(dm.get(D.D_CHANNEL))
            act = (dm.get(D.D_MUTE_ACTION) or "Toggle").lower()
            if mix and ch:
                if act == "mute":
                    muted = True
                elif act == "unmute":
                    muted = False
                else:
                    muted = not self._current_muted(mix, ch)
                self.sonar.set_mute(mix, ch, muted)

        elif action_id == D.ACT_MUTE_MIC:
            self._mute_microphone((dm.get(D.D_ONOFF) or "Toggle").lower())

        elif action_id == D.ACT_STREAM_MONITORING:
            v = (dm.get(D.D_ONOFF) or "Toggle").lower()
            if v == "on":
                self.sonar.set_stream_monitoring(True)
            elif v == "off":
                self.sonar.set_stream_monitoring(False)
            else:
                self.sonar.set_stream_monitoring(not self._stream_monitoring_on)

    def _mic_targets(self):
        """(mix_key, channel_key) pairs for the microphone in the active mode."""
        try:
            stream = "stream" in self.sonar.get_mode().lower()
        except Exception:
            stream = True
        if stream:
            return [(D.MIX_STREAMING, "chatCapture"), (D.MIX_MONITORING, "chatCapture")]
        return [(D.MIX_CLASSIC, "chatCapture")]

    def _select_next_microphone(self):
        """Cycle through physical capture devices using exact Windows IDs."""
        self.refresh_devices()
        if not self.capture:
            raise RuntimeError("No microphone input devices found")
        current = self._master_microphone_id()
        ids = [did for _, did in self.capture]
        try:
            index = (ids.index(current) + 1) % len(ids)
        except ValueError:
            index = 0
        self.sonar.set_master_microphone(ids[index])
        log.info("Microphone switched to %s", self.capture[index][0])

    def _master_microphone_id(self):
        mode = self.sonar.get_mode().lower()
        if "stream" in mode:
            return self.sonar.get_stream_redirections().get("mic")
        return self.sonar.get_classic_redirections().get("mic")

    def _set_master_microphone_by_name(self, device_name):
        did = self.device_id(device_name)
        if not did:
            raise RuntimeError("Selected Master microphone is unavailable: %r" % device_name)
        self.sonar.set_master_microphone(did)
        log.info("Master microphone set to %s (%s)", device_name, did)

    def _mute_microphone(self, action):
        targets = self._mic_targets()
        if action == "on":
            muted = True
        elif action == "off":
            muted = False
        else:
            muted = not self._current_muted(*targets[0])
        for mix, ch in targets:
            self.sonar.set_mute(mix, ch, muted)

    def _redirect_by_name(self, redirect_key, device_name):
        did = self.device_id(device_name)
        if redirect_key and did:
            if redirect_key == "mic":
                self.sonar.set_master_microphone(did)
            else:
                self.sonar.set_stream_redirect(redirect_key, did)
        else:
            log.warning("redirect skipped: key=%s name=%r id=%s", redirect_key, device_name, did)

    @staticmethod
    def _to_int(v, default):
        try:
            return int(round(float(v)))
        except Exception:
            return default

    # ---- connector (slider) --------------------------------------------
    def on_connector(self, msg):
        if msg.get("connectorId") != D.CON_VOLUME:
            return
        dm = self.data_map(msg.get("data", []))
        mix = D.MIX_KEY_BY_LABEL.get(dm.get(D.D_MIX))
        ch = D.CHANNEL_KEY_BY_LABEL.get(dm.get(D.D_CHANNEL))
        value = self._to_int(msg.get("value"), 0)
        if mix and ch:
            try:
                self.sonar.set_volume(mix, ch, value)
            except Exception:
                log.exception("connector volume failed")

    # ---- state polling --------------------------------------------------
    _stream_monitoring_on = True

    def poll_loop(self):
        # poll only while connected to TP; runs for the whole process lifetime
        while not self.stop.wait(1.5):
            if self.tp.connected:
                self.poll_once()

    def poll_once(self):
        if not self.tp.connected:
            return
        try:
            # Pick up microphones/headsets connected after plugin startup.
            if time.monotonic() - self._last_device_refresh >= 10:
                self.refresh_devices()
            self._poll()
        except Exception as e:
            log.info("poll failed: %s", e)

    def _poll(self):
        base = self.sonar.ensure()
        if not base:
            self.tp.state_update(D.S_MODE, "Sonar offline")
            return
        mode = self.sonar.get_mode()
        self.tp.state_update(D.S_MODE, mode)

        redir = self.sonar.get_stream_redirections()
        self.tp.state_update(D.S_REDIRECT_STREAMING,
                             self.id2name.get(redir.get("streaming"), ""))
        self.tp.state_update(D.S_REDIRECT_MONITORING,
                             self.id2name.get(redir.get("monitoring"), ""))
        master_mic = (redir.get("mic") if "stream" in mode.lower()
                      else self.sonar.get_classic_redirections().get("mic"))
        self.tp.state_update(D.S_REDIRECT_MIC, self.id2name.get(master_mic, ""))

        vs = self.sonar.get_volume_settings()
        self._update_volume_states(vs)

        mic_mix = D.MIX_STREAMING if "stream" in mode.lower() else D.MIX_CLASSIC
        self.tp.state_update(
            D.S_MIC_MUTED,
            self.muted_label if self._current_muted(mic_mix, "chatCapture") else self.unmuted_label)

    def _update_volume_states(self, vs):
        if not isinstance(vs, dict):
            return
        self._vol_cache = {}
        self._mute_cache = {}
        masters = vs.get("masters", {})
        devices = vs.get("devices", {})

        def emit(mix_key, ch_key, node):
            if not isinstance(node, dict):
                return
            vol = node.get("volume")
            muted = node.get("muted")
            if vol is not None:
                pct = int(round(vol * 100))
                self._vol_cache[(mix_key, ch_key)] = pct
                self.tp.state_update(D.s_volume(mix_key, ch_key), pct)
            if muted is not None:
                self._mute_cache[(mix_key, ch_key)] = bool(muted)
                self.tp.state_update(D.s_mute(mix_key, ch_key),
                                     self.muted_label if muted else self.unmuted_label)

        # Master
        m_stream = masters.get("stream", {})
        emit(D.MIX_STREAMING, "Master", m_stream.get("streaming"))
        emit(D.MIX_MONITORING, "Master", m_stream.get("monitoring"))
        emit(D.MIX_CLASSIC, "Master", masters.get("classic"))
        # per channel
        for ch_key, node in devices.items():
            if not isinstance(node, dict):
                continue
            st = node.get("stream", {})
            emit(D.MIX_STREAMING, ch_key, st.get("streaming"))
            emit(D.MIX_MONITORING, ch_key, st.get("monitoring"))
            emit(D.MIX_CLASSIC, ch_key, node.get("classic"))

    _vol_cache = {}
    _mute_cache = {}

    def _current_volume(self, mix_key, ch_key):
        return self._vol_cache.get((mix_key, ch_key), 50)

    def _current_muted(self, mix_key, ch_key):
        return self._mute_cache.get((mix_key, ch_key), False)


def main():
    log.info("=== SteelSeries Sonar plugin v%s starting (log: %s) ===",
             D.PLUGIN_VERSION_STR, LOG_PATH)
    plugin = Plugin()
    try:
        plugin.serve()
    except KeyboardInterrupt:
        pass
    except Exception:
        log.exception("fatal error in serve()")
    log.info("=== plugin stopped ===")


if __name__ == "__main__":
    main()
