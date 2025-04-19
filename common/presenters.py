# common\presenters.py

"""Presenter for formatting HTTP responses."""

from rest_framework.response import Response


class BasePresenter:
    """Wraps all responses in {status,data,error}."""

    def success(self, data: dict, http_status=200) -> Response:
        """Format successful response with provided data.

        Args:
            data (dict): The response payload to return
            http_status (int, optional): HTTP status code. Defaults to 200.

        Returns:
            Response: DRF Response object with formatted success payload
        """
        return Response(
            {
                "status": "success",
                "data": data,
                "error": None,
            },
            status=http_status,
        )

    def error(self, message: str, code: int = 400) -> Response:
        """Format error response with provided message and code.

        Args:
            message (str): The error message to return
            code (int, optional): HTTP status/error code. Defaults to 400.

        Returns:
            Response: DRF Response object with formatted error payload
        """
        return Response(
            {
                "status": "error",
                "data": None,
                "error": {"code": code, "message": message},
            },
            status=code,
        )
