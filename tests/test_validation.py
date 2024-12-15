import pytest

from src.validation import validate_expense_payload, validate_user


def test_validate_user_valid():
    event = {"requestContext": {"authorizer": {"claims": {"sub": "user123"}}}}
    assert validate_user(event) == "user123"


def test_validate_expense_payload_valid():
    data = {
        "merchantName": "Test Merchant",
        "categoryId": 8,
        "amount": 10.0,
        "date": "2023-10-01",
    }
    validate_expense_payload(data)  # Should not raise an error


def test_validate_expense_payload_missing_field():
    data = {
        "merchantName": "Test Merchant",
        "amount": 10.0,
        "date": "2023-10-01",
    }
    with pytest.raises(ValueError, match="Missing required field: categoryId"):
        validate_expense_payload(data)


def test_validate_expense_payload_invalid_category():
    data = {
        "merchantName": "Test Merchant",
        "categoryId": "invalid_category",
        "amount": 10.0,
        "date": "2023-10-01",
    }
    with pytest.raises(
        ValueError, match=f"Invalid categoryId: {data['categoryId']}"
    ):
        validate_expense_payload(data)


def test_validate_expense_payload_invalid_amount():
    data = {
        "merchantName": "Test Merchant",
        "categoryId": 9,
        "amount": -5,
        "date": "2023-10-01",
    }
    with pytest.raises(
        ValueError, match="Amount must be a positive non-zero number."
    ):
        validate_expense_payload(data)


def test_validate_expense_payload_invalid_date():
    data = {
        "merchantName": "Test Merchant",
        "categoryId": 6,
        "amount": 10.0,
        "date": "invalid_date",
    }
    with pytest.raises(
        ValueError, match="Invalid date format. Use YYYY-MM-DD."
    ):
        validate_expense_payload(data)
