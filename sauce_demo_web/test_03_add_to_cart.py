# import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert, error, input_field

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Optional for headless mode
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(config.WEB_URL)

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
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='item_4_title_link' and @data-test='item-4-title-link']")))
    return element

def check_product_details():
    return wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='inventory_details_name large_size']")))




def check_add_to_cart():
    return wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='add-to-cart']")))


def refresh_page():
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    return driver.refresh()


def check_the_cart():
    cart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-test='shopping-cart-link']")))
    return cart_icon


def check_cart_item():
    return wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))


def quit_browser():
    time.sleep(1)
    return driver.quit()


class TestSauceLogin:
    def test_valid_login_flow(self):
        username_input().send_keys(user_name)
        password_input().send_keys(password)
        login_btn().click()
        assert inventory_title().text == validation_assert.products
        logger.info("User logged in successfully")

    def test_product_browsing_and_view_details(self):
        refresh_page()
        element = check_product_selection()
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        assert check_product_details().is_displayed()
        logger.info("User product browsing in successfully")

    def test_add_to_cart(self):
        refresh_page()
        check_add_to_cart().click()
        logger.info("User add the cart successfully")

    def test_view_cart(self):
        refresh_page()
        check_the_cart().click()

        assert "cart" in driver.current_url
        assert check_cart_item().is_displayed()
        logger.info("User view the cart successfully")
        quit_browser()
