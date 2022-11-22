'''IMPORTS'''
import undetected_chromedriver as uc
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from easy_webdriver import *


from vk import *
from time import sleep
from random import randint


# Exceções

class GetLikeErrorLoginException(Exception):
    pass

class GetLikeErrorImportBalance(Exception):
    pass

class GetLikeErrorSwitchProfile(Exception):
    pass

class GetLikeErrorSwitchTab(Exception):
    pass

class GetLikeTaskWithError(Exception):
    pass

class GetLikeErrorCheckTask(Exception):pass
class GetLikeErrorHideTask(Exception):pass

'''CONSTS'''
TIME_WAIT = 10

'''CLASSES'''


class ResultTask:
    def __init__(self, id:str, status:str, value:float, task_type:str, profile_name:str) -> None:
        self.id = id
        self.status = status
        self.value = value
        self.task_type = task_type
        self.profile_name = profile_name

class ResultProfile:
    def __init__(self, id :str, earned:float, success_tasks:int, hided_tasks:int) -> None:
        self.id = id
        self.earned = earned
        self.success_tasks = success_tasks
        self.hided_tasks = hided_tasks



class GetLike:
    def __init__(self, driver: uc.Chrome):
        self.driver = driver
        self.login_status = self.check_login()
        if self.login_status:
            self.current_profile = self.get_current_profile()

    # Login methods
    def insert_cookies(self, cookies_path):
        '''Insert cookies in the driver'''
        self.driver.get('https://getlike.io/')
        sleep(3)

        with open(cookies_path, 'r') as cookies_file:
            cookies_list = eval(str(cookies_file.read()))

        for cookie in cookies_list:
            self.driver.add_cookie(cookie)

    def export_cookies(self, cookies_path):
        '''Export cookies to the file'''
        self.driver.get('https://getlike.io/')
        sleep(3)

        with open(cookies_path, 'w') as cookies_file:
            cookies_file.write(str(self.driver.get_cookies()))

    def check_login(self):
        self.driver.get('https://getlike.io/en/tasks/vkontakte/all/')
        sleep(2)
        if self.driver.current_url == 'https://getlike.io/en/tasks/vkontakte/all/':
            self.login_status = True
            return True
        else:
            self.login_status = False
            return False

    def credential_login(self, email: str, password: str):
        '''Login with email and password'''
        self.driver.get('https://getlike.io/login/')
        sleep(3)

        #Send email
        find_element(self.driver, 'id', 'User_loginLogin', 'clickable', TIME_WAIT).send_keys(email)
        sleep(2)

        #Send password
        find_element(self.driver, 'id', 'User_passwordLogin', 'clickable', TIME_WAIT).send_keys(password)
        sleep(2)

        for i in range(1, 5):
            print('WARNING -> RECAPTCHA')
            sleep(5)

        #Click in login
        find_element(self.driver, 'css', 'input[class="btn btn-primary btn-block btn-lg"]', 'clickable', TIME_WAIT).click()
        sleep(4)

        if (self.check_login() == False):
            raise GetLikeErrorLoginException(
                'Erro ao logar na conta por meio de credenciais')

    def import_balance(self):
        self.driver.get('https://getlike.io/en/tasks/')
        try:
            saldo = find_element(self.driver, 'id', 'user_money_balance', 'presence').text
            return float(saldo)
        except:
            raise GetLikeErrorImportBalance('Erro ao importar saldo, brother')

    def get_current_profile(self):
        '''Get current profile'''

        self.driver.get('https://getlike.io/en/tasks/vkontakte/all/')
        sleep(2)

        # Make sure the current profile is what we want
        current_profile = find_element(self.driver, 'class', 'media-info-name.text-capitalize.text-overflow', 'presence')
        self.current_profile = current_profile.get_dom_attribute('title')
        return self.current_profile

    def switch_profile(self, profile_link: str):
        '''Try to switch the profile to the profile with profile_link inside'''

        self.driver.get('https://getlike.io/en/tasks/vkontakte/all/')
        sleep(3)

        if profile_link.split('.com/')[1] == self.get_current_profile():
            return

        # Click switch button
        try:
            #Click in switch
            find_element(self.driver, 'class', 'media-info-type.text-inverse.text-overflow').click()
        except:
            #Try to click again
            find_element(self.driver, 'class', 'link.media-middle.media-right.text-right').click()

        sleep(2)

        # Get profiles
        profiles = WebDriverWait(self.driver, TIME_WAIT).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, 'media-info-name.text-overflow.visible-xs'
        )))

        # Find profile
        for profile_element in profiles:
            if profile_link == profile_element.get_dom_attribute('title').split()[0]:
                break
        else:
            raise GetLikeErrorSwitchProfile('Perfil não encontrado')

        # Click on founded profile
        click = WebDriverWait(self.driver, TIME_WAIT).until(
            EC.element_to_be_clickable(profile_element)).click()

        # Agree the alert
        alert = WebDriverWait(self.driver, TIME_WAIT).until(
            EC.alert_is_present()).accept()

        sleep(2)
        perfil_atual = self.get_current_profile()
        if profile_link.split('.com/')[1] == perfil_atual:
            return
        else:
            raise GetLikeErrorSwitchProfile(
                'Deu ruim na hora de trocar o perfil')

    def found_tasks(self):
        '''Found and return the tasks in getlike current profile'''

        self.driver.get("https://getlike.io/en/tasks/vkontakte/all/")
        sleep(3)

        # Found all tasks in getlike profile
        tasks = WebDriverWait(self.driver, TIME_WAIT).until(EC.presence_of_all_elements_located((
            By.CLASS_NAME, 'panel-group.task_item'
        )))

        # Add all the tasks and respectibe types and values in a list
        tasks_info = list()
        for task in tasks:
            tasks_info.append({'task': task, 
                               'id': task.get_attribute('id').split('-')[2], 
                               'type': task.text.split('\n')[0], 
                               'value': float(task.text.split('\n')[1])})

        return tasks_info

    def switch_to_vktab(self, parent_window):
        def tabs(): return self.driver.window_handles

        try:
            vk_tab = tabs()[-1]
        except:
            raise GetLikeErrorSwitchTab('')

        sleep(2)

        if (parent_window == vk_tab):
            raise GetLikeErrorSwitchTab('')

        # Troca de guia
        self.driver.switch_to.window(vk_tab)

        for i in range(0, 3):
            if 'vk.com' in self.driver.current_url:
                return
            else:
                sleep(5)
        else:
            raise GetLikeTaskWithError(
                'Erro ao tentar mudar de aba, tarefa com erro')

    def switch_to_getlike(self, parent_window):
        tabs = self.driver.window_handles

        for tab in tabs:
            if (tab != parent_window):
                self.driver.switch_to.window(tab)
                self.driver.close()
                self.driver.switch_to.window(parent_window)

    def hide_task(self, task) ->ResultTask:

        try:
            # Clica nos tres pontos
            WebDriverWait(task['task'], 5).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'button[class="btn btn-muted-light btn-link_bg btn-sm dropdown-toggle dropdown-toggle_no-caret"]'
            ))).click()

            # Clica em hide
            WebDriverWait(task['task'], 5).until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, f'a[href="javascript:;"]'
                )))[3].click()
            
            result = ResultTask(task['id'], 'Hided', task['value'], task['type'], self.current_profile)
            return result
        except:
            raise GetLikeErrorHideTask('Erro ao esconder a tarefa')

    def check_task(self, task):
        # Wait for auto check
        try:
            WebDriverWait(task, 5).until(EC.presence_of_element_located((
                By.CLASS_NAME, 'label.label-success.text-uppercase'
            )))
            return 'Success'
        except:
            try:
                WebDriverWait(task, 5).until(EC.presence_of_element_located((
                    By.CLASS_NAME, 'do.btn.btn-sm.btn-primary.btn-block.btn-success.check-task'
                ))).click()
                WebDriverWait(task, 5).until(EC.presence_of_element_located((
                    By.CLASS_NAME, 'label.label-success.text-uppercase'
                )))
                return 'Success'
            except:
                self.hide_task(task)
                return 'ErrorCheckTask'

    def execute_task(self, task: dict, vk: Vk):
        task_element = task['task']

        # Click task
        WebDriverWait(task_element, TIME_WAIT).until(EC.presence_of_element_located((
            By.CLASS_NAME, 'do.do-task.btn.btn-sm.btn-primary.btn-block'
        ))).click()

        parent_window = self.driver.current_window_handle

        try:
            self.switch_to_vktab(parent_window)
            vk.execute_task(task['type'])
            sleep(2)
            self.switch_to_getlike(parent_window)
            status = self.check_task(task_element)
        except GetLikeTaskWithError:
            self.switch_to_getlike(parent_window)
            status = 'InvalidTask'
        except VkErrorInvalidTaskType:
            self.switch_to_getlike(parent_window)
            status = 'InvalidTaskType'
        except VkErrorDoingTask:
            self.switch_to_getlike(parent_window)
            raise VkErrorDoingTask
        except NoSuchWindowException:
            return ResultTask(task['id'], 'Stopped', task['value'], task['type'], self.current_profile)
            
        self.switch_to_getlike(parent_window)
        
        result = ResultTask(task['id'], status, task['value'], task['type'], self.current_profile)
        return result
        




if __name__ == '__main__':
    pass
