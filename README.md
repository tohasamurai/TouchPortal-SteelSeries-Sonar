# SteelSeries Sonar for Touch Portal

⭐ **If this plugin helps you, please star the repository — it helps other Touch Portal users find it.**

**English** | [Русский](README.ru.md)

A Windows plugin for controlling **SteelSeries GG Sonar** from [Touch Portal](https://www.touch-portal.com/). It provides quick access to Streamer Mode, Personal and Audience mixes, the Master microphone input, channel volume, and mute controls.

> Tested on Windows 11, SteelSeries GG 116.0.0, and Touch Portal 3.1. Sonar is Windows-only.

## All functions

### Device routing and microphones

| Touch Portal action | What it does |
| --- | --- |
| **Set Personal Mix (Monitoring) source** | Selects the physical output device used for your personal monitoring mix in Streamer Mode. |
| **Set Streaming (audience) source** | Selects the physical output device used for the audience mix in Streamer Mode. |
| **Master - Set Microphone Input** | Selects the physical microphone shown under **MASTER → Microphone Input** in Sonar. The same input is written to the Stream and Classic routes. |
| **Master - Next Microphone Input** | Switches Master to the next available physical microphone with one button. |
| **Refresh audio devices** | Reloads output and microphone lists after a USB device is connected, removed, or renamed. |
| **Set Stream redirection device** | Selects a device for **Streaming (audience)**, **Monitoring (personal mix)**, or **Microphone input**. |
| **Set Classic redirection device** | Selects a device for the Classic **Game**, **Chat**, **Microphone input**, **Media**, or **Aux** route. |

Virtual Sonar microphones are intentionally hidden from the Master microphone list to prevent routing loops. Devices with identical Windows names are displayed with a distinguishing suffix.

### Modes and monitoring

| Touch Portal action | What it does |
| --- | --- |
| **Set Mode** | Selects **Classic** or **Stream** mode directly. |
| **Toggle Classic/Stream mode** | Switches between Classic and Stream modes with one button. |
| **Stream Monitoring (hear audience mix)** | Turns audience-mix monitoring **On**, **Off**, or **Toggle**. |

### Volume and mute

| Touch Portal action | What it does |
| --- | --- |
| **Set Volume** | Sets an exact volume from 0 to 100%. |
| **Adjust Volume (+/-)** | Raises or lowers volume by a chosen amount from -100 to +100%. |
| **Mute / Unmute** | Applies **Mute**, **Unmute**, or **Toggle** to the selected mix and channel. |
| **Microphone Mute** | Dedicated one-tap microphone mute with **On**, **Off**, or **Toggle**. |

Volume and mute controls support these mixes:

- **Classic**;
- **Stream – Streaming (audience)**;
- **Stream – Monitoring (personal mix)**.

Each mix supports **Master**, **Game**, **Chat**, **Mic**, **Media**, and **Aux** channels.

### Slider, states, and settings

- **Volume (slider)** — a Touch Portal fader for any supported mix and channel.
- Connection state: whether the plugin is connected to Sonar.
- Current Sonar mode: Classic or Stream.
- Selected Streaming, Monitoring, and Master microphone devices.
- Dedicated microphone-muted state.
- Volume percentage and mute state for every mix/channel combination.
- Customizable text labels for muted and unmuted states.
- Automatic Sonar API discovery and reconnection after Sonar or Touch Portal restarts.

## Installation

1. Download the latest `SteelSeriesSonar-vX.Y.Z.tpp` from [Releases](../../releases).
2. In Touch Portal, open **Settings → Import plug-in…**.
3. Select the `.tpp`, then fully restart Touch Portal.
4. Find the actions under **SteelSeries Sonar**.

No administrator privileges or internet access are required. The plugin communicates only with the local Sonar API at `127.0.0.1`.

## Master microphone

Add **Sonar: Master - Set Microphone Input** and choose a physical microphone. Use **Sonar: Master - Next Microphone Input** to cycle devices with one button. Virtual Sonar devices are hidden to prevent routing loops.

## Documentation

- [Full usage guide (Russian)](docs/USAGE.md)
- [Troubleshooting (Russian)](docs/TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)

## Button icons

| Headset microphone | Studio microphone |
| --- | --- |
| ![Headset microphone](assets/headset_microphone.png) | ![Studio microphone](assets/studio_microphone.png) |

The category icon and button images are separate. Assign button images manually from the image tab in Touch Portal's button editor.

## Build

Requirements: Python 3.12, PyInstaller, and Pillow.

```powershell
python -m pip install pyinstaller pillow
.\build.ps1 -Version 1.0.7
```

## Known limitations

- Some Classic volume endpoints in GG 116 may return HTTP 500; Streamer mixes work reliably.
- `chatMix` is not included because its old local endpoint is absent in GG 116.

## License

[MIT](LICENSE)
