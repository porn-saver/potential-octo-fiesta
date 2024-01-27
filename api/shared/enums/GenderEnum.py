from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    m2f = "mujerTrans"
    f2f = "hombreTrans"
