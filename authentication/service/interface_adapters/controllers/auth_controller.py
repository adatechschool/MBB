# authentication/service/interface_adapters/controllers/auth_controller.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from service.interface_adapters.presenters.auth_presenter import AuthPresenter
from service.application.use_cases.authenticate_user import AuthenticateUser
from service.interface_adapters.gateways.django_user_repository import DjangoUserRepository

class AuthController(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        user_repository = DjangoUserRepository()
        use_case = AuthenticateUser(user_repository)
        
        try:
            token = use_case.execute(email, password)
        except Exception as e:
            raise AuthenticationFailed(str(e))
        
        presenter = AuthPresenter()
        return presenter.present(token)
