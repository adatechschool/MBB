# authentication/service/interface_adapters/presenters/auth_presenter.py

from rest_framework.response import Response

class AuthPresenter:
    def present(self, token: str) -> Response:
        return Response({
            "token": token,
            "message": "Authentication successful"
        })
