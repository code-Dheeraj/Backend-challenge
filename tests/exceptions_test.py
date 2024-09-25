import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    """Test the initialization of the FyleError class."""
    error_message = "This is a test error"
    error_code = 404
    error = FyleError(status_code=error_code, message=error_message)

    assert error.message == error_message
    assert error.status_code == error_code

def test_fyle_error_to_dict():
    """Test the to_dict method of FyleError."""
    error_message = "This is a test error"
    error = FyleError(status_code=400, message=error_message)

    assert error.to_dict() == {'message': error_message}

def test_fyle_error_default_status_code():
    """Test default status code when not provided."""
    error_message = "Default status error"
    error = FyleError(status_code=400, message=error_message)

    assert error.status_code == 400  # Ensure default status code is used
