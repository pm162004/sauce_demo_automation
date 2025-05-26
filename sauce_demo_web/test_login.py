import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sauce_demo_setup.config import config
from constant import validation_assert, error, input_field
from log_config import setup_logger
import os
import datetime



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False

}


chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

chrome_options.add_argument("--headless") # Optional for headless mode

driver.maximize_window()
driver.get(config.WEB_URL)


wait = WebDriverWait(driver, 25)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD

logger = setup_logger()

def save_screenshot(filename, use_timestamp=True, folder="screenshorts"):
    os.makedirs(folder, exist_ok=True)

    if use_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "{}_{}.png".format(filename, timestamp)
    else:
        filename = "{}.png".format(filename)

    full_path = folder, filename
    driver.save_screenshot(f"{folder}/{filename}")  # using global driver
    return full_path

def username_input():
    return wait.until(EC.presence_of_element_located((By.ID, "user-name")))


def password_input():
    return wait.until(EC.presence_of_element_located((By.ID, "password")))


def login_btn():
    return wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']"))
    )


def check_blank_username():
    username_variable = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[normalize-space()='Epic sadface: Username is required']")
        )
    )
    return username_variable


def check_lockout_username():
    username_variable = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//h3[contains(text(),'Epic sadface: Sorry, this user has been locked out')]",
            )
        )
    )
    return username_variable


def check_blank_password():
    password_variable = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[normalize-space()='Epic sadface: Password is required']")
        )
    )
    return password_variable


def check_invalid_creds():
    creds_variable = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//h3[contains(text(),'Epic sadface: Username and password do not match any user in this service')]",
            )
        )
    )
    return creds_variable


def inventory_title():
    return wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))


def logout_menu():
    return wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='bm-burger-button']"))
    )


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
class TestLogin:

    def test_blank_username(self):
        login_btn().click()
        assert check_blank_username().text == validation_assert.ENTER_USERNAME
        save_screenshot("blank_username")
        logger.error("input blank username and check the error message is displayed.")

    def test_blank_password(self):
        refresh_page()
        username_input().send_keys(user_name)
        login_btn().click()
        assert check_blank_password().text == validation_assert.ENTER_PASSWORD
        save_screenshot("blank_password")
        logger.error("input blank password and check the error message is displayed.")

    def test_invalid_username(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(password)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_username")
        logger.error("Enter invalid username check the error message is displayed.")

    def test_locked_out_username(self):
        refresh_page()
        username_input().send_keys(input_field.LOCKED_OUT_USER)
        password_input().send_keys(password)
        login_btn().click()
        assert check_lockout_username().text == error.LOCKED_OUT_USER_ERROR_MESSAGE
        save_screenshot("locked_username")
        logger.error(
            "Enter locked out username and check the error message is displayed."
        )

    def test_invalid_password(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_password")
        logger.info("Enter invalid password and check the error message is displayed.")
        driver.refresh()

    def test_invalid_username_password(self):
        refresh_page()
        username_input().send_keys(input_field.INVALID_USERNAME)
        password_input().send_keys(input_field.INVALID_PASSWORD)
        login_btn().click()
        assert check_invalid_creds().text == error.INVALID_CREDS_ERROR_MESSAGE
        save_screenshot("invalid_username_password")
        logger.error(
            "Enter invalid username and password and check the error message is displayed."
        )
        driver.refresh()

    def test_valid_login_flow(self):
        refresh_page()
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.PRODUCTS
        logger.info("User logged in successfully")

    def test_logout(self):
        logout_menu().click()
        logout_link()
        logger.info("User Logout in successfully")
        quit_browser()
