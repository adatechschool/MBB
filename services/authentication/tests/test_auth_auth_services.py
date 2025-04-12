# services\authentication\tests\test_auth_auth_services.py

import pytest
from services.authentication.application.services import AuthService
from services.authentication.infrastructure.repositories import AuthRepository
from django.contrib.auth import get_user_model
from services.authentication.domain.models import AuthSession
from services.roles.domain.models import RoleModel

User = get_user_model()


class DummyAuthRepository(AuthRepository):
    def __init__(self):
        self.sessions = []

    def create_session(self, user, token, expires_at):
        session = AuthSession(user=user, token=token, expires_at=expires_at)
        self.sessions.append(session)
        return session

    def get_session_by_token(self, token):
        for session in self.sessions:
            if session.token == token:
                return session
        return None

    def delete_session(self, session):
        self.sessions.remove(session)


@pytest.fixture
def dummy_repo(db):
    return DummyAuthRepository()


@pytest.fixture
def auth_service(dummy_repo):
    return AuthService(dummy_repo)


@pytest.fixture
def test_user(db):
    default_role, _ = RoleModel.objects.get_or_create(role_name=RoleModel.USER)
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        role=default_role  # supply the required role
    )


def test_register_user(auth_service, db):
    username = "newuser"
    password = "newpass"
    email = "new@example.com"
    user = auth_service.register_user(username, password, email)
    assert user.username == username
    assert user.email == email


def test_login_user_success(auth_service, test_user):
    session = auth_service.login_user("testuser", "testpass")
    assert session.token is not None
    assert session.is_valid


def test_login_user_fail_wrong_password(auth_service, test_user):
    with pytest.raises(ValueError):
        auth_service.login_user("testuser", "wrongpass")
