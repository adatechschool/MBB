# services/authentication/application/services.py

import uuid
from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from services.authentication.infrastructure.repositories import AuthRepository
from services.posts.domain.models import RoleModel

User = get_user_model()


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register_user(self, username: str, password: str, email: str = None):
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already taken.")
        default_role, _ = RoleModel.objects.get_or_create(role_name=RoleModel.USER)
        user = User(username=username, email=email, role=default_role)
        user.password = make_password(password)
        user.save()
        return user

    def login_user(self, username: str, password: str):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("Invalid username or password.")

        if not check_password(password, user.password):
            raise ValueError("Invalid username or password.")

        # Generate a token and create a new authentication session (valid for 1 hour)
        token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = self.repository.create_session(user, token, expires_at)
        return session

    def logout_user(self, token: str):
        session = self.repository.get_session_by_token(token)
        if session:
            self.repository.delete_session(session)
            return True
        return False

    def verify_token(self, token: str):
        session = self.repository.get_session_by_token(token)
        if session and session.is_valid:
            return session.user
        return None
