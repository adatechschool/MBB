# authentication/service/application/use_cases/login_user.py

import datetime
import jwt  # make sure you have installed PyJWT (pip install PyJWT)
from django.contrib.auth.hashers import check_password
from django.conf import settings

class LoginUser:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise Exception("User not found")

        if not check_password(password, user.hashed_password):
            raise Exception("Invalid credentials")

        # Create a JWT token with an expiration (e.g., 1 hour)
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
