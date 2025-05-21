import os
import logging
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from log_config import setup_logger

# Initialize logger
logger = setup_logger()




# ---------- Test Ordering ----------
def pytest_collection_modify_items(session, config, items):
    # Define the desired file order
    file_order = [
        "test_01_login.py",
        "test_02_product_browsing.py",
        "test_03_add_to_cart.py",
        "test_04_update_to_cart.py",
        "test_05_checkout_flow.py",
        "test_06_logout.py",
    ]


    def file_index(item):
        for idx, filename in enumerate(file_order):
            if filename in item.nodeid:
                return idx
        return len(file_order)


# ---------- HTML Reporting ----------
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    config.option.htmlpath = report_path
    config.option.self_contained_html = True

    logger.info(f"HTML report will be saved to: {report_path}")

