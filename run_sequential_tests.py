
import pytest
import time

file_order = [
    "sauce_demo_web/test_01_login.py",
    "sauce_demo_web/test_02_product_browsing.py",
    "sauce_demo_web/test_03_add_to_cart.py",
    "sauce_demo_web/test_04_update_to_cart.py",
    "sauce_demo_web/test_05_checkout_flow.py",
    "sauce_demo_web/test_06_logout.py",
]

for test_file in file_order:

    print(f" Running: {test_file}")
    exit_code = pytest.main([test_file])

    if exit_code != 0:
        print(f" Test failed in: {test_file}. Stopping further execution.")
        break
else:
    print(" All test files executed successfully.")
