from datetime import datetime

from categories import VALID_CATEGORIES
from exceptions import UnauthorizedError


def validate_user(event) -> str:
    """
    Validates the presence of a user ID in the request.

    Args:
        event (dict): The Lambda event payload.

    Returns:
        str: The user ID.

    Raises:
        UnauthorizedError: If the user ID is not present.
    """
    user_id = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("claims", {})
        .get("sub")
    )
    if not user_id:
        raise UnauthorizedError()
    return user_id


def validate_expense_payload(data: dict[str, str | int | float]) -> None:
    """
    Validates the input data for creating and updating an expense.

    Args:
        data: The input dictionary containing expense details.

    Raises:
        ValueError: If any field is invalid.
    """

    required_fields = ["merchantName", "categoryId", "amount", "date"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate categoryId
    if data["categoryId"] not in VALID_CATEGORIES:
        raise ValueError(f"Invalid categoryId: {data['categoryId']}")

    # Validate amount
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        raise ValueError("Amount must be a positive non-zero number.")

    # Validate date
    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
