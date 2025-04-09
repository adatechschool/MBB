# services/authentication/infrastructure/repositories.py

from services.authentication.domain.models import AuthSession


class AuthRepository:
    def create_session(self, user, token, expires_at):
        session = AuthSession.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        return session

    def get_session_by_token(self, token):
        try:
            return AuthSession.objects.get(token=token)
        except AuthSession.DoesNotExist:
            return None

    def delete_session(self, session):
        session.delete()
