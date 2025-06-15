from time import sleep
from random import randint, uniform
import random
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from data.config import config


class OpenProfileException(Exception):
    pass


class CloseProfileException(Exception):
    pass


class AdsPowerProfile:
    API_ROOT = 'http://local.adspower.com:50325'

    def __init__(self, name: str, _id: str, twitter_handle: str):
        self.name = name
        self._id = _id
        self.twitter_handle = twitter_handle
        self.driver = None

    @staticmethod
    def random_sleep():
        sleep(randint(config["min_random_pause_sec"], config["max_random_pause_sec"]))

    def human_click(self, click_object):
        size = click_object.size

        widht_deviation_pixels = randint(1, int(size["width"] * config["max_widht_deviation"]))
        height_deviation_pixels = randint(1, int(size["height"] * config["max_height_deviation"]))

        positive_width_deviation = randint(0, 1)
        positive_height_deviation = randint(0, 1)

        x = widht_deviation_pixels if positive_width_deviation else -widht_deviation_pixels
        y = height_deviation_pixels if positive_height_deviation else -height_deviation_pixels

        action = ActionChains(self.driver)
        action.move_to_element_with_offset(click_object, x, y).click().perform()

    def human_type(self, text: str):
        for char in text:
            sleep(uniform(config["min_typing_pause_seconds"], config["max_typing_pause_seconds"]))
            self.driver.switch_to.active_element.send_keys(char)

    def open_profile(self, headless: bool):
        url = self.API_ROOT + '/api/v1/browser/start'
        params = {
            "user_id": self._id,
            "open_tabs": "1",
            "ip_tab": "0",
            "headless": "1" if headless else "0",
        }

        response = requests.get(url, params=params).json()
        if response["code"] != 0:
            raise OpenProfileException('Failed to open profile')

        chrome_driver = response["data"]["webdriver"]
        chrome_options = Options()
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        chrome_options.add_experimental_option("debuggerAddress", response["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(chrome_driver, options=chrome_options, desired_capabilities=caps)
        self.driver = driver

    def close_profile(self):
        url_check_status = self.API_ROOT + '/api/v1/browser/active' + f'?user_id={self._id}'
        url_close_profile = self.API_ROOT + '/api/v1/browser/stop' + f'?user_id={self._id}'

        status = requests.get(url_check_status).json()
        if status['data']['status'] == 'Inactive':
            self.driver = None
            return

        response = requests.get(url_close_profile).json()
        if response["code"] != 0:
            raise CloseProfileException('Failed to close profile')

        self.driver = None
    
    
    def get_tweet_text(self):
        with open('data/tweets.txt', 'r', encoding="utf8") as file:
            tweets = [i.strip() for i in file]
        return random.choice(tweets)

    def get_random_image(self):
        images_path = config['route_to_folder_with_images']
        image_files = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]
        random_image = random.choice(image_files)
        return config['route_to_folder_with_images'] + random_image
    
    def get_random_names(self):
        with open('data/new_data/new_names.txt', 'r') as file:
            new_names = [i.strip() for i in file]
        return random.choice(new_names)

    def get_random_bio(self):
        with open('data/new_data/new_bio.txt', 'r') as file:
            new_bio = [i.strip() for i in file]
        return random.choice(new_bio)

    def post_tweet(self):

        self.driver.implicitly_wait(30)

        self.driver.get(f'https://twitter.com/{self.twitter_handle}')

        self.random_sleep()
        tweet_button = self.driver.find_element(By.CSS_SELECTOR, '[href="/compose/tweet"]')

        try:
            self.human_click(tweet_button)
        except:
            tweet_button.click()

        self.random_sleep()
        self.human_type(self.get_tweet_text())

        self.random_sleep()
        final_tweet_button = self.driver.find_element(By.XPATH, 
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]')

        try:
            self.human_click(final_tweet_button)
        except:
            final_tweet_button.click()

        self.random_sleep()



    def change_avatar(self):
        self.random_sleep()
        # ava input
        ava_input = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[3]/div/input')\
            .send_keys(self.get_random_image())
        self.random_sleep()


        apply_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(apply_button)
        except:
            apply_button.click()
        
        final_save_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(final_save_button)
        except:
            final_save_button.click()
        self.random_sleep()



    def change_avatar_firstly(self):
        self.random_sleep()
        
        # ava input
        ava_input = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div[3]/div/input')\
            .send_keys(self.get_random_image())
        
        self.random_sleep()

        apply_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(apply_button)
        except:
            apply_button.click()

        self.random_sleep()
        skip_for_now = self.driver.find_element(By.XPATH,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')

        self.random_sleep()
        try:
            self.human_click(skip_for_now)
        except:
            skip_for_now.click()

        next_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
        self.random_sleep()

        try:
            self.human_click(next_button)
        except:
            next_button.click()
        self.random_sleep()            




    def change_wallpaper(self):
        self.random_sleep()
        # wall input
        wall_input = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[3]/div/input') \
            .send_keys(self.get_random_image())

        self.random_sleep()


        apply_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(apply_button)
        except:
            apply_button.click()
        
        final_save_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(final_save_button)
        except:
            final_save_button.click()
        self.random_sleep()



    def change_bio(self):
        self.random_sleep()

        # bio input 
        bio_input  = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[4]/label/div/div[1]')
        try:
            self.human_click(bio_input)
        except:
            bio_input.click()

        self.random_sleep()
        self.human_type(self.get_random_bio())

        self.random_sleep()

        final_save_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(final_save_button)
        except:
            final_save_button.click()
        self.random_sleep()




    def change_name(self):
        self.random_sleep()
        # name_input 
        
        name_input  = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/label/div/div[1]')
        
        
        try:
            self.human_click(name_input)
        except:
            name_input.click()

        self.random_sleep()
        self.human_type(self.get_random_names())

        self.random_sleep()
        final_save_button = self.driver.find_element(By.XPATH,
        '//*[@id="layers"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div')

        try:
            self.human_click(final_save_button)
        except:
            final_save_button.click()

        self.random_sleep()


    def change_all_data_profile_algorithm(self, *args):


        self.driver.implicitly_wait(30)
        
        self.driver.get(f'https://twitter.com/{self.twitter_handle}')

        self.random_sleep()


        settings_button_text = self.driver.find_element(By.XPATH, 
        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/a/div/span/span').text
        
        # проверка если нет авы
        ava = True
        ava = False if settings_button_text == 'Set up profile' else ava

        # вход в настройки профиля
        settings_button = self.driver.find_element(By.XPATH,
        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/a')

        try:
            self.human_click(settings_button)
        except:
            settings_button.click()
        
        self.random_sleep()

        
        # проверка если нет авы, то ставим и выходим в некст профиль
        
        if (ava == False):
            self.change_avatar_firstly()
        else:
            if config["change_ava"] == True:
                self.change_avatar()
            elif config ["change_wallpaper"] == True:
                self.change_wallpaper()
            elif config ["change_bio"] == True:
                self.change_bio()
            elif config ["change_name"] == True:
                self.change_name()




        



    
