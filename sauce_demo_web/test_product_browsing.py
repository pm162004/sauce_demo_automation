import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert
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

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

user_name = config.USER_NAME
password = config.PASSWORD
from log_config import setup_logger

logger = setup_logger()


def take_debug_screenshot(name="debug"):
    os.makedirs("screenshorts", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join("../screenshorts", f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"[DEBUG] Screenshot saved: {path}")

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


def check_product_selection():
    element = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@data-test='inventory-item-name' and text()='Sauce Labs Bike Light']")))
    return element

def check_product_details():
    return wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_details_name"))
    )


def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()


def quit_browser():
    time.sleep(1)
    return driver.quit()


# Test Cases
class TestProductBrowsing:
    def test_valid_login_flow(self):
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.PRODUCTS
        logger.info("User logged in successfully")

    def test_product_browsing_and_view_details(self):
        refresh_page()
        try:
            element = check_product_selection()
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
            assert check_product_details().is_displayed()
            logger.info("User product browsing in successfully")
        except Exception as e:
            take_debug_screenshot("product_browsing_failed")
            logger.error("Product browsing failed: {}".format(e))
            raise
