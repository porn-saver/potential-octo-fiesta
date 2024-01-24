from fastapi import APIRouter, Request

from api import main
from api.controllers.video.models.SortEnum import SORTENUM
from api.core.downloadCore import custom_dl_download
from api.middleware.cache import setCacheData

router = APIRouter(
    prefix='/video',
    tags=['video']
)


@router.get("/all")
def get_all_stars(request: Request, quantity: int = 5, page: int = 1, sort_by: SORTENUM = None):
    main.client.changeVideoKeyWords({})
    return setCacheData(request, main.client.getVideos(quantity, page, sort_by, False))


@router.get("/download")
def get_all_stars(request: Request, url: str):
    main.client.changeVideoKeyWords({})
    return custom_dl_download(url)
