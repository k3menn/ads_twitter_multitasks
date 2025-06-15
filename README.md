# AdsPower Twitter Warmup

Автоматизация прогрева Twitter-аккаунтов с помощью браузерных профилей AdsPower и Selenium.

## Описание

Скрипт автоматически выполняет действия (постинг твитов, изменение профиля и др.) для заданных Twitter-аккаунтов через индивидуальные браузерные профили AdsPower. Это помогает имитировать естественную активность и снижать риски блокировок.

## Структура проекта

```
adspower-twitter-warmup/
├── adspower_twitter_warmup.py      # Главный скрипт запуска
├── requirements.txt                # Зависимости (заполните при необходимости)
├── .gitignore
├── src/
│   └── Profile.py                  # Класс AdsPowerProfile и логика действий
├── data/
│   ├── config.py                   # Конфиг с параметрами работы
│   ├── profile_ids.py              # Сопоставление профилей AdsPower и их ID
│   ├── twitter_handles.txt         # Список Twitter-логинов (по одному в строке)
│   ├── tweets.txt                  # Примеры твитов для постинга
│   └── new_data/
│       ├── new_names.txt           # (опционально) Имена для смены профиля
│       ├── new_bio.txt             # (опционально) Биографии для профиля
│       └── new_images/             # (опционально) Картинки для аватарок/обоев
│   └── screenshots/                # Скриншоты действий
```

## Установка

1. **Установите Python 3.8+**
2. **Установите зависимости:**
   ```
   pip install -r requirements.txt
   ```
   _Примечание: заполните requirements.txt нужными библиотеками, например:_
   ```
   selenium
   loguru
   requests
   ```

3. **Настройте AdsPower**  
   Убедитесь, что AdsPower API доступен по адресу, указанному в `src/Profile.py` (`http://local.adspower.com:50325`).

## Настройка

- **data/config.py** — основные параметры работы:
  - `headless`: запускать браузер в фоновом режиме (True/False)
  - `profiles_to_warmup_min`, `profiles_to_warmup_max`: диапазон номеров профилей для прогрева
  - `min_idle_minutes`, `max_idle_minutes`: пауза между аккаунтами
  - `min_random_pause_sec`, `max_random_pause_sec`: пауза между действиями
  - `min_typing_pause_seconds`, `max_typing_pause_seconds`: пауза между вводом символов
  - `max_height_deviation`, `max_widht_deviation`: рандомизация кликов
  - `route_to_folder_with_images`: путь к папке с изображениями для профиля
  - `post_tweet`, `change_ava`, `change_bio`, `change_wallpaper`, `change_name`: включение/отключение действий

- **data/profile_ids.py** — словарь: имя профиля → AdsPower ID

- **data/twitter_handles.txt** — список логинов Twitter (по одному в строке, соответствуют профилям)

- **data/tweets.txt** — список твитов для постинга

## Запуск

1. Заполните файлы `profile_ids.py`, `twitter_handles.txt`, `tweets.txt` и при необходимости — дополнительные данные для профиля.
2. Запустите AdsPower и убедитесь, что API работает.
3. Запустите основной скрипт:
   ```
   python adspower_twitter_warmup.py
   ```

## Возможности

- Постинг твитов
- Изменение аватарки, имени, био, обоев (опционально, через config.py)
- Скриншоты действий для каждого профиля
- Гибкая настройка пауз и диапазонов

## Важно

- Каждый профиль должен иметь уникальный Twitter-логин и AdsPower ID.
- Скрипт имитирует "человеческие" действия (рандомизация кликов, паузы).
- Для работы требуется установленный и запущенный AdsPower с открытым API.

---

Если нужно добавить разделы (FAQ, примеры, troubleshooting) — дайте знать! 