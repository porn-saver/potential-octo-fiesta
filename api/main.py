from fastapi import FastAPI

import uvicorn

from api.controllers.star import StarController
from api.core import PornHub
from api.middleware.cacheInterceptor import intercept_all_requests
from api.middleware.cors import setup_cors
from api.middleware.timeCount import add_process_time_header

from Proxy_List_Scrapper import Scrapper

scrapper = Scrapper(category='SSL', print_err_trace=False)
app = FastAPI(title='Porn-saver', version='1.0.0')
client = PornHub([])

# Middleware
app.middleware("http")(intercept_all_requests)
app.middleware("http")(add_process_time_header)

# CORS
setup_cors(app)

app.include_router(StarController.router)

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=int(8080), log_level="info")
