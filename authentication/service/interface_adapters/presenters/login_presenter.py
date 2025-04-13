# authentication/service/interface_adapters/presenters/login_presenter.py

from rest_framework.response import Response

class LoginPresenter:
    def present(self, token: str) -> Response:
        return Response({
            "token": token,
            "message": "Authentication successful"
        })
