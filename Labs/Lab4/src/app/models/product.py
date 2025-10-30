"""Product model for e-commerce application."""

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Product:
    """Product entity with business logic."""

    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    is_available: bool = True

    def __post_init__(self):
        """Validate product data."""
        self.validate_price()
        self.validate_stock()
        self.validate_name()

    def validate_name(self) -> None:
        """
        Validate product name.

        Raises:
            ValueError: If name is invalid.
        """
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Product name cannot be empty")

        if len(self.name) > 200:
            raise ValueError("Product name is too long (max 200 characters)")

    def validate_price(self) -> None:
        """
        Validate product price.

        Raises:
            ValueError: If price is invalid.
        """
        if self.price < 0:
            raise ValueError("Price cannot be negative")

        if self.price > 1000000:
            raise ValueError("Price exceeds maximum allowed value")

    def validate_stock(self) -> None:
        """
        Validate stock quantity.

        Raises:
            ValueError: If stock is invalid.
        """
        if self.stock < 0:
            raise ValueError("Stock cannot be negative")

    def is_in_stock(self) -> bool:
        """
        Check if product is in stock.

        Returns:
            bool: True if stock > 0, False otherwise.
        """
        return self.stock > 0 and self.is_available

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce stock by specified quantity.

        Args:
            quantity: Amount to reduce from stock.

        Raises:
            ValueError: If quantity is invalid or insufficient stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > self.stock:
            raise ValueError(f"Insufficient stock. Available: {self.stock}, Requested: {quantity}")

        self.stock -= quantity

        if self.stock == 0:
            self.is_available = False

    def add_stock(self, quantity: int) -> None:
        """
        Add stock by specified quantity.

        Args:
            quantity: Amount to add to stock.

        Raises:
            ValueError: If quantity is invalid.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.stock += quantity

        if self.stock > 0:
            self.is_available = True

    def apply_discount(self, discount_percent: float) -> Decimal:
        """
        Calculate discounted price.

        Args:
            discount_percent: Discount percentage (0-100).

        Returns:
            Decimal: Discounted price.

        Raises:
            ValueError: If discount is invalid.
        """
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")

        discount_amount = self.price * Decimal(discount_percent / 100)
        return self.price - discount_amount

    def to_dict(self) -> dict:
        """
        Convert product to dictionary.

        Returns:
            dict: Product data as dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "category": self.category,
            "is_available": self.is_available
        }
