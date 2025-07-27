from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger

async def catch_exceptions_middleware(request:Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception("Unhandled exception occurred")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(exc)})
    