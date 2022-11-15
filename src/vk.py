'''IMPORTS'''
import selenium
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from random import randint

TIME_WAIT = 10

'''EXCEÇÕES'''
class VkErrorLoginException(Exception): pass

class Vk:
    def __init__(self, driver:uc.Chrome):
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
            else: return False

    def credencial_login(self, email:str, password:str):
        
        if self.check_login(): return
        
        '''Login in Vk using email and pass'''
        self.driver.get('https://vk.com')
        sleep(3)
        
        #Click in Login Button
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

        if self.check_login(): return
        else: raise VkErrorLoginException('Erro ao logar no Vk')

    def execute_task(self, type):
        pass
    
if __name__ == '__main__':
    pass