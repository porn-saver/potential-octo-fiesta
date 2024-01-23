from enum import Enum


class SORTENUM(str, Enum):
    mv = "view"
    t = "trend"
    ms = "subs"
    a = "alpha"
    nv = "videos"
    r = "random"
    ra = "rank"
