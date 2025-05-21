import pytest

file_order = [
    "test_01_login.py",
    "test_02_product_browsing.py",
    "test_03_add_to_cart.py",
    "test_04_update_to_cart.py",
    "test_05_checkout_flow.py",
    "test_06_logout.py",
]

for test_file in file_order:
    print(f" Running: {test_file}")
    exit_code = pytest.main([test_file])

    if exit_code != 0:
        print(f" Test failed in: {test_file}. Stopping further execution.")
        break
else:
    print(" All test files executed successfully.")
