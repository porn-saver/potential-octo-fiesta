from pydantic import BaseModel
from pydantic.fields import Field

from api.controllers.video.models.SortEnum import SORTENUM
from api.shared.enums.ProductionEnum import ProductionEnum
from api.shared.enums.TottoosEnum import BooleanEnum


class FilterVideo(BaseModel):
    search: str = Field(default='')
    isHd: BooleanEnum = Field(default=None)
    production: ProductionEnum = Field(default=None)
    min_duration: int = Field(default=0)
    max_duration: int = Field(default=0)
    quantity: int = Field(default=5)
    page: int = Field(default=1)
    sort_by: SORTENUM = Field(default=None)
