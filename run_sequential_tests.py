import pytest

file_order = [
    "sauce_demo_web/test_login.py",
    "sauce_demo_web/test_product_browsing.py",
    "sauce_demo_web/test_add_to_cart.py",
    "sauce_demo_web/test_update_to_cart.py",
    "sauce_demo_web/test_checkout_flow.py",
    "sauce_demo_web/test_logout.py"
]

for test_file in file_order:
    print("Running: {}".format(test_file))
    exit_code = pytest.main([test_file])

    if exit_code != 0:
        print("Test failed in: {}. Stopping further execution.".format(test_file))
        break
else:
    print("All test files executed successfully.")
