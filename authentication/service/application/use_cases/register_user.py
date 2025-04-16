# authentication/service/application/use_cases/register_user.py

"""
Module containing the use case for registering new users in the authentication service.
This module provides functionality to create new user accounts while ensuring email uniqueness.
"""

from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity


class RegisterUser:
    """Use case for registering new users in the system.

    This class handles the business logic for creating new user accounts,
    including validation of unique email addresses.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password: str) -> UserEntity:
        """Register a new user in the system.

        Args:
            username (str): The username for the new user
            email (str): The email address for the new user
            password (str): The password for the new user

        Returns:
            UserEntity: The newly created user entity

        Raises:
            ValueError: If a user with the provided email already exists
        """
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise ValueError("A user with this email already exists")

        new_user = self.user_repository.create_user(
            username=username, email=email, password=password
        )
        return new_user
