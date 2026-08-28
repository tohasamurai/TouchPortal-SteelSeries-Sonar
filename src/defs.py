# -*- coding: utf-8 -*-
"""Shared definitions for the SteelSeries Sonar TouchPortal plugin.

Imported by both plugin.py (runtime, bundled into the exe) and
gen_entry.py (build time, generates entry.tp). Keeping every id and
label in one place guarantees entry.tp and the plugin stay in sync.
"""

PLUGIN_ID = "steelseries_sonar_tp"
PLUGIN_NAME = "SteelSeries Sonar"
PLUGIN_VERSION = 107  # integer, bumped on each release
PLUGIN_VERSION_STR = "1.0.7"

# TouchPortal API/SDK version. TP 3.1 == 6.
TP_API = 6

# Executable / folder names used by plugin_start_cmd in entry.tp.
PLUGIN_FOLDER = "SteelSeriesSonar"          # folder name inside the .tpp zip
EXE_NAME = "SteelSeriesSonarPlugin.exe"     # built by PyInstaller


def pid(suffix: str) -> str:
    """Namespaced id helper."""
    return f"{PLUGIN_ID}.{suffix}"


# --- Mix submixes (Streamer mode has two, Classic has one) ---------------
# key used in the volume/mute state ids and, for stream, in the API path.
MIX_CLASSIC = "classic"
MIX_STREAMING = "streaming"
MIX_MONITORING = "monitoring"

# (label shown in TP, mix key)
MIXES = [
    ("Classic", MIX_CLASSIC),
    ("Stream – Streaming (audience)", MIX_STREAMING),
    ("Stream – Monitoring (personal mix)", MIX_MONITORING),
]

# --- Channels (virtual sub-devices) --------------------------------------
# (label, api_key). api_key matches Sonar's volumeSettings device keys.
CHANNELS = [
    ("Master", "Master"),
    ("Game", "game"),
    ("Chat", "chatRender"),
    ("Mic", "chatCapture"),
    ("Media", "media"),
    ("Aux", "aux"),
]
CHANNEL_LABELS = [c[0] for c in CHANNELS]
CHANNEL_KEY_BY_LABEL = {c[0]: c[1] for c in CHANNELS}

MIX_LABELS = [m[0] for m in MIXES]
MIX_KEY_BY_LABEL = {m[0]: m[1] for m in MIXES}

# --- Stream-mode redirections (device switching) -------------------------
# (label, redirect_key, data_flow)  data_flow: "render" (output) / "capture" (input)
STREAM_REDIRECTS = [
    ("Streaming (audience)", "streaming", "render"),
    ("Monitoring (personal mix)", "monitoring", "render"),
    ("Microphone input", "mic", "capture"),
]
STREAM_REDIRECT_LABELS = [r[0] for r in STREAM_REDIRECTS]
STREAM_REDIRECT_KEY_BY_LABEL = {r[0]: r[1] for r in STREAM_REDIRECTS}
STREAM_REDIRECT_FLOW_BY_LABEL = {r[0]: r[2] for r in STREAM_REDIRECTS}

# --- Classic-mode redirections -------------------------------------------
CLASSIC_REDIRECTS = [
    ("Game", "game", "render"),
    ("Chat", "chat", "render"),
    ("Microphone input", "mic", "capture"),
    ("Media", "media", "render"),
    ("Aux", "aux", "render"),
]
CLASSIC_REDIRECT_LABELS = [r[0] for r in CLASSIC_REDIRECTS]
CLASSIC_REDIRECT_KEY_BY_LABEL = {r[0]: r[1] for r in CLASSIC_REDIRECTS}
CLASSIC_REDIRECT_FLOW_BY_LABEL = {r[0]: r[2] for r in CLASSIC_REDIRECTS}

# --- Mute action choices --------------------------------------------------
MUTE_ACTIONS = ["Mute", "Unmute", "Toggle"]
ONOFF_TOGGLE = ["On", "Off", "Toggle"]
MODE_CHOICES = ["Classic", "Stream"]

# --- Action / connector / data ids ---------------------------------------
ACT_SET_MODE = pid("act.setMode")
ACT_TOGGLE_MODE = pid("act.toggleMode")
ACT_SET_VOLUME = pid("act.setVolume")
ACT_ADJ_VOLUME = pid("act.adjVolume")
ACT_MUTE = pid("act.mute")
ACT_STREAM_REDIRECT = pid("act.streamRedirect")
ACT_CLASSIC_REDIRECT = pid("act.classicRedirect")
ACT_SET_MONITORING_SRC = pid("act.setMonitoringSource")
ACT_SET_STREAMING_SRC = pid("act.setStreamingSource")
ACT_SET_MIC_SRC = pid("act.setMicSource")
ACT_NEXT_MIC_SRC = pid("act.nextMicSource")
ACT_REFRESH_DEVICES = pid("act.refreshDevices")
ACT_STREAM_MONITORING = pid("act.streamMonitoring")
ACT_MUTE_MIC = pid("act.muteMic")

CON_VOLUME = pid("con.volume")

# data field ids (suffix under an action)
D_MODE = pid("data.mode")
D_MIX = pid("data.mix")
D_CHANNEL = pid("data.channel")
D_VOLUME = pid("data.volume")
D_VOL_DELTA = pid("data.volDelta")
D_MUTE_ACTION = pid("data.muteAction")
D_STREAM_REDIRECT = pid("data.streamRedirect")
D_CLASSIC_REDIRECT = pid("data.classicRedirect")
D_DEVICE = pid("data.device")
D_DEVICE_CLASSIC = pid("data.deviceClassic")
D_MONITORING_DEVICE = pid("data.monitoringDevice")
D_STREAMING_DEVICE = pid("data.streamingDevice")
D_MIC_DEVICE = pid("data.micDevice")
D_ONOFF = pid("data.onoff")

# --- State ids -----------------------------------------------------------
S_MODE = pid("state.mode")
S_REDIRECT_STREAMING = pid("state.redirect.streaming")
S_REDIRECT_MONITORING = pid("state.redirect.monitoring")
S_REDIRECT_MIC = pid("state.redirect.mic")
S_CONNECTED = pid("state.connected")
S_MIC_MUTED = pid("state.micMuted")


def s_volume(mix_key: str, channel_key: str) -> str:
    return pid(f"state.vol.{mix_key}.{channel_key}")


def s_mute(mix_key: str, channel_key: str) -> str:
    return pid(f"state.mute.{mix_key}.{channel_key}")


# --- Settings ids --------------------------------------------------------
SET_MUTED_LABEL = "Muted state label"
SET_UNMUTED_LABEL = "Unmuted state label"
