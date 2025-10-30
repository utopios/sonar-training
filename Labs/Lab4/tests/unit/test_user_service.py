"""Unit tests for UserService."""

import pytest
from datetime import datetime
from src.app.services.user_service import UserService


class TestUserService:
    """Test suite for UserService."""

    @pytest.fixture
    def user_service(self):
        """Create a fresh UserService instance for each test."""
        return UserService()

    def test_create_user_success(self, user_service):
        """Test creating a user successfully."""
        user = user_service.create_user("john_doe", "john@example.com")

        assert user.id == 1
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.role == "user"
        assert user.is_active is True

    def test_create_user_with_admin_role(self, user_service):
        """Test creating user with admin role."""
        user = user_service.create_user("admin", "admin@example.com", role="admin")

        assert user.role == "admin"
        assert user.is_admin() is True

    def test_create_user_duplicate_username_raises_error(self, user_service):
        """Test creating user with duplicate username raises error."""
        user_service.create_user("john_doe", "john@example.com")

        with pytest.raises(ValueError, match="Username .* already exists"):
            user_service.create_user("john_doe", "different@example.com")

    def test_create_user_duplicate_email_raises_error(self, user_service):
        """Test creating user with duplicate email raises error."""
        user_service.create_user("john_doe", "john@example.com")

        with pytest.raises(ValueError, match="Email .* already exists"):
            user_service.create_user("different_user", "john@example.com")

    def test_get_user_by_id(self, user_service):
        """Test getting user by ID."""
        created_user = user_service.create_user("john_doe", "john@example.com")
        retrieved_user = user_service.get_user(created_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.username == "john_doe"

    def test_get_user_nonexistent_returns_none(self, user_service):
        """Test getting nonexistent user returns None."""
        user = user_service.get_user(999)
        assert user is None

    def test_get_user_by_username(self, user_service):
        """Test getting user by username."""
        user_service.create_user("john_doe", "john@example.com")
        user = user_service.get_user_by_username("john_doe")

        assert user is not None
        assert user.username == "john_doe"

    def test_get_user_by_username_nonexistent_returns_none(self, user_service):
        """Test getting nonexistent username returns None."""
        user = user_service.get_user_by_username("nonexistent")
        assert user is None

    def test_get_user_by_email(self, user_service):
        """Test getting user by email."""
        user_service.create_user("john_doe", "john@example.com")
        user = user_service.get_user_by_email("john@example.com")

        assert user is not None
        assert user.email == "john@example.com"

    def test_get_user_by_email_nonexistent_returns_none(self, user_service):
        """Test getting nonexistent email returns None."""
        user = user_service.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_get_all_users(self, user_service):
        """Test getting all users."""
        user_service.create_user("user1", "user1@example.com")
        user_service.create_user("user2", "user2@example.com")
        user_service.create_user("user3", "user3@example.com")

        users = user_service.get_all_users()
        assert len(users) == 3

    def test_get_active_users(self, user_service):
        """Test getting only active users."""
        user1 = user_service.create_user("user1", "user1@example.com")
        user2 = user_service.create_user("user2", "user2@example.com")
        user_service.create_user("user3", "user3@example.com")

        user1.deactivate()

        active_users = user_service.get_active_users()
        assert len(active_users) == 2

    def test_get_users_by_role(self, user_service):
        """Test getting users by role."""
        user_service.create_user("user1", "user1@example.com", role="user")
        user_service.create_user("admin1", "admin1@example.com", role="admin")
        user_service.create_user("admin2", "admin2@example.com", role="admin")

        admins = user_service.get_users_by_role("admin")
        assert len(admins) == 2

        users = user_service.get_users_by_role("user")
        assert len(users) == 1

    def test_update_user_username(self, user_service):
        """Test updating user username."""
        user = user_service.create_user("old_name", "user@example.com")
        updated = user_service.update_user(user.id, username="new_name")

        assert updated is not None
        assert updated.username == "new_name"

    def test_update_user_email(self, user_service):
        """Test updating user email."""
        user = user_service.create_user("user", "old@example.com")
        updated = user_service.update_user(user.id, email="new@example.com")

        assert updated is not None
        assert updated.email == "new@example.com"

    def test_update_user_duplicate_username_raises_error(self, user_service):
        """Test updating to duplicate username raises error."""
        user_service.create_user("user1", "user1@example.com")
        user2 = user_service.create_user("user2", "user2@example.com")

        with pytest.raises(ValueError, match="Username .* already exists"):
            user_service.update_user(user2.id, username="user1")

    def test_update_user_duplicate_email_raises_error(self, user_service):
        """Test updating to duplicate email raises error."""
        user_service.create_user("user1", "user1@example.com")
        user2 = user_service.create_user("user2", "user2@example.com")

        with pytest.raises(ValueError, match="Email .* already exists"):
            user_service.update_user(user2.id, email="user1@example.com")

    def test_update_user_nonexistent_returns_none(self, user_service):
        """Test updating nonexistent user returns None."""
        updated = user_service.update_user(999, username="test")
        assert updated is None

    def test_delete_user_success(self, user_service):
        """Test deleting user successfully."""
        user = user_service.create_user("user", "user@example.com")
        result = user_service.delete_user(user.id)

        assert result is True
        assert user_service.get_user(user.id) is None

    def test_delete_user_nonexistent_returns_false(self, user_service):
        """Test deleting nonexistent user returns False."""
        result = user_service.delete_user(999)
        assert result is False

    def test_deactivate_user_success(self, user_service):
        """Test deactivating user successfully."""
        user = user_service.create_user("user", "user@example.com")
        result = user_service.deactivate_user(user.id)

        assert result is True
        assert user.is_active is False

    def test_deactivate_user_nonexistent_returns_false(self, user_service):
        """Test deactivating nonexistent user returns False."""
        result = user_service.deactivate_user(999)
        assert result is False

    def test_activate_user_success(self, user_service):
        """Test activating user successfully."""
        user = user_service.create_user("user", "user@example.com")
        user.deactivate()

        result = user_service.activate_user(user.id)

        assert result is True
        assert user.is_active is True

    def test_activate_user_nonexistent_returns_false(self, user_service):
        """Test activating nonexistent user returns False."""
        result = user_service.activate_user(999)
        assert result is False

    def test_count_users(self, user_service):
        """Test counting total users."""
        user_service.create_user("user1", "user1@example.com")
        user_service.create_user("user2", "user2@example.com")

        count = user_service.count_users()
        assert count == 2

    def test_count_active_users(self, user_service):
        """Test counting active users."""
        user1 = user_service.create_user("user1", "user1@example.com")
        user_service.create_user("user2", "user2@example.com")

        user1.deactivate()

        active_count = user_service.count_active_users()
        assert active_count == 1
