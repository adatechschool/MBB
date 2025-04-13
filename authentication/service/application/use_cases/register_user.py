# authentication\service\application\use_cases\register_user.py

"""Use case for registering a new user in the system."""

from django.contrib.auth.hashers import make_password
from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity


class RegisterUser:
    """Use case for registering a new user in the system.

    This class handles the registration of new users by checking for existing emails,
    hashing passwords, and creating new user entities through the user repository.
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
            Exception: If a user with the given email already exists
        """
        # Check if the email is already registered.
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise ValueError("A user with this email already exists")

        # Hash the password.
        hashed_password = make_password(password)

        # Create the new user.
        new_user = self.user_repository.create_user(
            username=username, email=email, password=hashed_password
        )
        return new_user
