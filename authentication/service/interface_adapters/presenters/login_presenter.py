# authentication/service/interface_adapters/presenters/login_presenter.py

from rest_framework.response import Response

class LoginPresenter:
    def present(self, token_data):
        return Response(token_data, status=200)
