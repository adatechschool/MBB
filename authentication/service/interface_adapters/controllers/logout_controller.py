# authentication/service/interface_adapters/controllers/logout_controller.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class LogoutController(APIView):
    def post(self, request):
        try:
            # Expecting the refresh token in the request body
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                return Response({"error": "Refresh token is required."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token
            
            return Response({"message": "Successfully logged out."},
                            status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
