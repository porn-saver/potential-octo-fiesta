from fastapi import Request

from fastapi.responses import JSONResponse

from api.middleware.cache import checkCacheDate


async def intercept_all_requests(request: Request, call_next):
    data = checkCacheDate(request)
    if data:
        return JSONResponse(content=data)
    response = await call_next(request)

    return response
