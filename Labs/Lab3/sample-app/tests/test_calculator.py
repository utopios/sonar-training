"""
Unit tests for the Calculator class.

This module contains comprehensive tests for all calculator operations.
"""

import pytest
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture to create a Calculator instance for tests."""
    return Calculator()


class TestAddition:
    """Tests for the addition operation."""

    def test_add_positive_numbers(self, calculator):
        """Test adding two positive numbers."""
        result = calculator.add(5, 3)
        assert result == 8.0

    def test_add_negative_numbers(self, calculator):
        """Test adding two negative numbers."""
        result = calculator.add(-5, -3)
        assert result == -8.0

    def test_add_mixed_signs(self, calculator):
        """Test adding positive and negative numbers."""
        result = calculator.add(5, -3)
        assert result == 2.0

    def test_add_zero(self, calculator):
        """Test adding zero."""
        result = calculator.add(5, 0)
        assert result == 5.0

    def test_add_floats(self, calculator):
        """Test adding floating point numbers."""
        result = calculator.add(2.5, 3.5)
        assert result == 6.0


class TestSubtraction:
    """Tests for the subtraction operation."""

    def test_subtract_positive_numbers(self, calculator):
        """Test subtracting positive numbers."""
        result = calculator.subtract(10, 3)
        assert result == 7.0

    def test_subtract_negative_numbers(self, calculator):
        """Test subtracting negative numbers."""
        result = calculator.subtract(-5, -3)
        assert result == -2.0

    def test_subtract_to_zero(self, calculator):
        """Test subtraction resulting in zero."""
        result = calculator.subtract(5, 5)
        assert result == 0.0

    def test_subtract_resulting_negative(self, calculator):
        """Test subtraction resulting in negative number."""
        result = calculator.subtract(3, 10)
        assert result == -7.0


class TestMultiplication:
    """Tests for the multiplication operation."""

    def test_multiply_positive_numbers(self, calculator):
        """Test multiplying positive numbers."""
        result = calculator.multiply(4, 5)
        assert result == 20.0

    def test_multiply_negative_numbers(self, calculator):
        """Test multiplying negative numbers."""
        result = calculator.multiply(-4, -5)
        assert result == 20.0

    def test_multiply_mixed_signs(self, calculator):
        """Test multiplying mixed sign numbers."""
        result = calculator.multiply(4, -5)
        assert result == -20.0

    def test_multiply_by_zero(self, calculator):
        """Test multiplying by zero."""
        result = calculator.multiply(5, 0)
        assert result == 0.0

    def test_multiply_floats(self, calculator):
        """Test multiplying floating point numbers."""
        result = calculator.multiply(2.5, 4)
        assert result == 10.0


class TestDivision:
    """Tests for the division operation."""

    def test_divide_positive_numbers(self, calculator):
        """Test dividing positive numbers."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_negative_numbers(self, calculator):
        """Test dividing negative numbers."""
        result = calculator.divide(-10, -2)
        assert result == 5.0

    def test_divide_mixed_signs(self, calculator):
        """Test dividing mixed sign numbers."""
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_divide_by_zero(self, calculator):
        """Test division by zero raises error."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_zero(self, calculator):
        """Test dividing zero."""
        result = calculator.divide(0, 5)
        assert result == 0.0

    def test_divide_floats(self, calculator):
        """Test dividing floating point numbers."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0


class TestPower:
    """Tests for the power operation."""

    def test_power_positive_exponent(self, calculator):
        """Test raising to positive power."""
        result = calculator.power(2, 3)
        assert result == 8.0

    def test_power_zero_exponent(self, calculator):
        """Test raising to power of zero."""
        result = calculator.power(5, 0)
        assert result == 1.0

    def test_power_negative_exponent(self, calculator):
        """Test raising to negative power."""
        result = calculator.power(2, -2)
        assert result == 0.25

    def test_power_fractional_exponent(self, calculator):
        """Test raising to fractional power."""
        result = calculator.power(4, 0.5)
        assert result == 2.0


class TestSquareRoot:
    """Tests for the square root operation."""

    def test_square_root_perfect_square(self, calculator):
        """Test square root of perfect square."""
        result = calculator.square_root(16)
        assert result == 4.0

    def test_square_root_zero(self, calculator):
        """Test square root of zero."""
        result = calculator.square_root(0)
        assert result == 0.0

    def test_square_root_non_perfect_square(self, calculator):
        """Test square root of non-perfect square."""
        result = calculator.square_root(2)
        assert abs(result - 1.414) < 0.001

    def test_square_root_negative_number(self, calculator):
        """Test square root of negative number raises error."""
        with pytest.raises(ValueError):
            calculator.square_root(-4)


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_very_large_numbers(self, calculator):
        """Test operations with very large numbers."""
        result = calculator.add(1e10, 1e10)
        assert result == 2e10

    def test_very_small_numbers(self, calculator):
        """Test operations with very small numbers."""
        result = calculator.add(1e-10, 1e-10)
        assert abs(result - 2e-10) < 1e-15

    def test_precision(self, calculator):
        """Test floating point precision."""
        result = calculator.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10
