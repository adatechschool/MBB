# authentication/service/interface_adapters/controllers/login_controller.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from service.interface_adapters.presenters.login_presenter import LoginPresenter
from service.application.use_cases.login_user import LoginUser
from service.interface_adapters.gateways.django_user_repository import DjangoUserRepository

class LoginController(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        user_repository = DjangoUserRepository()
        use_case = LoginUser(user_repository)
        
        try:
            token = use_case.execute(email, password)
        except Exception as e:
            raise AuthenticationFailed(str(e))
        
        presenter = LoginPresenter()
        return presenter.present(token)
