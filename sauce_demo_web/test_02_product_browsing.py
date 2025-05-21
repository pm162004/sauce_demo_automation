# import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert, error, input_field

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


def check_product_selection():
    return wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "inventory_item_name")))


def check_product_details():
    return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_details_name")))


def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()


def quit_browser():
    time.sleep(1)
    return driver.quit()


# Test Cases
class TestSauceLogin:
    def test_valid_login_flow(self):
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.products
        logger.info("User logged in successfully")

    def test_product_browsing_and_view_details(self):
        # refresh_page()
        check_product_selection().click()
        assert check_product_details().is_displayed()
        logger.info("User product browsing in successfully")
        quit_browser()
