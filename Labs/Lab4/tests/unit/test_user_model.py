"""Unit tests for User model."""

import pytest
from datetime import datetime
from src.app.models.user import User


class TestUserModel:
    """Test suite for User model."""

    def test_create_valid_user(self):
        """Test creating a valid user."""
        user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            created_at=datetime.now()
        )

        assert user.id == 1
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert user.role == "user"

    def test_create_user_with_custom_role(self):
        """Test creating user with admin role."""
        user = User(
            id=1,
            username="admin_user",
            email="admin@example.com",
            created_at=datetime.now(),
            role="admin"
        )

        assert user.role == "admin"
        assert user.is_admin() is True

    def test_invalid_username_too_short(self):
        """Test that short username raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 characters"):
            User(
                id=1,
                username="ab",
                email="test@example.com",
                created_at=datetime.now()
            )

    def test_invalid_username_too_long(self):
        """Test that long username raises ValueError."""
        with pytest.raises(ValueError, match="must not exceed 50 characters"):
            User(
                id=1,
                username="a" * 51,
                email="test@example.com",
                created_at=datetime.now()
            )

    def test_invalid_username_special_chars(self):
        """Test that username with special characters raises ValueError."""
        with pytest.raises(ValueError, match="can only contain"):
            User(
                id=1,
                username="user@name!",
                email="test@example.com",
                created_at=datetime.now()
            )

    def test_invalid_email_format(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            User(
                id=1,
                username="testuser",
                email="invalid-email",
                created_at=datetime.now()
            )

    def test_invalid_role(self):
        """Test that invalid role raises ValueError."""
        with pytest.raises(ValueError, match="Role must be one of"):
            User(
                id=1,
                username="testuser",
                email="test@example.com",
                created_at=datetime.now(),
                role="superuser"
            )

    def test_deactivate_user(self):
        """Test deactivating a user."""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=datetime.now()
        )

        user.deactivate()
        assert user.is_active is False

    def test_activate_user(self):
        """Test activating a deactivated user."""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=datetime.now(),
            is_active=False
        )

        user.activate()
        assert user.is_active is True

    def test_is_admin_returns_true_for_admin(self):
        """Test is_admin returns True for admin role."""
        user = User(
            id=1,
            username="admin",
            email="admin@example.com",
            created_at=datetime.now(),
            role="admin"
        )

        assert user.is_admin() is True

    def test_is_admin_returns_false_for_regular_user(self):
        """Test is_admin returns False for regular user."""
        user = User(
            id=1,
            username="regular",
            email="user@example.com",
            created_at=datetime.now()
        )

        assert user.is_admin() is False

    def test_to_dict(self):
        """Test converting user to dictionary."""
        created_at = datetime.now()
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=created_at
        )

        user_dict = user.to_dict()

        assert user_dict["id"] == 1
        assert user_dict["username"] == "testuser"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["created_at"] == created_at.isoformat()
        assert user_dict["is_active"] is True
        assert user_dict["role"] == "user"

    def test_from_dict(self):
        """Test creating user from dictionary."""
        data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "role": "user"
        }

        user = User.from_dict(data)

        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.role == "user"
