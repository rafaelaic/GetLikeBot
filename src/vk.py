'''IMPORTS'''
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

class VkErrorCheckTask(Exception):
    pass


class Vk:
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
        self.login_status = self.check_login()

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
            self.login_status = True
            return
        else:
            raise VkErrorLoginException('Erro ao logar no Vk')

    def check_18box(self):
        try:
            pop_up = find_element(self.driver, 'class', 'popup_box_container', wait=1)
            
            #click on box
            find_element(pop_up, 'class', 'checkbox group_age_checkbox').click()
            
            find_element(pop_up, 'class', 'FlatButton FlatButton--primary FlatButton--size-m').click()
            sleep(2)
        except:
            pass

    #Follow user
    def check_following_user(self, follow_button):
        try:
            if follow_button.text in ['Following', 'Request sent', 'Message']: return True
            else: return False
        except:
            raise VkErrorCheckTask('Invalid Follow Button')
        
    def follow_user(self):
        try:
            #Get follow button
            follow_button = find_element(self.driver, 'class', 'ProfileHeaderButton', 'presence')
            
            #Return if already following
            if(self.check_following_user(follow_button)): return
            
            #Click to follow
            follow_button.click()
            
            #Get follow button
            '''follow_button = find_element(self.driver, 'class', 'ProfileHeaderButton', 'presence')
            
            #Return if following
            if(self.check_following_user(follow_button)): return
            else: raise VkErrorCheckTask("Error check task Vk")'''
        except:
            raise VkErrorDoingTask()


    #Follow page
    def check_following_page(self, follow_button):
        try:
            if follow_button.text in ['Following', 'Request sent', 'Message']: return True
            else: return False
        except:
            raise VkErrorCheckTask('Invalid Follow Button')
    
    def follow_page(self):
        try:
            for element in find_elements(self.driver, 'class', 'FlatButton__in', 'presence'):
            #Click on follow
                if element.text == 'Follow': break

            if element.text != 'Follow': raise VkErrorDoingTask('Follow button not found')
            
            #Check if following
            if(self.check_following_page(element)): return
            
            #Click on follow
            element.click()
            
            ''' #Check if following
            for element in find_elements(self.driver, 'class', 'FlatButton__in', 'presence'):
                if(self.check_following_page(element)): return
            raise VkErrorCheckTask("Error check task Vk")'''
        except:
            raise VkErrorDoingTask()


    #Join group
    def check_following_group(self, follow_button):
        try:
            if follow_button.text in ["You're a member", "Following", "Message"]: return True
            else: return False
        except:
            raise VkErrorCheckTask('Invalid Follow Button')
    
    def join_group(self):
        try:
            for element in find_elements(self.driver, 'class', 'FlatButton__in', 'presence'):
            #Find element
                if element.text in ['Follow', 'Join community']: break

            if element.text not in ['Follow', 'Join community']: raise VkErrorDoingTask('Follow button not found')
            
            #Check if following
            if(self.check_following_group(element)):return
            
            #Click on join
            element.click()
            
            '''#Check if following
            for element in find_elements(self.driver, 'class', 'FlatButton__in', 'presence'):
                if self.check_following_group(element): return
            raise VkErrorCheckTask("Error check task Vk")'''
        except:
            raise VkErrorDoingTask('Error join group')

    #Like photo
    def like_photo(self):

        try:
            try:
                #Check if already following
                find_element(self.driver, 'class', 'like_btn like _like active', 'presence')
                return
            except:
                pass
            
            #Click on follow
            find_element(self.driver, 'class', 'like_btn like _like', 'presence').click()

            #Check if following
            find_element(self.driver, 'class', 'like_btn like _like animate active', 'presence')
        except:
            raise VkErrorDoingTask('Error liking photo')
        
    #Like post
    def like_post(self):
        try:
            #Get like button
            like_button = find_element(self.driver, 'class', 'PostBottomActionContainer PostButtonReactionsContainer', 'presence')

            #Scroll to button and click
            self.driver.execute_script(f"window.scrollTo(0, {int(like_button.location['y']/2)})")
            like_button.click()
            
            #Check if like
            find_element(like_button, 'class', 'PostBottomAction PostBottomAction--withBg PostButtonReactions PostButtonReactions--post PostButtonReactions--icon-active PostButtonReactions--active', 'presence')
        except:
            raise VkErrorDoingTask('Error liking post')

    def execute_task(self, type: str):
        self.check_18box()
        
        if type == 'Follow page':
            self.follow_page()
        elif type == 'Follow user':
            self.follow_user()
        elif type == 'Join group':
            self.join_group()
        elif type == 'Liking post':
            self.like_post()
        elif type == 'Liking photo':
            self.like_photo()
        else:
            raise VkErrorInvalidTaskType('')

        sleep(1)

if __name__ == '__main__':
    pass
