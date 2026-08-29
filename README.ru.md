# SteelSeries Sonar для Touch Portal

⭐ **Если плагин оказался полезным, поставьте репозиторию звезду — так его найдут другие пользователи Touch Portal.**

[English](README.md) | **Русский**

Плагин для управления **SteelSeries GG Sonar** из [Touch Portal](https://www.touch-portal.com/): Streamer Mode, личный микс и микс для зрителей, Master-вход микрофона, громкость и mute каналов.

> Проверено на Windows 11, SteelSeries GG 116.0.0 и Touch Portal 3.1. Sonar работает только в Windows.

## Все функции

### Маршрутизация устройств и микрофоны

| Действие Touch Portal | Что делает |
| --- | --- |
| **Set Personal Mix (Monitoring) source** | Выбирает физическое устройство вывода для личного микса в Streamer Mode. |
| **Set Streaming (audience) source** | Выбирает физическое устройство вывода для микса зрителей в Streamer Mode. |
| **Master - Set Microphone Input** | Выбирает физический микрофон в поле **МАСТЕР → Вход микрофона** Sonar. Один вход устанавливается для маршрутов Stream и Classic. |
| **Master - Next Microphone Input** | Переключает Master на следующий доступный физический микрофон одной кнопкой. |
| **Refresh audio devices** | Обновляет списки выходов и микрофонов после подключения, отключения или переименования USB-устройства. |
| **Set Stream redirection device** | Выбирает устройство для **Streaming (audience)**, **Monitoring (personal mix)** или **Microphone input**. |
| **Set Classic redirection device** | Выбирает устройство для маршрута Classic: **Game**, **Chat**, **Microphone input**, **Media** или **Aux**. |

Виртуальные микрофоны Sonar намеренно скрыты из списка Master, чтобы не создавать петли маршрутизации. Устройства с одинаковыми именами Windows получают различающий суффикс.

### Режимы и мониторинг

| Действие Touch Portal | Что делает |
| --- | --- |
| **Set Mode** | Напрямую включает режим **Classic** или **Stream**. |
| **Toggle Classic/Stream mode** | Переключает Classic и Stream одной кнопкой. |
| **Stream Monitoring (hear audience mix)** | Включает, выключает или переключает прослушивание микса зрителей: **On**, **Off**, **Toggle**. |

### Громкость и mute

| Действие Touch Portal | Что делает |
| --- | --- |
| **Set Volume** | Устанавливает точную громкость от 0 до 100%. |
| **Adjust Volume (+/-)** | Повышает или понижает громкость на выбранную величину от -100 до +100%. |
| **Mute / Unmute** | Выполняет **Mute**, **Unmute** или **Toggle** для выбранного микса и канала. |
| **Microphone Mute** | Отдельный one-tap mute микрофона: **On**, **Off** или **Toggle**. |

Громкость и mute поддерживаются для трёх миксов:

- **Classic**;
- **Stream – Streaming (audience)**;
- **Stream – Monitoring (personal mix)**.

В каждом миксе доступны каналы **Master**, **Game**, **Chat**, **Mic**, **Media** и **Aux**.

### Фейдер, состояния и настройки

- **Volume (slider)** — фейдер Touch Portal для любого поддерживаемого микса и канала.
- Состояние подключения плагина к Sonar.
- Текущий режим Sonar: Classic или Stream.
- Выбранные устройства Streaming, Monitoring и Master microphone.
- Отдельное состояние mute микрофона.
- Процент громкости и состояние mute для каждой комбинации микса и канала.
- Настраиваемые текстовые обозначения состояний muted и unmuted.
- Автоматический поиск локального Sonar API и переподключение после перезапуска Sonar или Touch Portal.

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
