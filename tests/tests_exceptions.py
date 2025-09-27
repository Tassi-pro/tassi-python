import pytest
from tassi.exceptions import (
    TassiException,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
)


class TestTassiExceptions:
    """Tests pour les exceptions personnalisées."""

    def test_tassi_exception_inheritance(self):
        """Test que TassiException hérite de Exception."""
        exception = TassiException("Test message")
        assert isinstance(exception, Exception)
        assert str(exception) == "Test message"

    def test_authentication_error_inheritance(self):
        """Test que AuthenticationError hérite de TassiException."""
        exception = AuthenticationError("Auth failed")
        assert isinstance(exception, TassiException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Auth failed"

    def test_validation_error_inheritance(self):
        """Test que ValidationError hérite de TassiException."""
        exception = ValidationError("Validation failed")
        assert isinstance(exception, TassiException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Validation failed"

    def test_not_found_error_inheritance(self):
        """Test que NotFoundError hérite de TassiException."""
        exception = NotFoundError("Resource not found")
        assert isinstance(exception, TassiException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Resource not found"

    def test_rate_limit_error_inheritance(self):
        """Test que RateLimitError hérite de TassiException."""
        exception = RateLimitError("Rate limit exceeded")
        assert isinstance(exception, TassiException)
        assert isinstance(exception, Exception)
        assert str(exception) == "Rate limit exceeded"

    def test_exception_with_no_message(self):
        """Test des exceptions sans message."""
        exception = TassiException()
        assert str(exception) == ""

    def test_exception_raising(self):
        """Test que les exceptions peuvent être levées correctement."""
        with pytest.raises(TassiException) as exc_info:
            raise TassiException("Test error")
        assert str(exc_info.value) == "Test error"

        with pytest.raises(AuthenticationError) as exc_info:
            raise AuthenticationError("Auth error")
        assert str(exc_info.value) == "Auth error"

        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Validation error")
        assert str(exc_info.value) == "Validation error"

        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError("Not found error")
        assert str(exc_info.value) == "Not found error"

        with pytest.raises(RateLimitError) as exc_info:
            raise RateLimitError("Rate limit error")
        assert str(exc_info.value) == "Rate limit error"
