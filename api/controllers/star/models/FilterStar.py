from pydantic.fields import Field
from pydantic.main import BaseModel

from api.controllers.star.models.SortEnum import SORTENUM
from api.shared.enums.BreastTypeEnum import BreastTypeEnum
from api.shared.enums.CupEnum import CupSizeEnum
from api.shared.enums.EthnicityEnum import EthnicityEnum
from api.shared.enums.GenderEnum import GenderEnum
from api.shared.enums.HairColorEnum import HairColorEnum
from api.shared.enums.PerformerTypeEnum import PerformerType
from api.shared.enums.QuantityEnum import QuantityEnum
from api.shared.enums.TottoosEnum import BooleanEnum


class FilterStar(BaseModel):
    performerType: PerformerType = Field(default=None)
    gender: GenderEnum = Field(default=None)
    ethnicity: EthnicityEnum = Field(default=None)
    hair: HairColorEnum = Field(default=None)
    tattoos: BooleanEnum = Field(default=None)
    piercings: BooleanEnum = Field(default=None)
    breasttype: BreastTypeEnum = Field(default=None)
    minAge: str = Field(default='')
    maxAge: str = Field(default='')
    cup: CupSizeEnum = Field(default=None)
    quantity: QuantityEnum = Field(default=5)
    page: int = Field(default=1)
    sort_by: SORTENUM = Field(default=None)
