from enum import Enum


class BuildingName(Enum):
    goods = "goods"
    cotton = ("cotton",)
    pottery = "pottery"
    oil = "oil"
    coal = "coal"
    beer = "beer"
    iron = "iron"


class BuildingType(Enum):
    industry = "industry"
    market = "market"
