from enum import Enum


class BooleanEnum(str, Enum):
    true = "yes"
    false = "no"
