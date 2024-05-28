from fastapi import Request

from fastapi import APIRouter, Depends

from api.middleware.cache import setCacheDataEnum
from api.shared.enums.CupEnum import CupSizeEnum
from api.shared.enums.BreastTypeEnum import BreastTypeEnum
from api.shared.enums.EthnicityEnum import EthnicityEnum
from api.shared.enums.GenderEnum import GenderEnum
from api.shared.enums.HairColorEnum import HairColorEnum
from api.shared.enums.PerformerTypeEnum import PerformerType
from api.shared.enums.ProductionEnum import ProductionEnum
from api.shared.enums.QuantityEnum import QuantityEnum
from api.shared.enums.TottoosEnum import BooleanEnum

router = APIRouter(
    prefix='/combos',
    tags=['combos']
)


@router.get("/breast-type")
def get_breast_type_enum(request: Request):
    return setCacheDataEnum(request, BreastTypeEnum)


@router.get("/cup")
def get_cup_enum(request: Request):
    return setCacheDataEnum(request, CupSizeEnum)


@router.get("/ethnicity")
def get_ethnicity_enum(request: Request):
    return setCacheDataEnum(request, EthnicityEnum)


@router.get("/gender")
def get_gender_enum(request: Request):
    return setCacheDataEnum(request, GenderEnum)


@router.get("/hair-color")
def get_hair_color_enum(request: Request):
    return setCacheDataEnum(request, HairColorEnum)


@router.get("/performer-type")
def get_performer_type_enum(request: Request):
    return setCacheDataEnum(request, PerformerType)


@router.get("/production")
def get_production_enum(request: Request):
    return setCacheDataEnum(request, ProductionEnum)


@router.get("/quantity")
def get_quantity_enum(request: Request):
    return setCacheDataEnum(request, QuantityEnum)


@router.get("/tattoos")
def get_tattoos_enum(request: Request):
    return setCacheDataEnum(request, BooleanEnum)
