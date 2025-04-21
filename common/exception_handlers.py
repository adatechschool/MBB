# common\exception_handlers.py

"""Custom exception handlers for the API.

This module contains custom exception handlers to provide consistent error responses
across the API. It handles specific exceptions like UserAlreadyExists and
AuthenticationFailed with appropriate HTTP status codes and formatted error messages.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from authentication.service.exceptions import (
    UserAlreadyExists,
    AuthenticationFailed,
    TokenBlacklistError,
)


def custom_exception_handler(exc, context):
    """Handle custom exceptions and return appropriate API responses.

    Args:
        exc: The exception that was raised
        context: Additional context information

    Returns:
        Response: A REST framework Response object with error details
    """
    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, UserAlreadyExists):
        return Response(
            {"status": "error", "error": {"message": str(exc)}},
            status=status.HTTP_409_CONFLICT,
        )
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {"status": "error", "error": {"message": str(exc)}},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, TokenBlacklistError):
        return Response(
            {"status": "error", "error": {"message": str(exc)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"status": "error", "error": {"message": "Internal server error"}},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
