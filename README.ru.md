# SteelSeries Sonar для Touch Portal

⭐ **Если плагин оказался полезным, поставьте репозиторию звезду — так его найдут другие пользователи Touch Portal.**

[English](README.md) | **Русский**

Плагин для управления **SteelSeries GG Sonar** из [Touch Portal](https://www.touch-portal.com/): Streamer Mode, личный микс и микс для зрителей, Master-вход микрофона, громкость и mute каналов.

> Проверено на Windows 11, SteelSeries GG 116.0.0 и Touch Portal 3.1. Sonar работает только в Windows.

## Возможности

- Выбор устройств для **Monitoring (Personal Mix)** и **Streaming (Audience Mix)**.
- Выбор физического микрофона в **МАСТЕР → Вход микрофона** Sonar.
- Циклическое переключение микрофонов одной кнопкой.
- Classic / Stream mode и управление маршрутизацией.
- Громкость и mute каналов Master, Game, Chat, Mic, Media и Aux.
- Слайдеры, states и автопереподключение после перезапуска.

## Установка

1. Скачай последний `SteelSeriesSonar-vX.Y.Z.tpp` из [Releases](../../releases).
2. В Touch Portal открой **Settings → Import plug-in…**.
3. Выбери `.tpp`, затем полностью перезапусти Touch Portal.
4. Действия появятся в категории **SteelSeries Sonar**.

Плагину не нужны права администратора и интернет. Он обращается только к локальному Sonar API на `127.0.0.1`.

## Master microphone

Добавь действие **Sonar: Master - Set Microphone Input** и выбери физический микрофон. Для переключения одной кнопкой используй **Sonar: Master - Next Microphone Input**. Виртуальные устройства Sonar скрыты, чтобы не создавать петлю маршрутизации.

## Документация

- [Полное использование](docs/USAGE.md)
- [Устранение неполадок](docs/TROUBLESHOOTING.md)
- [История изменений](CHANGELOG.md)

## Иконки кнопок

| Гарнитура | Студийный микрофон |
| --- | --- |
| ![Гарнитура](assets/headset_microphone.png) | ![Студийный микрофон](assets/studio_microphone.png) |

Иконка категории и картинки кнопок — разные элементы. Картинки кнопок назначаются вручную на вкладке изображения в редакторе Touch Portal.

## Сборка

Требования: Python 3.12, PyInstaller и Pillow.

```powershell
python -m pip install pyinstaller pillow
.\build.ps1 -Version 1.0.7
```

## Ограничения

- Некоторые Classic volume-эндпоинты в GG 116 могут вернуть HTTP 500; Streamer-миксы работают стабильно.
- `chatMix` не включён: его старый endpoint отсутствует в GG 116.

## Лицензия

[MIT](LICENSE)
