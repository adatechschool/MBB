# common\response.py

"""Common response module for returning HTTP responses."""

from rest_framework.response import Response


def success(data=None, http_status=200):
    """
    Wrap a successful response in a standard envelope.
    - data: any JSON-serializable object (default: {}).
    - http_status: HTTP status code (default: 200).
    """
    return Response(
        {
            "status": "success",
            "data": data or {},
            "error": None
        },
        status=http_status,
    )


def error(message, http_status):
    """
    Wrap an error response.
    - message: human-readable string.
    - http_status: HTTP status code.
    """
    return Response(
        {
            "status": "error",
            "data": None,
            "error": {
                "code": http_status,
                "message": message
            },
        },
        status=http_status,
    )
