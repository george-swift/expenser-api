from src.utils.exceptions import UnauthorizedError

def test_unauthorized_error_default_message():
    """Test that UnauthorizedError has the default message."""
    error = UnauthorizedError()
    assert str(error) == "Unauthorized"

def test_unauthorized_error_custom_message():
    """Test that UnauthorizedError can accept a custom message."""
    custom_message = "Custom unauthorized message"
    error = UnauthorizedError(message=custom_message)
    assert str(error) == custom_message