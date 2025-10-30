"""User service for business logic."""

from typing import List, Optional
from datetime import datetime
from src.app.models.user import User


class UserService:
    """Service for managing user operations."""

    def __init__(self):
        """Initialize user service with in-memory storage."""
        self._users: dict[int, User] = {}
        self._next_id: int = 1

    def create_user(self, username: str, email: str, role: str = "user") -> User:
        """
        Create a new user.

        Args:
            username: User's username.
            email: User's email address.
            role: User's role (default: "user").

        Returns:
            User: Created user instance.

        Raises:
            ValueError: If username or email already exists.
        """
        # Check for duplicate username
        if self.get_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists")

        # Check for duplicate email
        if self.get_user_by_email(email):
            raise ValueError(f"Email '{email}' already exists")

        user = User(
            id=self._next_id,
            username=username,
            email=email,
            created_at=datetime.now(),
            role=role
        )

        self._users[self._next_id] = user
        self._next_id += 1

        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID to retrieve.

        Returns:
            Optional[User]: User instance or None if not found.
        """
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for.

        Returns:
            Optional[User]: User instance or None if not found.
        """
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: Email to search for.

        Returns:
            Optional[User]: User instance or None if not found.
        """
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> List[User]:
        """
        Get all users.

        Returns:
            List[User]: List of all users.
        """
        return list(self._users.values())

    def get_active_users(self) -> List[User]:
        """
        Get all active users.

        Returns:
            List[User]: List of active users.
        """
        return [user for user in self._users.values() if user.is_active]

    def get_users_by_role(self, role: str) -> List[User]:
        """
        Get users by role.

        Args:
            role: Role to filter by.

        Returns:
            List[User]: List of users with specified role.
        """
        return [user for user in self._users.values() if user.role == role]

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update user attributes.

        Args:
            user_id: User ID to update.
            **kwargs: Attributes to update.

        Returns:
            Optional[User]: Updated user or None if not found.

        Raises:
            ValueError: If trying to update to duplicate username/email.
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # Check for duplicate username if updating
        if 'username' in kwargs and kwargs['username'] != user.username:
            if self.get_user_by_username(kwargs['username']):
                raise ValueError(f"Username '{kwargs['username']}' already exists")

        # Check for duplicate email if updating
        if 'email' in kwargs and kwargs['email'] != user.email:
            if self.get_user_by_email(kwargs['email']):
                raise ValueError(f"Email '{kwargs['email']}' already exists")

        # Update allowed fields
        allowed_fields = ['username', 'email', 'role', 'is_active']
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(user, key, value)

        # Re-validate after update
        user.validate_username()
        user.validate_email()
        user.validate_role()

        return user

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user.

        Args:
            user_id: User ID to deactivate.

        Returns:
            bool: True if deactivated, False if not found.
        """
        user = self.get_user(user_id)
        if user:
            user.deactivate()
            return True
        return False

    def activate_user(self, user_id: int) -> bool:
        """
        Activate a user.

        Args:
            user_id: User ID to activate.

        Returns:
            bool: True if activated, False if not found.
        """
        user = self.get_user(user_id)
        if user:
            user.activate()
            return True
        return False

    def count_users(self) -> int:
        """
        Count total users.

        Returns:
            int: Total number of users.
        """
        return len(self._users)

    def count_active_users(self) -> int:
        """
        Count active users.

        Returns:
            int: Number of active users.
        """
        return len(self.get_active_users())
