from random import choice, randint
from sys import stderr
from time import sleep

from loguru import logger

from src.Profile import AdsPowerProfile
from data.config import config
from data.profile_ids import profile_ids


logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")

def start_warmup(_profile: AdsPowerProfile):
    logger.info(f'{_profile.name} - starting warmup')
    try:
        _profile.open_profile(config["headless"])
        _profile.driver.set_window_size(1100, 950)
    except Exception as _e:
        logger.error(f'{_profile.name} - failed to open profile, reason: {_e}')
        return
    if config['post_tweet'] == True:
        logger.info(f'{_profile.name} - posting tweet')
        try:
            _profile.post_tweet()
            # _profile.change_all_data_profile()
            
            logger.info(f'{_profile.name} - tweet posted')
        except Exception as _e:
            logger.error(f'{_profile.name} - failed to post tweet, reason: {_e}')
            return _profile.name
        finally:
            sleep(5)
            _profile.driver.get_screenshot_as_file(f"data/screenshots/{_profile.name}_posted_tweet.png")

    else:
        logger.info(f'{_profile.name} - doing action')
        try:
            _profile.change_all_data_profile_algorithm()
            logger.info(f'{_profile.name} - action done')
        except Exception as _e:
            logger.error(f'{_profile.name} - action failed, reason: {_e}')
            return _profile.name


    logger.info(f'{_profile.name} - closing profile')
    try:
        _profile.close_profile()
    except Exception as _e:
        logger.error(f'{_profile.name} - failed to close profile, reason: {_e}')


if __name__ == "__main__":
    with open('data/twitter_handles.txt', 'r') as file:
        twitter_handles = [i.strip() for i in file]

    profiles = []
    for i, (profile_number, profile_id) in enumerate(profile_ids.items()):
        profiles.append(AdsPowerProfile(profile_number, profile_id, twitter_handles[i]))


    if config["profiles_to_warmup_max"] > len(profiles):
        logger.error(f"Amount of profiles to warmup > total amount of profiles, adjusted")
        config["profiles_to_warmup"] = len(profiles)
    err = 0
    err_list = []
    for i in range(config["profiles_to_warmup_min"], config["profiles_to_warmup_max"]):
        tmp_res = start_warmup(profiles[i])

        if  tmp_res != None:
            err +=1
            err_list.append(tmp_res)

        sleep_time = randint(config["min_idle_minutes"] * 60, config["max_idle_minutes"] * 60)
        logger.info(f'Sleeping {round(sleep_time / 60, 1)} minutes')
        sleep(sleep_time)
    
    logger.info(f"Количество ошибок: {err}")
    logger.info(f"Номера профилей с ошибками: {err_list}")

