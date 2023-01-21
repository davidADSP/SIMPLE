from enum import Enum


class CardType(Enum):
    location = "location"
    industry = "industry"


class CardName(Enum):
    iron_works = "iron_works"
    coal_mine = "coal_mine"
    brewery = "brewery"
    pottery = "pottery"
    man_goods_or_cotton = "man_goods_or_cotton"
    wild_location = "wild_location"
    wild_industry = "wild_industry"
