from fastapi import APIRouter, Request

from api import main
from api.controllers.video.models.SortEnum import SORTENUM
from api.core.downloadCore import custom_dl_download
from api.middleware.cache import setCacheData
from api.shared.ErrorResponse import ErrorResponse

router = APIRouter(
    prefix='/video',
    tags=['video']
)


@router.get("/all")
def get_all_videos(request: Request, quantity: int = 5, page: int = 1, sort_by: SORTENUM = None):
    main.client.changeVideoKeyWords({})
    return setCacheData(request, main.client.getVideos(quantity, page, sort_by, False))


@router.get("/download")
def get_download_video(request: Request, url: str):
    if not url:
        errorResponse: ErrorResponse = ErrorResponse(400, 'Bas request')
        return errorResponse
    return setCacheData(request, custom_dl_download(url))
