# authentication/service/interface_adapters/controllers/logout_controller.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.application.use_cases.logout_user import LogoutUser

class LogoutController(APIView):
    def post(self, request):
        logout_use_case = LogoutUser()
        try:
            logout_use_case.execute(request.user)
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
