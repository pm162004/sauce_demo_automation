import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sauce_demo_setup.config import config
from constant import validation_assert
from log_config import setup_logger




# Setup driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()
driver.get(config.WEB_URL)

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

logger = setup_logger()

@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user", "secret_sauce"),
        ("locked_out_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
    ],
)
def test_login_multiple_users(username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    assert "Products" == validation_assert.PRODUCTS
    logger.info("User logged in successfully in data driven")
