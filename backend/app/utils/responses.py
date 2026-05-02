from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(
    message: str = "Berhasil",
    data: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    """Standard success response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error_response(
    message: str,
    errors: Optional[Any] = None,
    status_code: int = 400,
) -> JSONResponse:
    """Standard error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors,
        },
    )


def paginated_response(
    message: str = "Berhasil",
    data: Any = None,
    total: int = 0,
    page: int = 1,
    per_page: int = 20,
) -> JSONResponse:
    """Standard paginated response."""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page,
            },
        },
    )
