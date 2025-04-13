# authentication/service/interface_adapters/presenters/logout_presenter.py

from rest_framework.response import Response

class LogoutPresenter:
    def present(self, success: bool):
        if success:
            return Response({"message": "Successfully logged out"})
        else:
            return Response({"error": "Failed to log out"}, status=400)
