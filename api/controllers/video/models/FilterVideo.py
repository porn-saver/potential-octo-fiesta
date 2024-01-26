from pydantic import BaseModel
from pydantic.fields import Field

from api.controllers.video.models.SortEnum import SORTENUM


class FilterVideo(BaseModel):
    search: str = Field(default='')
    isHd: bool = Field(default=False)
    production: str = Field(enum=['', 'homemade', 'professional'], default='')
    min_duration: int = Field(default=0)
    max_duration: int = Field(default=0)

    quantity: int = Field(default=5)
    page: int = Field(default=1)
    sort_by: SORTENUM = Field(default='recent')
