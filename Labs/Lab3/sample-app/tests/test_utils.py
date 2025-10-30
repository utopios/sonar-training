"""
Unit tests for utility functions.

This module contains tests for all utility functions.
"""

import pytest
from src.utils import (
    validate_number,
    format_result,
    is_positive,
    is_negative,
    is_even,
    is_odd
)


class TestValidateNumber:
    """Tests for the validate_number function."""

    def test_validate_integer(self):
        """Test validating an integer."""
        assert validate_number(42) is True

    def test_validate_float(self):
        """Test validating a float."""
        assert validate_number(3.14) is True

    def test_validate_string_number(self):
        """Test validating a string that represents a number."""
        assert validate_number("123") is True
        assert validate_number("45.67") is True

    def test_validate_invalid_string(self):
        """Test validating an invalid string."""
        assert validate_number("abc") is False
        assert validate_number("12.34.56") is False

    def test_validate_none(self):
        """Test validating None."""
        assert validate_number(None) is False

    def test_validate_empty_string(self):
        """Test validating empty string."""
        assert validate_number("") is False

    def test_validate_negative_number(self):
        """Test validating negative numbers."""
        assert validate_number(-42) is True
        assert validate_number("-3.14") is True

    def test_validate_zero(self):
        """Test validating zero."""
        assert validate_number(0) is True
        assert validate_number("0") is True


class TestFormatResult:
    """Tests for the format_result function."""

    def test_format_addition(self):
        """Test formatting addition result."""
        result = format_result("addition", 2, 3, 5)
        assert result == {
            'operation': 'addition',
            'a': 2,
            'b': 3,
            'result': 5
        }

    def test_format_subtraction(self):
        """Test formatting subtraction result."""
        result = format_result("subtraction", 10, 3, 7)
        assert result['operation'] == 'subtraction'
        assert result['result'] == 7

    def test_format_with_floats(self):
        """Test formatting with floating point numbers."""
        result = format_result("division", 10.5, 2.5, 4.2)
        assert result['a'] == 10.5
        assert result['b'] == 2.5
        assert result['result'] == 4.2

    def test_format_with_negative_result(self):
        """Test formatting with negative result."""
        result = format_result("subtraction", 3, 10, -7)
        assert result['result'] == -7


class TestIsPositive:
    """Tests for the is_positive function."""

    def test_positive_number(self):
        """Test with positive number."""
        assert is_positive(5) is True
        assert is_positive(0.1) is True

    def test_negative_number(self):
        """Test with negative number."""
        assert is_positive(-5) is False
        assert is_positive(-0.1) is False

    def test_zero(self):
        """Test with zero."""
        assert is_positive(0) is False


class TestIsNegative:
    """Tests for the is_negative function."""

    def test_negative_number(self):
        """Test with negative number."""
        assert is_negative(-5) is True
        assert is_negative(-0.1) is True

    def test_positive_number(self):
        """Test with positive number."""
        assert is_negative(5) is False
        assert is_negative(0.1) is False

    def test_zero(self):
        """Test with zero."""
        assert is_negative(0) is False


class TestIsEven:
    """Tests for the is_even function."""

    def test_even_positive(self):
        """Test with even positive numbers."""
        assert is_even(2) is True
        assert is_even(4) is True
        assert is_even(100) is True

    def test_odd_positive(self):
        """Test with odd positive numbers."""
        assert is_even(1) is False
        assert is_even(3) is False
        assert is_even(99) is False

    def test_even_negative(self):
        """Test with even negative numbers."""
        assert is_even(-2) is True
        assert is_even(-4) is True

    def test_odd_negative(self):
        """Test with odd negative numbers."""
        assert is_even(-1) is False
        assert is_even(-3) is False

    def test_zero(self):
        """Test with zero."""
        assert is_even(0) is True


class TestIsOdd:
    """Tests for the is_odd function."""

    def test_odd_positive(self):
        """Test with odd positive numbers."""
        assert is_odd(1) is True
        assert is_odd(3) is True
        assert is_odd(99) is True

    def test_even_positive(self):
        """Test with even positive numbers."""
        assert is_odd(2) is False
        assert is_odd(4) is False
        assert is_odd(100) is False

    def test_odd_negative(self):
        """Test with odd negative numbers."""
        assert is_odd(-1) is True
        assert is_odd(-3) is True

    def test_even_negative(self):
        """Test with even negative numbers."""
        assert is_odd(-2) is False
        assert is_odd(-4) is False

    def test_zero(self):
        """Test with zero."""
        assert is_odd(0) is False
