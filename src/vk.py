'''IMPORTS'''
import selenium
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from easy_webdriver import *

from time import sleep
from random import randint

TIME_WAIT = 15

'''EXCEÇÕES'''


class VkErrorLoginException(Exception):
    pass


class VkErrorDoingTask(Exception):
    pass


class VkErrorInvalidTaskType(Exception):
    pass


class Vk:
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
        self.login_status = False

    def check_login(self):
        self.driver.get('https://vk.com/feed')
        sleep(3)
        if self.driver.current_url == 'https://vk.com/feed':
            return True
        else:
            sleep(5)
            if self.driver.current_url == 'https://vk.com/feed':
                return True
            else:
                return False

    def credencial_login(self, email: str, password: str):

        if self.check_login():
            return

        '''Login in Vk using email and pass'''
        self.driver.get('https://vk.com')
        sleep(3)

        # Click in Login Button
        login_button = WebDriverWait(self.driver, TIME_WAIT).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'button[type="submit"]'
        ))).click()

        type_email = WebDriverWait(self.driver, TIME_WAIT).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'input[name="login"]'))).send_keys(email)
        sleep(2)

        enter_botton = WebDriverWait(self.driver, TIME_WAIT).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'button[type="submit"]'
        ))).click()

        type_password = WebDriverWait(self.driver, TIME_WAIT).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'input[name="password"]'
        ))).send_keys(password)
        sleep(2)

        login_button = WebDriverWait(self.driver, TIME_WAIT).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'button[type="submit"]'
        ))).click()

        sleep(5)

        if self.check_login():
            return
        else:
            raise VkErrorLoginException('Erro ao logar no Vk')

    def follow_page(self):
        try:
            # Click to follow
            element = WebDriverWait(self.driver, TIME_WAIT).until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'button[id="public_subscribe"]'
            )))
            element.click()

            # Check if following
            text = WebDriverWait(self.driver, TIME_WAIT).until  (EC.visibility_of_all_elements_located((
            By.CSS_SELECTOR, 'button[id="page_actions_btn"]'
            )))[0].text

            if (text == 'Following'):
                return
        except:
            raise VkErrorDoingTask()

    def join_group(self):
        try:
            # Click to follow
            element = WebDriverWait(self.driver, TIME_WAIT).until(EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'button[id="join_button"]'
            )))
            element.click()

            # Check if following
            text = WebDriverWait(self.driver, TIME_WAIT).until(EC.visibility_of_all_elements_located((
                By.CSS_SELECTOR, 'span[class="FlatButton__content"]'
            )))[0].text

            if (text == "You're a member"):
                return
        except:
            raise VkErrorDoingTask()

    def like_post(self):
        try:
            # Click to follow
            element = WebDriverWait(self.driver, TIME_WAIT).until(EC.visibility_of_element_located((
                By.CLASS_NAME, 'PostBottomAction.PostBottomAction--withBg.PostButtonReactions.PostButtonReactions--post'
            )))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()

            # Check if following
            text = WebDriverWait(self.driver, TIME_WAIT).until(EC.visibility_of_all_elements_located((
                By.CLASS_NAME, 'PostBottomAction.PostBottomAction--withBg.PostButtonReactions.PostButtonReactions--post.PostButtonReactions--icon-active.PostButtonReactions--active'
            )))[0].get_attribute('aria-label')

            if (text == "Remove Like"):
                return
        except:
            raise VkErrorDoingTask()

    def execute_task(self, type: str):
        if type == 'Follow page':
            self.follow_page()
        elif type == 'Join group':
            self.join_group()
        elif type == 'Liking post':
            self.like_post()
        else:
            raise VkErrorInvalidTaskType('')

        sleep(1)

if __name__ == '__main__':
    pass
