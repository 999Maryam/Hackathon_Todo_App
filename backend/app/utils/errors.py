"""Custom exception classes and error handlers."""

from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    """Raised when authentication fails (401 Unauthorized)."""

    def __init__(self, detail: str = "Missing or invalid authentication token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class ForbiddenException(HTTPException):
    """Raised when user lacks permission (403 Forbidden)."""

    def __init__(self, detail: str = "You do not have permission to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundException(HTTPException):
    """Raised when resource is not found (404 Not Found)."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class BadRequestException(HTTPException):
    """Raised when request validation fails (400 Bad Request)."""

    def __init__(self, detail: str = "Invalid request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
