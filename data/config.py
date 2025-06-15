config = {
    # запускать браузер в скрытом режиме (True / False)
    "headless": True,

    # сколько профилей прогреть диапазон
    "profiles_to_warmup_min": 0,
    "profiles_to_warmup_max": 100,


    # пауза между аккаунтами в минутах
    "min_idle_minutes": 0,
    "max_idle_minutes": 0,

    # пауза перед следующим действием в рамках прогрева
    "min_random_pause_sec": 4,
    "max_random_pause_sec": 8,

    # пауза между вводом символов в процессе печатания
    "min_typing_pause_seconds": 0.02,
    "max_typing_pause_seconds": 0.8,

    # селениум кликает всегда в один и тот же пиксель, этот параметр отвечает
    # за максимальное рандомное отклонение от этого пикселя (0 - 1)
    "max_height_deviation": 0.02,
    "max_widht_deviation": 0.02,

    # путь к папке с изображениями для аватарок и обоев
    "route_to_folder_with_images": "/Users/Downloads/Adspower-twitter-warmup-main/data/new_data/new_images/",

    # действия
    "post_tweet":True,
    "change_ava": False,
    "change_bio": False,
    "change_wallpaper": False,
    "change_name": False
}
