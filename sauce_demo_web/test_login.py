import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert, error,input_field
from log_config import setup_logger




logger = setup_logger()



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

# Elements
def username_input():
    return wait.until(EC.presence_of_element_located((By.ID, "user-name")))

def password_input():
    return wait.until(EC.presence_of_element_located((By.ID, "password")))

def login_btn():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))


def check_blank_username():
    username_variable = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[normalize-space()='Epic sadface: Username is required']")))
    return username_variable

def check_lockout_username():
    username_variable = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Epic sadface: Sorry, this user has been locked out')]")))
    return username_variable

def check_blank_password():
    password_variable = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[normalize-space()='Epic sadface: Password is required']")))
    return password_variable

def check_invalid_creds():
    creds_variable = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Epic sadface: Username and password do not match any user in this service')]")))
    return creds_variable

def inventory_title():
    return wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

def logout_menu():
    return wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))

def logout_link():
    return wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))

def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()

# Test Cases
class TestSauceLogin:

    def test_blank_username(self):
        login_btn().click()
        assert check_blank_username().text == validation_assert.ENTER_USERNAME

    def test_blank_password(self):
        refresh_page()
        username_input().send_keys(user_name)
        login_btn().click()
        assert check_blank_password().text == validation_assert.ENTER_PASSWORD
        driver.save_screenshot( f"/home/web-h-028/PycharmProjects/sauce_demo_automation/screenshorts/blank_creds.png")
        logger.info("input blank username and check the error message is displayed.")


    def test_invalid_username(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(password)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        driver.save_screenshot( f"/home/web-h-028/PycharmProjects/sauce_demo_automation/screenshorts/invalid_username.png")
        logger.info("Enter invalid username check the error message is displayed.")

    def test_locked_out_username(self):
        refresh_page()
        username_input().send_keys(input_field.LOCKED_OUT_USER)
        password_input().send_keys(password)
        login_btn().click()
        assert check_lockout_username().text == error.LOCKED_OUT_USER_ERROR_MESSAGE
        driver.save_screenshot( f"/home/web-h-028/PycharmProjects/sauce_demo_automation/screenshorts/locked_username.png")
        logger.info("Enter locked out username and check the error message is displayed.")

    def test_invalid_password(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        driver.save_screenshot( f"/home/web-h-028/PycharmProjects/sauce_demo_automation/screenshorts/invalid_password.png")
        logger.info("Enter invalid password and check the error message is displayed.")
        driver.refresh()

    def test_invalid_username_password(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        driver.save_screenshot(f"/home/web-h-028/PycharmProjects/sauce_demo_automation/screenshorts/invalid_username_password.png")
        logger.info("Enter invalid username and password and check the error message is displayed.")
        driver.refresh()

    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.products
        logger.info("User logged in successfully")

    def test_logout(self):
        refresh_page()
        logout_menu().click()
        time.sleep(1)
        logout_link().click()
        assert login_btn().is_displayed()
        logger.info("Log out is successfully")