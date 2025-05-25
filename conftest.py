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
        return getattr(item, 'cls', None).__name__ if hasattr(item, 'cls') else ""

    sorted_items = []
    for class_name in class_order:
        sorted_items.extend([item for item in items if get_class_name(item) == class_name])

    remaining = [item for item in items if item not in sorted_items]
    items[:] = sorted_items + remaining
