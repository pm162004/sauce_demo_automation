def pytest_collection_modify_items(session, config, items):
    """Modifies test items in place to ensure test classes run in a given order."""
    CLASS_ORDER = [
        "TestLogin",
        # "TestProductBrowsing",
        # "TestSauceAddToCart",
        # "TestUpdateToCart",
        # "TestCheckoutFlow",
        # "TestSauceLogout",
    ]
    class_mapping = {item: item.cls.__name__ for item in items}
    sorted_items = items.copy()
    # Iteratively move tests of each class to the end of the test queue
    for class_ in CLASS_ORDER:
        sorted_items = [it for it in sorted_items if class_mapping[it] != class_] + [
            it for it in sorted_items if class_mapping[it] == class_
        ]
    items[:] = sorted_items
