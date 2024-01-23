from fastapi import Request

from fastapi import APIRouter, Depends

from api import main
from api.controllers.star.models.FilterStar import FilterStar
from api.controllers.star.models.SortEnum import SORTENUM
from api.middleware.cache import setCacheData

router = APIRouter(
    prefix='/star',
    tags=['star']
)


@router.get("/all")
def get_all_stars(request: Request, quantity: int = 5, page: int = 1, sort_by: SORTENUM = None):
    main.client.changeStarKeyWords({})
    return{"msg":"aaaaaa putaaaaaa"}
    return setCacheData(request, main.client.getStars(quantity, page, sort_by))


@router.get("/filter")
def get_all_stars_filter(request: Request, params: FilterStar = Depends(FilterStar)):
    main.client.changeStarKeyWords(params)
    return setCacheData(request, main.client.getStars(params.quantity, params.page, params.sort_by.value))


@router.get("/byName")
def get_star_by_name(request: Request, name=''):
    searchName = name.lower().replace(' ', '-')
    main.client.changeStarKeyWords({searchName})
    return setCacheData(request, main.client.getStarByName(searchName))
