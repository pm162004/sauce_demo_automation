import csv
import pytest
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

# user_name = config.USER_NAME
# password = config.PASSWORD

def get_login_data():
    with open('/home/web-h-028/PycharmProjects/sauce_demo_automation/test_login_csv.py') as file:
        return [tuple(row.values()) for row in csv.DictReader(file)]

@pytest.mark.parametrize("username,password", get_login_data())
def test_login_csv(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    assert "Products" == validation_assert.products
    logger.info("User logged in successfully in data driven")
