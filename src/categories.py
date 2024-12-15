VALID_CATEGORIES = {
    1: "Advertising",
    2: "Benefits",
    3: "Car",
    4: "Equipment",
    5: "Fees",
    6: "Home Office",
    7: "Insurance",
    8: "Interest",
    9: "Labor",
    10: "Maintenance",
    11: "Materials",
    12: "Meals and Entertainment",
    13: "Office Supplies",
    14: "Other",
    15: "Professional Services",
    16: "Rent",
    17: "Taxes",
    18: "Travel",
    19: "Utilities",
}


def map_category_id_to_name(category_id: int) -> str:
    """
    Maps a valid category ID to the corresponding category name.

    Args:
        category_id: The category ID.

    Returns:
        str: The mapped category name.

    Raises:
        ValueError: If the category ID is invalid.
    """
    if category_id in VALID_CATEGORIES:
        return VALID_CATEGORIES[category_id]
    raise ValueError(f"Invalid categoryId: {category_id}")
