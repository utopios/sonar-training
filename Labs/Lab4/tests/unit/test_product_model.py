"""Unit tests for Product model."""

import pytest
from decimal import Decimal
from src.app.models.product import Product


class TestProductModel:
    """Test suite for Product model."""

    def test_create_valid_product(self):
        """Test creating a valid product."""
        product = Product(
            id=1,
            name="Laptop",
            description="High-performance laptop",
            price=Decimal("999.99"),
            stock=10,
            category="Electronics"
        )

        assert product.id == 1
        assert product.name == "Laptop"
        assert product.price == Decimal("999.99")
        assert product.stock == 10
        assert product.is_available is True

    def test_invalid_negative_price(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product(
                id=1,
                name="Test",
                description="Test product",
                price=Decimal("-10.00"),
                stock=5,
                category="Test"
            )

    def test_invalid_excessive_price(self):
        """Test that excessive price raises ValueError."""
        with pytest.raises(ValueError, match="exceeds maximum"):
            Product(
                id=1,
                name="Test",
                description="Test product",
                price=Decimal("2000000"),
                stock=5,
                category="Test"
            )

    def test_invalid_negative_stock(self):
        """Test that negative stock raises ValueError."""
        with pytest.raises(ValueError, match="Stock cannot be negative"):
            Product(
                id=1,
                name="Test",
                description="Test product",
                price=Decimal("10.00"),
                stock=-5,
                category="Test"
            )

    def test_invalid_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Product(
                id=1,
                name="",
                description="Test product",
                price=Decimal("10.00"),
                stock=5,
                category="Test"
            )

    def test_invalid_long_name(self):
        """Test that long name raises ValueError."""
        with pytest.raises(ValueError, match="name is too long"):
            Product(
                id=1,
                name="a" * 201,
                description="Test product",
                price=Decimal("10.00"),
                stock=5,
                category="Test"
            )

    def test_is_in_stock_returns_true(self):
        """Test is_in_stock returns True when stock > 0."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        assert product.is_in_stock() is True

    def test_is_in_stock_returns_false_when_zero_stock(self):
        """Test is_in_stock returns False when stock is 0."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=0,
            category="Test"
        )

        assert product.is_in_stock() is False

    def test_is_in_stock_returns_false_when_unavailable(self):
        """Test is_in_stock returns False when product is unavailable."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test",
            is_available=False
        )

        assert product.is_in_stock() is False

    def test_reduce_stock_success(self):
        """Test reducing stock successfully."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=10,
            category="Test"
        )

        product.reduce_stock(3)
        assert product.stock == 7
        assert product.is_available is True

    def test_reduce_stock_to_zero(self):
        """Test reducing stock to zero marks product unavailable."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        product.reduce_stock(5)
        assert product.stock == 0
        assert product.is_available is False

    def test_reduce_stock_insufficient_raises_error(self):
        """Test reducing stock with insufficient quantity raises error."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        with pytest.raises(ValueError, match="Insufficient stock"):
            product.reduce_stock(10)

    def test_reduce_stock_invalid_quantity_raises_error(self):
        """Test reducing stock with invalid quantity raises error."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=10,
            category="Test"
        )

        with pytest.raises(ValueError, match="Quantity must be positive"):
            product.reduce_stock(0)

    def test_add_stock_success(self):
        """Test adding stock successfully."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        product.add_stock(10)
        assert product.stock == 15
        assert product.is_available is True

    def test_add_stock_makes_product_available(self):
        """Test adding stock makes unavailable product available."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=0,
            category="Test",
            is_available=False
        )

        product.add_stock(5)
        assert product.stock == 5
        assert product.is_available is True

    def test_add_stock_invalid_quantity_raises_error(self):
        """Test adding invalid quantity raises error."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        with pytest.raises(ValueError, match="Quantity must be positive"):
            product.add_stock(-5)

    def test_apply_discount_valid(self):
        """Test applying valid discount."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("100.00"),
            stock=5,
            category="Test"
        )

        discounted_price = product.apply_discount(20)
        assert discounted_price == Decimal("80.00")

    def test_apply_discount_invalid_negative(self):
        """Test applying negative discount raises error."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("100.00"),
            stock=5,
            category="Test"
        )

        with pytest.raises(ValueError, match="between 0 and 100"):
            product.apply_discount(-10)

    def test_apply_discount_invalid_over_100(self):
        """Test applying discount over 100 raises error."""
        product = Product(
            id=1,
            name="Test",
            description="Test product",
            price=Decimal("100.00"),
            stock=5,
            category="Test"
        )

        with pytest.raises(ValueError, match="between 0 and 100"):
            product.apply_discount(150)

    def test_to_dict(self):
        """Test converting product to dictionary."""
        product = Product(
            id=1,
            name="Laptop",
            description="High-performance laptop",
            price=Decimal("999.99"),
            stock=10,
            category="Electronics"
        )

        product_dict = product.to_dict()

        assert product_dict["id"] == 1
        assert product_dict["name"] == "Laptop"
        assert product_dict["description"] == "High-performance laptop"
        assert product_dict["price"] == 999.99
        assert product_dict["stock"] == 10
        assert product_dict["category"] == "Electronics"
        assert product_dict["is_available"] is True
