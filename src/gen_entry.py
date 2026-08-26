# -*- coding: utf-8 -*-
"""Generates entry.tp from the shared definitions in defs.py.

Run at build time:  python gen_entry.py > ../dist_build/SteelSeriesSonar/entry.tp
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import defs as D

ICON = f"%TP_PLUGIN_FOLDER%{D.PLUGIN_FOLDER}/icon.png"

DEVICE_PLACEHOLDER = ["<open the action in TP to load devices>"]


def choice(id_, label, choices, default=None):
    d = {"id": id_, "type": "choice", "label": label,
         "default": default if default is not None else (choices[0] if choices else ""),
         "valueChoices": choices}
    return d


def number(id_, label, default, mn, mx):
    return {"id": id_, "type": "number", "label": label, "default": default,
            "allowDecimals": False, "minValue": mn, "maxValue": mx}


def action(id_, name, fmt, data, hold=False):
    return {"id": id_, "name": name, "prefix": "Sonar", "type": "communicate",
            "tryInline": True, "hasHoldFunctionality": hold, "format": fmt, "data": data}


def build_actions():
    a = []
    # --- Priority quick actions --------------------------------------
    a.append(action(
        D.ACT_SET_MONITORING_SRC,
        "Sonar: Set Personal Mix (Monitoring) source",
        "Sonar: set Personal Mix (Monitoring) source to {$" + D.D_MONITORING_DEVICE + "$}",
        [choice(D.D_MONITORING_DEVICE, "Output device", DEVICE_PLACEHOLDER)]))

    a.append(action(
        D.ACT_SET_MIC_SRC,
        "Sonar: Master - Set Microphone Input",
        "Sonar: set Master microphone input to {$" + D.D_MIC_DEVICE + "$}",
        [choice(D.D_MIC_DEVICE, "Physical microphone", DEVICE_PLACEHOLDER)]))

    a.append(action(
        D.ACT_NEXT_MIC_SRC,
        "Sonar: Master - Next Microphone Input",
        "Sonar: switch Master to next physical microphone", []))

    a.append(action(
        D.ACT_REFRESH_DEVICES,
        "Sonar: Refresh audio devices",
        "Sonar: refresh audio device lists", []))

    a.append(action(
        D.ACT_SET_STREAMING_SRC,
        "Sonar: Set Streaming (audience) source",
        "Sonar: set Streaming (audience) source to {$" + D.D_STREAMING_DEVICE + "$}",
        [choice(D.D_STREAMING_DEVICE, "Output device", DEVICE_PLACEHOLDER)]))

    # --- Generic stream redirection (dependent device dropdown) ------
    a.append(action(
        D.ACT_STREAM_REDIRECT,
        "Sonar: Set Stream redirection device",
        "Sonar: set Stream redirection {$" + D.D_STREAM_REDIRECT + "$} to {$" + D.D_DEVICE + "$}",
        [choice(D.D_STREAM_REDIRECT, "Redirection", D.STREAM_REDIRECT_LABELS),
         choice(D.D_DEVICE, "Device", DEVICE_PLACEHOLDER)]))

    # --- Classic redirection -----------------------------------------
    a.append(action(
        D.ACT_CLASSIC_REDIRECT,
        "Sonar: Set Classic redirection device",
        "Sonar: set Classic redirection {$" + D.D_CLASSIC_REDIRECT + "$} to {$" + D.D_DEVICE_CLASSIC + "$}",
        [choice(D.D_CLASSIC_REDIRECT, "Redirection", D.CLASSIC_REDIRECT_LABELS),
         choice(D.D_DEVICE_CLASSIC, "Device", DEVICE_PLACEHOLDER)]))

    # --- Mode ---------------------------------------------------------
    a.append(action(
        D.ACT_SET_MODE, "Sonar: Set Mode",
        "Sonar: set mode to {$" + D.D_MODE + "$}",
        [choice(D.D_MODE, "Mode", D.MODE_CHOICES, default="Stream")]))

    a.append(action(
        D.ACT_TOGGLE_MODE, "Sonar: Toggle Classic/Stream mode",
        "Sonar: toggle Classic/Stream mode", []))

    # --- Volume set / adjust -----------------------------------------
    a.append(action(
        D.ACT_SET_VOLUME, "Sonar: Set Volume",
        "Sonar: set {$" + D.D_MIX + "$} / {$" + D.D_CHANNEL + "$} volume to {$" + D.D_VOLUME + "$}%",
        [choice(D.D_MIX, "Mix", D.MIX_LABELS, default=D.MIX_LABELS[2]),
         choice(D.D_CHANNEL, "Channel", D.CHANNEL_LABELS, default="Master"),
         number(D.D_VOLUME, "Volume %", 50, 0, 100)]))

    a.append(action(
        D.ACT_ADJ_VOLUME, "Sonar: Adjust Volume (+/-)",
        "Sonar: adjust {$" + D.D_MIX + "$} / {$" + D.D_CHANNEL + "$} volume by {$" + D.D_VOL_DELTA + "$}%",
        [choice(D.D_MIX, "Mix", D.MIX_LABELS, default=D.MIX_LABELS[2]),
         choice(D.D_CHANNEL, "Channel", D.CHANNEL_LABELS, default="Master"),
         number(D.D_VOL_DELTA, "Delta %", 5, -100, 100)]))

    # --- Mute ---------------------------------------------------------
    a.append(action(
        D.ACT_MUTE, "Sonar: Mute / Unmute",
        "Sonar: {$" + D.D_MUTE_ACTION + "$} {$" + D.D_MIX + "$} / {$" + D.D_CHANNEL + "$}",
        [choice(D.D_MIX, "Mix", D.MIX_LABELS, default=D.MIX_LABELS[2]),
         choice(D.D_CHANNEL, "Channel", D.CHANNEL_LABELS, default="Master"),
         choice(D.D_MUTE_ACTION, "Action", D.MUTE_ACTIONS)]))

    # --- Microphone mute (dedicated one-tap) -------------------------
    a.append(action(
        D.ACT_MUTE_MIC, "Sonar: Microphone Mute",
        "Sonar: microphone mute {$" + D.D_ONOFF + "$}",
        [choice(D.D_ONOFF, "State", D.ONOFF_TOGGLE, default="Toggle")]))

    # --- Stream monitoring toggle ------------------------------------
    a.append(action(
        D.ACT_STREAM_MONITORING, "Sonar: Stream Monitoring (hear audience mix)",
        "Sonar: turn Stream monitoring {$" + D.D_ONOFF + "$}",
        [choice(D.D_ONOFF, "State", D.ONOFF_TOGGLE)]))

    return a


def build_connectors():
    return [{
        "id": D.CON_VOLUME,
        "name": "Sonar: Volume (slider)",
        "format": "Sonar: {$" + D.D_MIX + "$} / {$" + D.D_CHANNEL + "$} volume",
        "data": [
            choice(D.D_MIX, "Mix", D.MIX_LABELS, default=D.MIX_LABELS[2]),
            choice(D.D_CHANNEL, "Channel", D.CHANNEL_LABELS, default="Master"),
        ],
    }]


def build_states():
    st = []
    st.append({"id": D.S_CONNECTED, "type": "text", "desc": "Sonar: Plugin connected", "default": "0"})
    st.append({"id": D.S_MODE, "type": "text", "desc": "Sonar: Current mode", "default": ""})
    st.append({"id": D.S_REDIRECT_STREAMING, "type": "text",
               "desc": "Sonar: Streaming (audience) device", "default": ""})
    st.append({"id": D.S_REDIRECT_MONITORING, "type": "text",
               "desc": "Sonar: Monitoring (personal mix) device", "default": ""})
    st.append({"id": D.S_REDIRECT_MIC, "type": "text",
               "desc": "Sonar: Master microphone input device", "default": ""})
    st.append({"id": D.S_MIC_MUTED, "type": "text",
               "desc": "Sonar: Microphone muted", "default": ""})

    for mix_label, mix_key in D.MIXES:
        for ch_label, ch_key in D.CHANNELS:
            st.append({"id": D.s_volume(mix_key, ch_key), "type": "text",
                       "desc": f"Sonar: Volume {mix_label} / {ch_label} (%)", "default": "0"})
            st.append({"id": D.s_mute(mix_key, ch_key), "type": "text",
                       "desc": f"Sonar: Mute {mix_label} / {ch_label}", "default": ""})
    return st


def build_settings():
    return [
        {"name": D.SET_MUTED_LABEL, "type": "text", "default": "muted", "readOnly": False},
        {"name": D.SET_UNMUTED_LABEL, "type": "text", "default": "unmuted", "readOnly": False},
    ]


def build_entry():
    return {
        "sdk": D.TP_API,
        "version": D.PLUGIN_VERSION,
        "name": D.PLUGIN_NAME,
        "id": D.PLUGIN_ID,
        "plugin_start_cmd": f"%TP_PLUGIN_FOLDER%{D.PLUGIN_FOLDER}\\{D.EXE_NAME}",
        "configuration": {"colorDark": "#232B32", "colorLight": "#272F37", "parentCategory": "audio"},
        "settings": build_settings(),
        "categories": [{
            "id": D.pid("cat.main"),
            "name": "SteelSeries Sonar",
            "imagepath": ICON,
            "actions": build_actions(),
            "connectors": build_connectors(),
            "states": build_states(),
            "events": [],
        }],
    }


if __name__ == "__main__":
    entry = build_entry()
    text = json.dumps(entry, indent=2, ensure_ascii=False)
    out = sys.argv[1] if len(sys.argv) > 1 else None
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
