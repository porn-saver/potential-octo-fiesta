from fastapi import APIRouter, Request, Depends

from api import main
from api.controllers.video.models.FilterVideo import FilterVideo
from api.controllers.video.models.SortEnum import SORTENUM
from api.core.downloadCore import custom_dl_download
from api.middleware.cache import setCacheData
from api.shared.ErrorResponse import ErrorResponse
from api.shared.enums.QuantityEnum import QuantityEnum

router = APIRouter(
    prefix='/video',
    tags=['video']
)


@router.get("/all")
def get_all_videos(request: Request, quantity: QuantityEnum = 5, page: int = 1, sort_by: SORTENUM = None):
    main.client.changeVideoKeyWords({})
    return setCacheData(request, main.client.getVideos(int(quantity), page, sort_by, False))


@router.get("/filter")
def get_all_videos_filter(request: Request, params: FilterVideo = Depends(FilterVideo)):
    main.client.changeVideoKeyWords(params)
    return setCacheData(request, main.client.getVideos(int(params.quantity), params.page, params.sort_by))


@router.get("/download")
def get_download_video(request: Request, url: str):
    if not url:
        errorResponse: ErrorResponse = ErrorResponse(400, 'Bas request')
        return errorResponse
    return setCacheData(request, custom_dl_download(url))
