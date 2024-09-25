# tests/server_test.py
import pytest
from flask import Flask
from core.server import app, handle_error
from core.libs.exceptions import FyleError
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_handle_fyle_error(client):
    """Test that FyleError is handled correctly."""
    with app.app_context():
        error = FyleError(status_code=400, message='Test Fyle Error')
        response = handle_error(error)  # Call the updated function
        
        assert response[1] == 400
        assert response[0].json['error'] == 'FyleError'
        assert response[0].json['message'] == 'Test Fyle Error'

def test_handle_validation_error(client):
    """Test that ValidationError is handled correctly."""
    with app.app_context():
        error = ValidationError("This field is required.", field_name='field')
        response = handle_error(error)  # Call the updated function

        assert response[1] == 400
        assert response[0].json['error'] == 'ValidationError'
        assert response[0].json['message'] == {'field': ['This field is required.']}  # Check for dictionary


def test_handle_integrity_error(client):
    """Test that IntegrityError is handled correctly."""
    with app.app_context():
        error = IntegrityError("Unique constraint failed", orig=None, params=None)      
        response = handle_error(error)  # Call the updated function

        assert response[1] == 400
        assert response[0].json['error'] == 'IntegrityError'
        assert 'Integrity error occurred' in response[0].json['message']  # Expect default message



from werkzeug.exceptions import NotFound

def test_handle_http_exception(client):
    """Test that HTTPException is handled correctly."""
    with app.app_context():
        class MockHTTPException(NotFound):
            code = 404

            def __str__(self):
                return 'Not Found'

        error = MockHTTPException()
        response = handle_error(error)  # Call the updated function
        
        assert response[1] == 404
        assert response[0].json['error'] == 'MockHTTPException'
        assert response[0].json['message'] == 'Not Found'


def test_handle_generic_exception(client):
    """Test that generic exceptions are raised."""
    with pytest.raises(Exception):
        handle_error(Exception("Generic error"))
