
def pytest_collection_modify_items(session, config, items):
    order = [
        "test_blank_username",
        "test_blank_password",
        "test_invalid_username",
        "test_locked_out_username",
        "test_invalid_password",
        "test_invalid_username_password",
        "test_valid_login_flow",
        "test_logout"
    ]
    item_dict = {item.name: item for item in items}
    ordered_items = [item_dict[name] for name in order if name in item_dict]
    # Add remaining tests at the end if any
    rest = [item for item in items if item not in ordered_items]
    items[:] = ordered_items + rest
