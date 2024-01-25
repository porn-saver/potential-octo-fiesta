from fastapi import APIRouter, Request

from api import main
from api.controllers.video.models.SortEnum import SORTENUM
from api.middleware.cache import setCacheData

router = APIRouter(
    prefix='/video',
    tags=['video']
)


@router.get("/all")
def get_all_stars(request: Request, quantity: int = 5, page: int = 1, sort_by: SORTENUM = None):
    print('test video')
    main.client.changeVideoKeyWords({})
    return setCacheData(request, main.client.getVideos(quantity, page, sort_by, False))

