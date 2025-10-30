"""
Utility functions for the application.

This module provides helper functions used across the application.
"""


def validate_number(value) -> bool:
    """
    Validate if a value can be converted to a number.

    Args:
        value: The value to validate

    Returns:
        True if value is a valid number, False otherwise

    Example:
        >>> validate_number(42)
        True
        >>> validate_number("3.14")
        True
        >>> validate_number("abc")
        False
    """
    if value is None:
        return False

    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def format_result(operation: str, a: float, b: float, result: float) -> dict:
    """
    Format calculation result as a dictionary.

    Args:
        operation: The operation performed
        a: First operand
        b: Second operand
        result: The calculation result

    Returns:
        Dictionary containing operation details

    Example:
        >>> format_result("addition", 2, 3, 5)
        {'operation': 'addition', 'a': 2, 'b': 3, 'result': 5}
    """
    return {
        'operation': operation,
        'a': a,
        'b': b,
        'result': result
    }


def is_positive(number: float) -> bool:
    """
    Check if a number is positive.

    Args:
        number: The number to check

    Returns:
        True if number is positive, False otherwise

    Example:
        >>> is_positive(5)
        True
        >>> is_positive(-3)
        False
    """
    return number > 0


def is_negative(number: float) -> bool:
    """
    Check if a number is negative.

    Args:
        number: The number to check

    Returns:
        True if number is negative, False otherwise

    Example:
        >>> is_negative(-5)
        True
        >>> is_negative(3)
        False
    """
    return number < 0


def is_even(number: int) -> bool:
    """
    Check if a number is even.

    Args:
        number: The number to check

    Returns:
        True if number is even, False otherwise

    Example:
        >>> is_even(4)
        True
        >>> is_even(5)
        False
    """
    return number % 2 == 0


def is_odd(number: int) -> bool:
    """
    Check if a number is odd.

    Args:
        number: The number to check

    Returns:
        True if number is odd, False otherwise

    Example:
        >>> is_odd(5)
        True
        >>> is_odd(4)
        False
    """
    return number % 2 != 0
