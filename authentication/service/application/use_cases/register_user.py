# authentication\service\application\use_cases\register_user.py

from django.contrib.auth.hashers import make_password
from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity

class RegisterUser:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password: str) -> UserEntity:
        # Check if the email is already registered.
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise Exception("User already exists")
        
        # Hash the password.
        hashed_password = make_password(password)
        
        # Create the new user.
        new_user = self.user_repository.create_user(username=username, email=email, password=hashed_password)
        return new_user
