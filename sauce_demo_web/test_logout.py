import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sauce_demo_setup.config import config
from constant import validation_assert
from log_config import setup_logger

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

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD



logger = setup_logger()


# Elements
def username_input():
    return wait.until(EC.presence_of_element_located((By.ID, "user-name")))


def password_input():
    return wait.until(EC.presence_of_element_located((By.ID, "password")))


def login_btn():
    return wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']"))
    )


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
class TestSauceLogout:
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
