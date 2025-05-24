from fastapi import HTTPException, Request, Response


async def connection_error_handler(request: Request, exc: Exception) -> Response:
    """
    Handle connection errors by returning a 503 Service Unavailable response.

    :param request: The request that caused the error.
    :param exc: The exception raised.
    :return: A JSON response with an error message and status code 503.
    """
    return Response(
        content="Service Unavailable. Please try again later.",
        status_code=503,
        media_type="text/plain",
    )
