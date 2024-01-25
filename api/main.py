import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

from api.controllers.socket.ConnectionManager import ConnectionManager
from api.controllers.star import StarController
from api.controllers.video import VideoController
from api.core import PornHub
from api.core.downloadCore import custom_dl_download
from api.middleware.cacheInterceptor import intercept_all_requests
from api.middleware.cors import setup_cors
from api.middleware.timeCount import add_process_time_header

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI(title='Porn-saver', version='1.0.0')
client = PornHub([])

# Middleware
app.middleware("http")(intercept_all_requests)
app.middleware("http")(add_process_time_header)

# CORS
setup_cors(app)

app.include_router(StarController.router)
app.include_router(VideoController.router)

manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('test')
    await manager.connect(websocket)
    try:
        url = await websocket.receive_text()
        await custom_dl_download(url, manager, websocket)
        await manager.disconnect(websocket)
        return
    except WebSocketDisconnect as e:
        logger.info(e)
        await manager.send_personal_message(e, websocket)
        await manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=int(8080), log_level="info")
