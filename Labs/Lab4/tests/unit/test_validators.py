"""Unit tests for validator utilities."""

import pytest
from src.app.utils.validators import (
    validate_email,
    validate_username,
    validate_password_strength,
    validate_phone_number,
    validate_url,
    sanitize_input,
    is_positive_integer,
    is_non_negative_number
)


class TestValidators:
    """Test suite for validator functions."""

    def test_validate_email_valid(self):
        """Test validating valid email addresses."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@example.co.uk") is True
        assert validate_email("user+tag@example.com") is True

    def test_validate_email_invalid(self):
        """Test validating invalid email addresses."""
        assert validate_email("invalid") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("") is False
        assert validate_email(None) is False

    def test_validate_username_valid(self):
        """Test validating valid usernames."""
        assert validate_username("john_doe") is True
        assert validate_username("user123") is True
        assert validate_username("test-user") is True

    def test_validate_username_invalid_short(self):
        """Test validating short username."""
        assert validate_username("ab") is False

    def test_validate_username_invalid_long(self):
        """Test validating long username."""
        assert validate_username("a" * 51) is False

    def test_validate_username_invalid_characters(self):
        """Test validating username with invalid characters."""
        assert validate_username("user@name") is False
        assert validate_username("user name") is False
        assert validate_username("") is False
        assert validate_username(None) is False

    def test_validate_password_strength_valid(self):
        """Test validating strong password."""
        is_valid, message = validate_password_strength("MyPass123!")
        assert is_valid is True
        assert "strong" in message.lower()

    def test_validate_password_strength_too_short(self):
        """Test password too short."""
        is_valid, message = validate_password_strength("Pass1!")
        assert is_valid is False
        assert "at least 8 characters" in message

    def test_validate_password_strength_no_uppercase(self):
        """Test password without uppercase."""
        is_valid, message = validate_password_strength("mypass123!")
        assert is_valid is False
        assert "uppercase" in message

    def test_validate_password_strength_no_lowercase(self):
        """Test password without lowercase."""
        is_valid, message = validate_password_strength("MYPASS123!")
        assert is_valid is False
        assert "lowercase" in message

    def test_validate_password_strength_no_digit(self):
        """Test password without digit."""
        is_valid, message = validate_password_strength("MyPassword!")
        assert is_valid is False
        assert "digit" in message

    def test_validate_password_strength_no_special(self):
        """Test password without special character."""
        is_valid, message = validate_password_strength("MyPassword123")
        assert is_valid is False
        assert "special character" in message

    def test_validate_password_strength_too_long(self):
        """Test password too long."""
        is_valid, message = validate_password_strength("MyPass123!" * 20)
        assert is_valid is False
        assert "too long" in message

    def test_validate_phone_number_valid(self):
        """Test validating valid phone numbers."""
        assert validate_phone_number("+1234567890") is True
        assert validate_phone_number("+12 345 678 9012") is True
        assert validate_phone_number("1234567890") is True

    def test_validate_phone_number_invalid(self):
        """Test validating invalid phone numbers."""
        assert validate_phone_number("123") is False
        assert validate_phone_number("abc") is False
        assert validate_phone_number("") is False
        assert validate_phone_number(None) is False

    def test_validate_url_valid(self):
        """Test validating valid URLs."""
        assert validate_url("http://example.com") is True
        assert validate_url("https://example.com/path") is True
        assert validate_url("https://example.com/path?query=value") is True

    def test_validate_url_invalid(self):
        """Test validating invalid URLs."""
        assert validate_url("not-a-url") is False
        assert validate_url("ftp://example.com") is False
        assert validate_url("") is False
        assert validate_url(None) is False

    def test_sanitize_input_valid(self):
        """Test sanitizing valid input."""
        result = sanitize_input("Hello World")
        assert result == "Hello World"

    def test_sanitize_input_removes_control_chars(self):
        """Test sanitizing input with control characters."""
        result = sanitize_input("Hello\x00World\x1F")
        assert result == "HelloWorld"

    def test_sanitize_input_trims_length(self):
        """Test sanitizing input trims to max length."""
        long_text = "a" * 2000
        result = sanitize_input(long_text, max_length=100)
        assert len(result) == 100

    def test_sanitize_input_empty_or_none(self):
        """Test sanitizing empty or None input."""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""
        assert sanitize_input(123) == ""

    def test_is_positive_integer_valid(self):
        """Test checking positive integers."""
        assert is_positive_integer(1) is True
        assert is_positive_integer(100) is True
        assert is_positive_integer("5") is True

    def test_is_positive_integer_invalid(self):
        """Test checking invalid positive integers."""
        assert is_positive_integer(0) is False
        assert is_positive_integer(-1) is False
        assert is_positive_integer(1.5) is False
        assert is_positive_integer("abc") is False
        assert is_positive_integer(None) is False
        assert is_positive_integer(True) is False

    def test_is_non_negative_number_valid(self):
        """Test checking non-negative numbers."""
        assert is_non_negative_number(0) is True
        assert is_non_negative_number(1) is True
        assert is_non_negative_number(1.5) is True
        assert is_non_negative_number("5.5") is True

    def test_is_non_negative_number_invalid(self):
        """Test checking invalid non-negative numbers."""
        assert is_non_negative_number(-1) is False
        assert is_non_negative_number(-0.1) is False
        assert is_non_negative_number("abc") is False
        assert is_non_negative_number(None) is False
