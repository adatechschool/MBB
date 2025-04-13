# authentication/service/application/use_cases/logout_user.py

from rest_framework.authtoken.models import Token

class LogoutUser:
    def execute(self, user):
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return True
        except Token.DoesNotExist:
            # Alternatively, you could choose to silently succeed if no token exists.
            raise Exception("User token not found – possibly already logged out.")
