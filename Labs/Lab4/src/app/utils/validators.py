"""Validation utility functions."""

import re
from typing import Any


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """
    Validate username format.

    Args:
        username: Username to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not username or not isinstance(username, str):
        return False

    if len(username) < 3 or len(username) > 50:
        return False

    return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Args:
        password: Password to validate.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password is too long (max 128 characters)"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format (international format).

    Args:
        phone: Phone number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not phone or not isinstance(phone, str):
        return False

    # Remove common separators
    cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    # Check international format
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, cleaned))


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False

    pattern = r'^https?://[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+$'
    return bool(re.match(pattern, url))


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input by removing potentially dangerous characters.

    Args:
        text: Text to sanitize.
        max_length: Maximum allowed length.

    Returns:
        str: Sanitized text.
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove control characters
    sanitized = ''.join(char for char in text if char.isprintable() or char.isspace())

    # Trim to max length
    return sanitized[:max_length].strip()


def is_positive_integer(value: Any) -> bool:
    """
    Check if value is a positive integer.

    Args:
        value: Value to check.

    Returns:
        bool: True if positive integer, False otherwise.
    """
    if isinstance(value, bool):
        return False

    try:
        int_value = int(value)
        return int_value > 0 and int_value == float(value)
    except (ValueError, TypeError):
        return False


def is_non_negative_number(value: Any) -> bool:
    """
    Check if value is a non-negative number.

    Args:
        value: Value to check.

    Returns:
        bool: True if non-negative number, False otherwise.
    """
    try:
        float_value = float(value)
        return float_value >= 0
    except (ValueError, TypeError):
        return False
