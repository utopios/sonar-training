"""
Calculator module providing basic arithmetic operations.

This module contains a Calculator class with methods for
addition, subtraction, multiplication, and division.
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The sum of a and b

        Example:
            >>> calc = Calculator()
            >>> calc.add(2, 3)
            5.0
        """
        return float(a + b)

    def subtract(self, a: float, b: float) -> float:
        """
        Subtract b from a.

        Args:
            a: Number to subtract from
            b: Number to subtract

        Returns:
            The difference of a and b

        Example:
            >>> calc = Calculator()
            >>> calc.subtract(5, 3)
            2.0
        """
        return float(a - b)

    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The product of a and b

        Example:
            >>> calc = Calculator()
            >>> calc.multiply(4, 5)
            20.0
        """
        return float(a * b)

    def divide(self, a: float, b: float) -> float:
        """
        Divide a by b.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            The quotient of a and b

        Raises:
            ZeroDivisionError: If b is zero

        Example:
            >>> calc = Calculator()
            >>> calc.divide(10, 2)
            5.0
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return float(a / b)

    def power(self, base: float, exponent: float) -> float:
        """
        Raise base to the power of exponent.

        Args:
            base: The base number
            exponent: The exponent

        Returns:
            base raised to the power of exponent

        Example:
            >>> calc = Calculator()
            >>> calc.power(2, 3)
            8.0
        """
        return float(base ** exponent)

    def square_root(self, number: float) -> float:
        """
        Calculate the square root of a number.

        Args:
            number: The number to calculate square root of

        Returns:
            The square root of the number

        Raises:
            ValueError: If number is negative

        Example:
            >>> calc = Calculator()
            >>> calc.square_root(16)
            4.0
        """
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return float(number ** 0.5)
