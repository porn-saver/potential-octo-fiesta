import logging
import sys

from fastapi import FastAPI

import uvicorn

from api.controllers.star import StarController
from api.core import PornHub
from api.middleware.cacheInterceptor import intercept_all_requests
from api.middleware.cors import setup_cors
from api.middleware.timeCount import add_process_time_header

app = FastAPI(title='Porn-saver', version='1.0.0')
client = PornHub([])

# Middleware
app.middleware("http")(intercept_all_requests)
app.middleware("http")(add_process_time_header)

# CORS
setup_cors(app)

app.include_router(StarController.router)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=int(8080), log_level="info")
