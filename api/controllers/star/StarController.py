from fastapi import Request

from fastapi import APIRouter, Depends

from api import main
from api.controllers.star.models.FilterStar import FilterStar
from api.controllers.star.models.SortEnum import SORTENUM
from api.middleware.cache import setCacheData
from api.shared.ErrorResponse import ErrorResponse
from api.shared.enums.QuantityEnum import QuantityEnum

router = APIRouter(
    prefix='/star',
    tags=['star']
)


@router.get("/all")
def get_all_stars(request: Request, quantity: QuantityEnum = 5, page: int = 1, sort_by: SORTENUM = None):
    main.client.changeStarKeyWords({})
    return setCacheData(request, main.client.getStars(int(quantity), page, sort_by))


@router.get("/filter")
def get_all_stars_filter(request: Request, params: FilterStar = Depends(FilterStar)):
    main.client.changeStarKeyWords(params)
    return setCacheData(request, main.client.getStars(int(params.quantity), params.page, params.sort_by))


@router.get("/byName")
def get_star_by_name(request: Request, name: str):
    if not name:
        errorResponse: ErrorResponse = ErrorResponse(400, 'Bas request')
        return errorResponse
    searchName = name.lower().replace(' ', '-')
    main.client.changeStarKeyWords({searchName})
    return setCacheData(request, main.client.getStarByName(searchName))
