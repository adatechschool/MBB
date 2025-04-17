# authentication/service/interface_adapters/controllers/logout_controller.py

"""Module handling user logout functionality through JWT token blacklisting."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutController(APIView):
    """Controller handling user logout by blacklisting their JWT refresh token."""

    def post(self, request):
        """Handle POST request to logout user by blacklisting their refresh token.

        Args:
            request: HTTP request object containing refresh token in cookies.

        Returns:
            Response: HTTP response indicating logout success or error
        """
        try:
            # Get the refresh token from the HttpOnly cookie
            refresh_token = request.COOKIES.get("refreshToken")

            if refresh_token is None:
                return Response(
                    {"error": "Refresh token is required in cookie."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token

            # Clear cookies after logout
            response = Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
            response.delete_cookie("accessToken", path="/")
            response.delete_cookie("refreshToken", path="/")

            return response

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
