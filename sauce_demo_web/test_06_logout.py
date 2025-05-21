# import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert, error,input_field
import log_config

# def setup_logger():
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)
#     fh = logging.FileHandler('logs/test_log.log')
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)
#     return logger
#
# logger = setup_logger()

# Setup driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Optional for headless mode
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(config.WEB_URL)

# driver.implicitly_wait(10)
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD

from log_config import setup_logger




logger = setup_logger()



# Elements
def username_input():
    return wait.until(EC.presence_of_element_located((By.ID, "user-name")))

def password_input():
    return wait.until(EC.presence_of_element_located((By.ID, "password")))

def login_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))



def inventory_title():
    return wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

def logout_menu():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='bm-burger-button']")))

def logout_link():
    time.sleep(1)
    logout_element = driver.find_element(By.ID, "logout_sidebar_link")
    return driver.execute_script("arguments[0].click();", logout_element)

def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()

def quit_browser():
    time.sleep(1)
    return driver.quit()
# Test Cases
class TestSauceLogOUT:


    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.products
        logger.info("User logged in successfully")

    def test_logout(self):
        logout_menu().click()
        logout_link()
        logger.info("User Logout in successfully")
        quit_browser()





