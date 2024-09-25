import pytest
from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError


def test_assert_auth_raises_fyle_error():
    """Test assert_auth raises FyleError when condition is False."""
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False)
    assert exc_info.value.status_code == 401
    assert str(exc_info.value) == "UNAUTHORIZED"


def test_assert_auth_passes():
    """Test assert_auth does not raise an error when condition is True."""
    try:
        assert_auth(True)
    except FyleError:
        pytest.fail("assert_auth raised FyleError unexpectedly!")


def test_assert_true_raises_fyle_error():
    """Test assert_true raises FyleError when condition is False."""
    with pytest.raises(FyleError) as exc_info:
        assert_true(False)
    assert exc_info.value.status_code == 403
    assert str(exc_info.value) == "FORBIDDEN"


def test_assert_true_passes():
    """Test assert_true does not raise an error when condition is True."""
    try:
        assert_true(True)
    except FyleError:
        pytest.fail("assert_true raised FyleError unexpectedly!")


def test_assert_valid_raises_fyle_error():
    """Test assert_valid raises FyleError when condition is False."""
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False)
    assert exc_info.value.status_code == 400
    assert str(exc_info.value) == "BAD_REQUEST"


def test_assert_valid_passes():
    """Test assert_valid does not raise an error when condition is True."""
    try:
        assert_valid(True)
    except FyleError:
        pytest.fail("assert_valid raised FyleError unexpectedly!")


def test_assert_found_raises_fyle_error():
    """Test assert_found raises FyleError when object is None."""
    with pytest.raises(FyleError) as exc_info:
        assert_found(None)
    assert exc_info.value.status_code == 404
    assert str(exc_info.value) == "NOT_FOUND"


def test_assert_found_passes():
    """Test assert_found does not raise an error when object is not None."""
    try:
        assert_found("some_object")
    except FyleError:
        pytest.fail("assert_found raised FyleError unexpectedly!")
