import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from easy_webdriver import *

from vk import *
from gen_log import GenLog
from settings import Settings
from getlike import *

class ErrorMakeReady(Exception):pass


import os

def inicia_chromedriver(headless = False, user_data_dir = None) -> uc.Chrome: 
    options = uc.ChromeOptions()
    if headless: options.add_argument('--headless')
    driver = uc.Chrome(user_data_dir=user_data_dir, options=options)
    return driver
    

class RPBot:
    def __init__(self):
        self.root_path = os.path.realpath(__file__ + '/../../')
        print(self.root_path)
        self.settings = Settings(self.root_path + '/config/config.json')
        self.log = GenLog(self.root_path + '/log/tasks.log', self.root_path + '/log/profiles.log')
        self.log.log_message('Starting bot')
        
    
    def __inicia_driver__(self, headless = False, user_data_dir = None) -> uc.Chrome:
        self.log.log_message('Opening chromedriver')
        options = uc.ChromeOptions()
        if headless: options.add_argument('--headless')
        driver = uc.Chrome(user_data_dir=user_data_dir, options=options)
        return driver
    
    def make_ready(self, getlike:GetLike, vk:Vk, profile:dict):
        if getlike.login_status and vk.login_status: return
        else:
            if vk.login_status == False:
                vk.credencial_login(profile['email'], profile['pass'])
            if getlike.login_status == False:
                getlike.insert_cookies(self.root_path + '/config/cookies.txt')
                if getlike.check_login() == False:
                    getlike.credential_login(self.settings.getlike_account['email'], self.settings.getlike_account['pass'])
                    getlike.export_cookies(self.root_path + '/config/cookies.txt')
            
        if getlike.login_status and vk.login_status: return
        else: raise ErrorMakeReady('Erro ao logar no getlike e/ou vk')
            
    def rape_profile(self, profile:dict): 
        success_tasks = 0
        hided_tasks = 0
        earned = 0
        
        driver = self.__inicia_driver__(headless = False, user_data_dir=(self.root_path + '/profiles/' + profile['id'].lower()))
        getlike = GetLike(driver)
        vk = Vk(driver)
        
        self.make_ready(getlike, vk, profile)
            
        getlike.switch_profile(profile['id'])
        
        try:
            while True:
                try:
                    tasks = getlike.found_tasks()
                except:
                    break
                
                for task in tasks:
                    if(task['type'] in self.settings.allowed_tasks):
                        result = getlike.execute_task(task, vk)
                        
                        if result.status == 'Success': 
                            success_tasks+=1
                            earned+=result.value
                        else:
                            hided_tasks+=1
                        
                        self.log.log_task(result)
                    else:
                        result = getlike.hide_task(task)
                        hided_tasks+=1
                        self.log.log_task(result)
        except:
            self.log.log_message('\nOcorreu um erro ao rapear esse perfil, passando pro próximo\n')
            
                    
        profile_log = ResultProfile(profile['id'], earned, success_tasks, hided_tasks)
        self.log.log_profile(profile_log)
        driver.quit()

    def execute(self):
        for profile in self.settings.vk_accounts:
            self.log.log_message(f'Going to rape: {profile["id"]}')
            self.rape_profile(profile)          
        

if __name__ == '__main__':
    bot = RPBot()
    bot.execute()
