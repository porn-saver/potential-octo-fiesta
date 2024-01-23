from datetime import datetime

from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    start_time = datetime.utcnow()

    response = await call_next(request)

    end_time = datetime.utcnow()
    process_time = end_time - start_time

    response.headers["X-Process-Time"] = str(process_time.total_seconds())

    return response
