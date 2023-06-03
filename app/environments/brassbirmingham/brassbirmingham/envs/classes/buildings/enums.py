from enum import Enum


class BuildingName(Enum):
    goods = "goods"
    cotton = "cotton"
    pottery = "pottery"
    coal = "coal"
    beer = "beer"
    iron = "iron"


class BuildingType(Enum):
    industry = "industry"
    market = "market"

class MerchantName(Enum):
    goods = "goods"
    cotton = "cotton"
    pottery = "pottery"
    all = "all"
    blank = "blank"