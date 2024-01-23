from pydantic.fields import Field
from pydantic.main import BaseModel

from api.controllers.star.models.SortEnum import SORTENUM


class FilterStar(BaseModel):
    performerType: str = Field(enum=['', 'amateur', 'pornstar'], default='')
    gender: str = Field(enum=['', 'male', 'female', 'm2f', 'f2f'], default='')
    ethnicity: str = Field(enum=['', 'asian', 'indian', 'black', 'middle+eastern', 'latin', 'mixed', 'white', 'other'],
                           default='')
    hair: str = Field(enum=['', 'auburn', 'bald', 'black', 'blonde', 'brunette', 'grey', 'red', 'varius', 'other'],
                      default='')
    tattoos: str = Field(enum=['', 'yes', 'no'], default='')
    piercings: str = Field(enum=['', 'yes', 'no'], default='')
    breasttype: str = Field(enum=['', ' natural', 'fake'], default='')
    minAge: str = Field(default='')
    maxAge: str = Field(default='')
    cup: str = Field(enum=['', 'a', 'b', 'c', 'd', 'e', 'f-z'], default='')
    quantity: int = Field(default=5)
    page: int = Field(default=1)
    sort_by: SORTENUM = Field(default='rank')
