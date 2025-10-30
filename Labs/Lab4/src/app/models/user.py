"""User model with validation and business logic."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re


@dataclass
class User:
    """User entity with validation."""

    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True
    role: str = "user"

    def __post_init__(self):
        """Validate user data after initialization."""
        self.validate_username()
        self.validate_email()
        self.validate_role()

    def validate_username(self) -> None:
        """
        Validate username format.

        Raises:
            ValueError: If username is invalid.
        """
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        if len(self.username) > 50:
            raise ValueError("Username must not exceed 50 characters")

        if not re.match(r'^[a-zA-Z0-9_-]+$', self.username):
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")

    def validate_email(self) -> None:
        """
        Validate email format.

        Raises:
            ValueError: If email is invalid.
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

    def validate_role(self) -> None:
        """
        Validate user role.

        Raises:
            ValueError: If role is invalid.
        """
        valid_roles = ["user", "admin", "moderator"]
        if self.role not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def is_admin(self) -> bool:
        """
        Check if user is an administrator.

        Returns:
            bool: True if user is admin, False otherwise.
        """
        return self.role == "admin"

    def to_dict(self) -> dict:
        """
        Convert user to dictionary representation.

        Returns:
            dict: User data as dictionary.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Create user from dictionary.

        Args:
            data: Dictionary containing user data.

        Returns:
            User: New user instance.
        """
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])

        return cls(**data)
