# import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from sauce_demo_setup.config import config
from constant import validation_assert, error, input_field
from log_config import setup_logger

logger = setup_logger()

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


def update_cart():
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    return cart_items


def remove_cart_item():
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart_button"))).click()


def checkout_cart_item():
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()


def first_name_error():
    return wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Error: First Name is required']")))


def last_name_error():
    return wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Error: Last Name is required']")))


def postal_code_error():
    return wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Error: Postal Code is required']")))


def first_name_input():
    return wait.until(EC.presence_of_element_located((By.ID, "first-name")))


def last_name_input():
    return wait.until(EC.presence_of_element_located((By.ID, "last-name")))


def postal_code_input():
    return wait.until(EC.presence_of_element_located((By.ID, "postal-code")))


def continue_btn():
    return wait.until(EC.element_to_be_clickable((By.ID, "continue")))


def summary_info():
    return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_info")))


def finish_btn():
    return wait.until(EC.element_to_be_clickable((By.ID, "finish")))


def success_message():
    return wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))


def quit_browser():
    time.sleep(1)
    return driver.quit()


class Test1:
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
        wait.until(EC.url_contains("cart"))
        assert "cart" in driver.current_url
        assert check_cart_item().is_displayed()
        logger.info("User view the cart successfully")

    def test_checkout_process(self):
        refresh_page()
        checkout_cart_item()

    def test_checkout_blank_first_name(self):
        # refresh_page()
        continue_btn().click()
        assert first_name_error().text == validation_assert.ENTER_FIRST_NAME

    def test_checkout_blank_last_name(self):
        refresh_page()
        first_name_input().send_keys(input_field.FIRST_NAME)
        continue_btn().click()

        assert last_name_error().text == validation_assert.ENTER_LAST_NAME

    def test_checkout_blank_postal_code(self):
        refresh_page()
        first_name_input().send_keys(input_field.FIRST_NAME)
        last_name_input().send_keys(input_field.LAST_NAME)
        continue_btn().click()

        assert postal_code_error().text == validation_assert.ENTER_POSTAL_CODE

    def test_checkout_process_positive_flow(self):
        refresh_page()
        # checkout_cart_item()
        first_name_input().send_keys(input_field.FIRST_NAME)
        last_name_input().send_keys(input_field.LAST_NAME)
        postal_code_input().send_keys(input_field.POSTAL_CODE)
        continue_btn().click()
        summary = summary_info()
        assert summary.is_displayed()
        finish_btn().click()
        success_msg = success_message()
        assert success_msg.text == validation_assert.THANK_YOU
        logger.info("User check out the cart successfully")
        quit_browser()
