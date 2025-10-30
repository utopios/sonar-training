"""Unit tests for ProductService."""

import pytest
from decimal import Decimal
from src.app.services.product_service import ProductService
from src.app.models.product import Product


class TestProductService:
    """Test suite for ProductService class."""

    @pytest.fixture
    def service(self):
        """Create a fresh ProductService instance for each test."""
        return ProductService()

    @pytest.fixture
    def sample_product_data(self):
        """Sample product data for testing."""
        return {
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": Decimal("999.99"),
            "stock": 10,
            "category": "Electronics"
        }

    def test_create_product_success(self, service, sample_product_data):
        """Test creating a product successfully."""
        product = service.create_product(**sample_product_data)

        assert product is not None
        assert product.id == 1
        assert product.name == "Laptop"
        assert product.price == Decimal("999.99")
        assert product.stock == 10
        assert product.category == "Electronics"

    def test_create_multiple_products_increments_id(self, service, sample_product_data):
        """Test that product IDs increment correctly."""
        product1 = service.create_product(**sample_product_data)
        product2 = service.create_product(**sample_product_data)
        product3 = service.create_product(**sample_product_data)

        assert product1.id == 1
        assert product2.id == 2
        assert product3.id == 3

    def test_create_product_with_invalid_data_raises_error(self, service):
        """Test creating product with invalid data raises ValueError."""
        with pytest.raises(ValueError):
            service.create_product(
                name="",
                description="Test",
                price=Decimal("10.00"),
                stock=5,
                category="Test"
            )

    def test_get_product_exists(self, service, sample_product_data):
        """Test getting an existing product."""
        created = service.create_product(**sample_product_data)
        retrieved = service.get_product(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name

    def test_get_product_not_exists(self, service):
        """Test getting a non-existent product returns None."""
        result = service.get_product(999)
        assert result is None

    def test_get_all_products_empty(self, service):
        """Test getting all products when service is empty."""
        products = service.get_all_products()
        assert products == []

    def test_get_all_products_with_data(self, service, sample_product_data):
        """Test getting all products with data."""
        service.create_product(**sample_product_data)
        service.create_product(
            name="Mouse",
            description="Wireless mouse",
            price=Decimal("29.99"),
            stock=50,
            category="Electronics"
        )

        products = service.get_all_products()
        assert len(products) == 2

    def test_get_available_products(self, service):
        """Test getting only available products."""
        # Create available product
        service.create_product(
            name="Product1",
            description="Available",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )

        # Create unavailable product
        product2 = service.create_product(
            name="Product2",
            description="Unavailable",
            price=Decimal("20.00"),
            stock=0,
            category="Test"
        )

        available = service.get_available_products()
        assert len(available) == 1
        assert available[0].name == "Product1"

    def test_get_products_by_category(self, service):
        """Test getting products by category."""
        service.create_product(
            name="Laptop",
            description="Test",
            price=Decimal("999.99"),
            stock=10,
            category="Electronics"
        )
        service.create_product(
            name="Book",
            description="Test",
            price=Decimal("19.99"),
            stock=100,
            category="Books"
        )
        service.create_product(
            name="Mouse",
            description="Test",
            price=Decimal("29.99"),
            stock=50,
            category="Electronics"
        )

        electronics = service.get_products_by_category("Electronics")
        assert len(electronics) == 2
        assert all(p.category == "Electronics" for p in electronics)

    def test_get_products_by_category_empty(self, service):
        """Test getting products from non-existent category."""
        result = service.get_products_by_category("NonExistent")
        assert result == []

    def test_search_products_by_name(self, service):
        """Test searching products by name."""
        service.create_product(
            name="Gaming Laptop",
            description="High-end gaming laptop",
            price=Decimal("1999.99"),
            stock=5,
            category="Electronics"
        )
        service.create_product(
            name="Office Laptop",
            description="Business laptop",
            price=Decimal("899.99"),
            stock=10,
            category="Electronics"
        )

        results = service.search_products("Gaming")
        assert len(results) == 1
        assert "Gaming" in results[0].name

    def test_search_products_by_description(self, service):
        """Test searching products by description."""
        service.create_product(
            name="Product A",
            description="Ultra powerful device",
            price=Decimal("999.99"),
            stock=10,
            category="Test"
        )
        service.create_product(
            name="Product B",
            description="Basic device",
            price=Decimal("99.99"),
            stock=20,
            category="Test"
        )

        results = service.search_products("powerful")
        assert len(results) == 1
        assert "powerful" in results[0].description

    def test_search_products_case_insensitive(self, service):
        """Test that search is case insensitive."""
        service.create_product(
            name="Laptop",
            description="Test",
            price=Decimal("999.99"),
            stock=10,
            category="Electronics"
        )

        results = service.search_products("LAPTOP")
        assert len(results) == 1

    def test_search_products_no_results(self, service):
        """Test searching with no matching results."""
        service.create_product(
            name="Laptop",
            description="Test",
            price=Decimal("999.99"),
            stock=10,
            category="Electronics"
        )

        results = service.search_products("xyz")
        assert results == []

    def test_update_product_success(self, service, sample_product_data):
        """Test updating product successfully."""
        product = service.create_product(**sample_product_data)
        updated = service.update_product(product.id, name="Updated Laptop", price=Decimal("1099.99"))

        assert updated is not None
        assert updated.name == "Updated Laptop"
        assert updated.price == Decimal("1099.99")

    def test_update_product_not_found(self, service):
        """Test updating non-existent product."""
        result = service.update_product(999, name="Test")
        assert result is None

    def test_update_product_invalid_data_raises_error(self, service, sample_product_data):
        """Test updating product with invalid data raises error."""
        product = service.create_product(**sample_product_data)

        with pytest.raises(ValueError):
            service.update_product(product.id, name="")

    def test_update_product_ignores_invalid_fields(self, service, sample_product_data):
        """Test that update ignores fields not in allowed list."""
        product = service.create_product(**sample_product_data)
        original_id = product.id

        service.update_product(product.id, id=999, invalid_field="test")

        # ID should not change
        assert product.id == original_id

    def test_delete_product_success(self, service, sample_product_data):
        """Test deleting product successfully."""
        product = service.create_product(**sample_product_data)
        result = service.delete_product(product.id)

        assert result is True
        assert service.get_product(product.id) is None

    def test_delete_product_not_found(self, service):
        """Test deleting non-existent product."""
        result = service.delete_product(999)
        assert result is False

    def test_add_stock_success(self, service, sample_product_data):
        """Test adding stock successfully."""
        product = service.create_product(**sample_product_data)
        original_stock = product.stock

        result = service.add_stock(product.id, 5)

        assert result is True
        assert product.stock == original_stock + 5

    def test_add_stock_product_not_found(self, service):
        """Test adding stock to non-existent product."""
        result = service.add_stock(999, 5)
        assert result is False

    def test_add_stock_invalid_quantity_raises_error(self, service, sample_product_data):
        """Test adding invalid stock quantity raises error."""
        product = service.create_product(**sample_product_data)

        with pytest.raises(ValueError):
            service.add_stock(product.id, -5)

    def test_reduce_stock_success(self, service, sample_product_data):
        """Test reducing stock successfully."""
        product = service.create_product(**sample_product_data)
        original_stock = product.stock

        result = service.reduce_stock(product.id, 3)

        assert result is True
        assert product.stock == original_stock - 3

    def test_reduce_stock_product_not_found(self, service):
        """Test reducing stock from non-existent product."""
        result = service.reduce_stock(999, 5)
        assert result is False

    def test_reduce_stock_insufficient_raises_error(self, service, sample_product_data):
        """Test reducing more stock than available raises error."""
        product = service.create_product(**sample_product_data)

        with pytest.raises(ValueError):
            service.reduce_stock(product.id, 999)

    def test_get_total_inventory_value_empty(self, service):
        """Test calculating total inventory value when empty."""
        total = service.get_total_inventory_value()
        assert total == Decimal("0")

    def test_get_total_inventory_value_with_products(self, service):
        """Test calculating total inventory value with products."""
        service.create_product(
            name="Product1",
            description="Test",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )
        service.create_product(
            name="Product2",
            description="Test",
            price=Decimal("20.00"),
            stock=3,
            category="Test"
        )

        # Total = (10 * 5) + (20 * 3) = 50 + 60 = 110
        total = service.get_total_inventory_value()
        assert round(total, 2) == Decimal("110.00")

    def test_get_low_stock_products_default_threshold(self, service):
        """Test getting low stock products with default threshold."""
        service.create_product(
            name="Low Stock",
            description="Test",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )
        service.create_product(
            name="High Stock",
            description="Test",
            price=Decimal("20.00"),
            stock=50,
            category="Test"
        )
        service.create_product(
            name="Out of Stock",
            description="Test",
            price=Decimal("30.00"),
            stock=0,
            category="Test"
        )

        low_stock = service.get_low_stock_products()
        assert len(low_stock) == 1
        assert low_stock[0].name == "Low Stock"

    def test_get_low_stock_products_custom_threshold(self, service):
        """Test getting low stock products with custom threshold."""
        service.create_product(
            name="Product1",
            description="Test",
            price=Decimal("10.00"),
            stock=15,
            category="Test"
        )
        service.create_product(
            name="Product2",
            description="Test",
            price=Decimal("20.00"),
            stock=25,
            category="Test"
        )

        low_stock = service.get_low_stock_products(threshold=20)
        assert len(low_stock) == 1
        assert low_stock[0].stock == 15

    def test_get_out_of_stock_products(self, service):
        """Test getting out of stock products."""
        service.create_product(
            name="In Stock",
            description="Test",
            price=Decimal("10.00"),
            stock=5,
            category="Test"
        )
        service.create_product(
            name="Out of Stock 1",
            description="Test",
            price=Decimal("20.00"),
            stock=0,
            category="Test"
        )
        service.create_product(
            name="Out of Stock 2",
            description="Test",
            price=Decimal("30.00"),
            stock=0,
            category="Test"
        )

        out_of_stock = service.get_out_of_stock_products()
        assert len(out_of_stock) == 2
        assert all(p.stock == 0 for p in out_of_stock)

    def test_count_products_empty(self, service):
        """Test counting products when service is empty."""
        count = service.count_products()
        assert count == 0

    def test_count_products_with_data(self, service, sample_product_data):
        """Test counting products with data."""
        service.create_product(**sample_product_data)
        service.create_product(**sample_product_data)
        service.create_product(**sample_product_data)

        count = service.count_products()
        assert count == 3

    def test_count_products_after_deletion(self, service, sample_product_data):
        """Test counting products after deletion."""
        product1 = service.create_product(**sample_product_data)
        product2 = service.create_product(**sample_product_data)

        assert service.count_products() == 2

        service.delete_product(product1.id)
        assert service.count_products() == 1
