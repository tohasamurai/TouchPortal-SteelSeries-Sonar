# SteelSeries Sonar for Touch Portal

⭐ **If this plugin helps you, please star the repository — it helps other Touch Portal users find it.**

**English** | [Русский](README.ru.md)

A Windows plugin for controlling **SteelSeries GG Sonar** from [Touch Portal](https://www.touch-portal.com/). It provides quick access to Streamer Mode, Personal and Audience mixes, the Master microphone input, channel volume, and mute controls.

> Tested on Windows 11, SteelSeries GG 116.0.0, and Touch Portal 3.1. Sonar is Windows-only.

## Features

- Select devices for **Monitoring (Personal Mix)** and **Streaming (Audience Mix)**.
- Select the physical microphone shown under **MASTER → Microphone Input** in Sonar.
- Cycle through available microphones with one button.
- Switch Classic / Stream mode and control routing devices.
- Control volume and mute for Master, Game, Chat, Mic, Media, and Aux.
- Touch Portal sliders, states, and automatic reconnection.

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
