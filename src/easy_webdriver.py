import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FindElementFunctionInvalidParams(Exception):
    pass


class FindElementsFunctionInvalidParams(Exception):
    pass


def find_element(driver, element_type: str, name: str, mode='clickable', wait=10):
    '''Try to find a element in a webdriver or inside a element:
        Types available: id, class, css, xpath and name
        Modes available: clickable, presence'''

    element_type = element_type.lower()
    name = name.replace(' ', '.')

    if mode == 'clickable':
        if element_type == 'id':
            return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((
                By.ID, name
            )))
        elif element_type == 'class':
            return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((
                By.CLASS_NAME, name
            )))
        elif element_type == 'css':
            return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, name
            )))
        elif element_type == 'xpath':
            return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((
                By.CLASS_NAME, name
            )))
        elif element_type == 'name':
            return WebDriverWait(driver, wait).until(EC.element_to_be_clickable((
                By.NAME, name
            )))
        else:
            raise FindElementFunctionInvalidParams()
    elif mode == 'presence':
        if element_type == 'id':
            return WebDriverWait(driver, wait).until(EC.presence_of_element_located((
                By.ID, name
            )))
        elif element_type == 'class':
            return WebDriverWait(driver, wait).until(EC.presence_of_element_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'css':
            return WebDriverWait(driver, wait).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, name
            )))
        elif element_type == 'xpath':
            return WebDriverWait(driver, wait).until(EC.presence_of_element_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'name':
            return WebDriverWait(driver, wait).until(EC.presence_of_element_located((
                By.NAME, name
            )))
        else:
            raise FindElementFunctionInvalidParams()
    else: raise FindElementFunctionInvalidParams()

def find_elements(driver, element_type: str, name: str, mode='visibility', wait=10):
    '''Try to find a element in a webdriver or inside a element:
    Types available: id, class, css, xpath and name
    Modes available: visibility, presence'''

    element_type = element_type.lower()
    name = name.replace(' ', '.')
    
    if mode == 'presence':
        if element_type == 'id':
            return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((
                By.ID, name
            )))
        elif element_type == 'class':
            return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'css':
            return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, name
            )))
        elif element_type == 'xpath':
            return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'name':
            return WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((
                By.NAME, name
            )))
        else:
            raise FindElementsFunctionInvalidParams()
    elif mode == 'visibility':
        if element_type == 'id':
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((
                By.ID, name
            )))
        elif element_type == 'class':
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'css':
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((
                By.CSS_SELECTOR, name
            )))
        elif element_type == 'xpath':
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((
                By.CLASS_NAME, name
            )))
        elif element_type == 'name':
            return WebDriverWait(driver, wait).until(EC.visibility_of_all_elements_located((
                By.NAME, name
            )))
        else:
            raise FindElementsFunctionInvalidParams()
    else: raise FindElementsFunctionInvalidParams()