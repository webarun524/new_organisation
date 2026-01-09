import re
from typing import Any


def create_response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    """Create a standardized Lambda response"""
    return {
        "statusCode": status_code,
        "body": body,
    }


def create_error_response(
    status_code: int, error_message: str, error_type: str = "Error"
) -> dict[str, Any]:
    """Create a standardized error response"""
    return create_response(
        status_code,
        {
            "error": error_type,
            "message": error_message,
        },
    )


def to_snake_case(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
