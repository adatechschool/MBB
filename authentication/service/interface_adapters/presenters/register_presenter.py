# authentication\service\interface_adapters\presenters\register_presenter.py

from rest_framework.response import Response

class RegisterPresenter:
    def present(self, user_data: dict) -> Response:
        return Response({
            "message": "Registration successful",
            "user": user_data,
        })
