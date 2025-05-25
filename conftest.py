def pytest_collection_modifyitems(session, config, items):
    class_order = [
        "TestLogin",
        "TestProductBrowsing",
        "TestSauceAddToCart",
        "TestUpdateToCart",
        "TestCheckoutFlow",
        "TestSauceLogout"
    ]

    def get_class_name(item):
        cls = getattr(item, 'cls', None)
        return cls.__name__ if cls else ""

    filtered_items = []
    for class_name in class_order:
        filtered_items.extend([item for item in items if get_class_name(item) == class_name])

    # Only include tests from specified classes
    items[:] = filtered_items
