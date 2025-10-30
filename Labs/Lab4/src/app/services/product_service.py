"""Product service for inventory management."""

from typing import List, Optional
from decimal import Decimal
from src.app.models.product import Product


class ProductService:
    """Service for managing product operations."""

    def __init__(self):
        """Initialize product service with in-memory storage."""
        self._products: dict[int, Product] = {}
        self._next_id: int = 1

    def create_product(
        self,
        name: str,
        description: str,
        price: Decimal,
        stock: int,
        category: str
    ) -> Product:
        """
        Create a new product.

        Args:
            name: Product name.
            description: Product description.
            price: Product price.
            stock: Initial stock quantity.
            category: Product category.

        Returns:
            Product: Created product instance.
        """
        product = Product(
            id=self._next_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )

        self._products[self._next_id] = product
        self._next_id += 1

        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Get product by ID.

        Args:
            product_id: Product ID to retrieve.

        Returns:
            Optional[Product]: Product instance or None if not found.
        """
        return self._products.get(product_id)

    def get_all_products(self) -> List[Product]:
        """
        Get all products.

        Returns:
            List[Product]: List of all products.
        """
        return list(self._products.values())

    def get_available_products(self) -> List[Product]:
        """
        Get all available products.

        Returns:
            List[Product]: List of available products.
        """
        return [p for p in self._products.values() if p.is_in_stock()]

    def get_products_by_category(self, category: str) -> List[Product]:
        """
        Get products by category.

        Args:
            category: Category to filter by.

        Returns:
            List[Product]: List of products in category.
        """
        return [p for p in self._products.values() if p.category == category]

    def search_products(self, query: str) -> List[Product]:
        """
        Search products by name or description.

        Args:
            query: Search query string.

        Returns:
            List[Product]: List of matching products.
        """
        query_lower = query.lower()
        return [
            p for p in self._products.values()
            if query_lower in p.name.lower() or query_lower in p.description.lower()
        ]

    def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        """
        Update product attributes.

        Args:
            product_id: Product ID to update.
            **kwargs: Attributes to update.

        Returns:
            Optional[Product]: Updated product or None if not found.
        """
        product = self.get_product(product_id)
        if not product:
            return None

        # Update allowed fields
        allowed_fields = ['name', 'description', 'price', 'stock', 'category', 'is_available']
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(product, key, value)

        # Re-validate after update
        product.validate_name()
        product.validate_price()
        product.validate_stock()

        return product

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product.

        Args:
            product_id: Product ID to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

    def add_stock(self, product_id: int, quantity: int) -> bool:
        """
        Add stock to a product.

        Args:
            product_id: Product ID.
            quantity: Quantity to add.

        Returns:
            bool: True if successful, False if product not found.

        Raises:
            ValueError: If quantity is invalid.
        """
        product = self.get_product(product_id)
        if not product:
            return False

        product.add_stock(quantity)
        return True

    def reduce_stock(self, product_id: int, quantity: int) -> bool:
        """
        Reduce stock from a product.

        Args:
            product_id: Product ID.
            quantity: Quantity to reduce.

        Returns:
            bool: True if successful, False if product not found.

        Raises:
            ValueError: If quantity is invalid or insufficient stock.
        """
        product = self.get_product(product_id)
        if not product:
            return False

        product.reduce_stock(quantity)
        return True

    def get_total_inventory_value(self) -> Decimal:
        """
        Calculate total inventory value.

        Returns:
            Decimal: Total value of all products in stock.
        """
        total = Decimal('0')
        for product in self._products.values():
            total += product.price * product.stock
        return total

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Get products with low stock.

        Args:
            threshold: Stock level threshold (default: 10).

        Returns:
            List[Product]: Products with stock below threshold.
        """
        return [p for p in self._products.values() if 0 < p.stock < threshold]

    def get_out_of_stock_products(self) -> List[Product]:
        """
        Get out of stock products.

        Returns:
            List[Product]: Products with zero stock.
        """
        return [p for p in self._products.values() if p.stock == 0]

    def count_products(self) -> int:
        """
        Count total products.

        Returns:
            int: Total number of products.
        """
        return len(self._products)
