from typing import Dict, List

from classes.build_location import BuildLocation
from classes.buildings.building import Building
from classes.buildings.enums import BuildingName, MerchantName
from classes.buildings.industry_building import IndustryBuilding
from classes.buildings.market_building import MarketBuilding
from classes.cards.card import Card
from classes.cards.enums import CardName
from classes.cards.industry_card import IndustryCard
from classes.cards.location_card import LocationCard
from classes.road_location import RoadLocation
from classes.town import Town
from classes.trade_post import TradePost

STARTING_ROADS = 14
STARTING_MONEY = 17
CANAL_PRICE = 3
ONE_RAILROAD_PRICE = 5
ONE_RAILROAD_COAL_PRICE = 1
TWO_RAILROAD_PRICE = 15
TWO_RAILROAD_COAL_PRICE = 2
TWO_RAILROAD_BEER_PRICE = 1
MAX_MARKET_COAL = 14
MAX_MARKET_IRON = 10
# TOTAL_COAL = 30
# TOTAL_IRON = 18
# TOTAL_BEER = 15
# amt of tokens doesn't matter actually


# towns
LEEK = "Leek"
STOKE_ON_TRENT = "Stoke-On-Trent"
STONE = "Stone"
CANNOCK = "Cannock"
UTTOXETER = "Uttoxeter"
BELPER = "Belper"
DERBY = "Derby"
STAFFORD = "Stafford"
BURTON_UPON_TRENT = "Burton-Upon-Trent"
BEER1 = "beer1"
TAMWORTH = "Tamworth"
WALSALL = "Walsall"
DUDLEY = "Dudley"
WORCESTER = "Worcester"
COALBROOKDALE = "Coalbrookdale"
WOLVERHAMPTON = "Wolverhampton"
KIDDERMINSTER = "Kidderminster"
BEER2 = "beer2"
BIRMINGHAM = "Birmingham"
NUNEATON = "Nuneaton"
COVENTRY = "Coventry"
REDDITCH = "Redditch"

# trade posts
WARRINGTON = "Warrington"
NOTTINGHAM = "Nottingham"
SHREWBURY = "Shrewbury"
OXFORD = "Oxford"
GLOUCESTER = "Gloucester"

# merchant tiles
MERCHANT_TILES = {
    "2": [
        MerchantName.all,
        MerchantName.blank,
        MerchantName.blank,
        MerchantName.cotton,
        MerchantName.goods,
    ],
    "3": [
        MerchantName.all,
        MerchantName.blank,
        MerchantName.blank,
        MerchantName.blank,
        MerchantName.cotton,
        MerchantName.pottery,
        MerchantName.goods,
    ],
    "4": [
        MerchantName.all,
        MerchantName.blank,
        MerchantName.blank,
        MerchantName.blank,
        MerchantName.cotton,
        MerchantName.cotton,
        MerchantName.pottery,
        MerchantName.goods,
        MerchantName.goods,
    ]
}

TOWNS: List[Town] = [
    Town(
        "blue",
        LEEK,
        [
            BuildLocation([BuildingName.cotton, BuildingName.goods]),
            BuildLocation([BuildingName.cotton, BuildingName.coal]),
        ],
    ),
    Town(
        "blue",
        STOKE_ON_TRENT,
        [
            BuildLocation([BuildingName.cotton, BuildingName.goods]),
            BuildLocation([BuildingName.pottery, BuildingName.iron]),
            BuildLocation([BuildingName.goods]),
        ],
    ),
    Town(
        "blue",
        STONE,
        [
            BuildLocation([BuildingName.cotton, BuildingName.beer]),
            BuildLocation([BuildingName.goods, BuildingName.coal]),
        ],
    ),
    Town(
        "blue",
        UTTOXETER,
        [
            BuildLocation([BuildingName.goods, BuildingName.beer]),
            BuildLocation([BuildingName.cotton, BuildingName.beer]),
        ],
    ),
    Town(
        "green",
        BELPER,
        [
            BuildLocation([BuildingName.cotton, BuildingName.goods]),
            BuildLocation([BuildingName.coal]),
            BuildLocation([BuildingName.pottery]),
        ],
    ),
    Town(
        "green",
        DERBY,
        [
            BuildLocation([BuildingName.cotton, BuildingName.beer]),
            BuildLocation([BuildingName.cotton, BuildingName.goods]),
            BuildLocation([BuildingName.iron]),
        ],
    ),
    Town(
        "red",
        STAFFORD,
        [
            BuildLocation([BuildingName.goods, BuildingName.beer]),
            BuildLocation([BuildingName.pottery]),
        ],
    ),
    Town(
        "red",
        BURTON_UPON_TRENT,
        [
            BuildLocation([BuildingName.goods, BuildingName.coal]),
            BuildLocation([BuildingName.beer]),
        ],
    ),
    Town(BEER1, BEER1, [BuildLocation([BuildingName.beer])]),
    Town(
        "red",
        "Cannock",
        [
            BuildLocation([BuildingName.goods, BuildingName.coal]),
            BuildLocation([BuildingName.coal]),
        ],
    ),
    Town(
        "red",
        TAMWORTH,
        [
            BuildLocation([BuildingName.cotton, BuildingName.coal]),
            BuildLocation([BuildingName.cotton, BuildingName.coal]),
        ],
    ),
    Town(
        "red",
        WALSALL,
        [
            BuildLocation([BuildingName.iron, BuildingName.goods]),
            BuildLocation([BuildingName.goods, BuildingName.beer]),
        ],
    ),
    Town(
        "yellow",
        COALBROOKDALE,
        [
            BuildLocation([BuildingName.iron, BuildingName.beer]),
            BuildLocation([BuildingName.iron]),
            BuildLocation([BuildingName.coal]),
        ],
    ),
    Town(
        "yellow",
        WOLVERHAMPTON,
        [
            BuildLocation([BuildingName.goods]),
            BuildLocation([BuildingName.goods, BuildingName.coal]),
        ],
    ),
    Town(
        "yellow",
        DUDLEY,
        [BuildLocation([BuildingName.coal]), BuildLocation([BuildingName.iron])],
    ),
    Town(
        "yellow",
        KIDDERMINSTER,
        [
            BuildLocation([BuildingName.cotton, BuildingName.coal]),
            BuildLocation([BuildingName.cotton]),
        ],
    ),
    Town(BEER2, BEER2, [BuildLocation([BuildingName.beer])]),
    Town(
        "yellow",
        WORCESTER,
        [BuildLocation([BuildingName.cotton]), BuildLocation([BuildingName.cotton])],
    ),
    Town(
        "purple",
        BIRMINGHAM,
        [
            BuildLocation([BuildingName.cotton, BuildingName.goods]),
            BuildLocation([BuildingName.goods]),
            BuildLocation([BuildingName.iron]),
            BuildLocation([BuildingName.goods]),
        ],
    ),
    Town(
        "purple",
        NUNEATON,
        [
            BuildLocation([BuildingName.goods, BuildingName.beer]),
            BuildLocation([BuildingName.cotton, BuildingName.coal]),
        ],
    ),
    Town(
        "purple",
        COVENTRY,
        [
            BuildLocation([BuildingName.pottery]),
            BuildLocation([BuildingName.goods, BuildingName.coal]),
            BuildLocation([BuildingName.iron, BuildingName.goods]),
        ],
    ),
    Town(
        "purple",
        REDDITCH,
        [
            BuildLocation([BuildingName.goods, BuildingName.coal]),
            BuildLocation([BuildingName.iron]),
        ],
    ),
]


TRADEPOSTS: Dict[int, List[TradePost]] = {
    "2": [
        TradePost(SHREWBURY, 1, 0, 4, 0, 2, False),
        TradePost(OXFORD, 2, 0, 0, 2, 2, False),
        TradePost(GLOUCESTER, 2, 0, 0, 2, 2, True),
    ],
    "3": [
        TradePost(SHREWBURY, 1, 0, 4, 0, 2, False),
        TradePost(OXFORD, 2, 0, 0, 2, 2, False),
        TradePost(GLOUCESTER, 2, 0, 0, 2, 2, True),
        TradePost(WARRINGTON, 2, 5, 0, 0, 2, False),
    ],
    "4": [
        TradePost(SHREWBURY, 1, 0, 4, 0, 2, False),
        TradePost(OXFORD, 2, 0, 0, 2, 2, False),
        TradePost(GLOUCESTER, 2, 0, 0, 2, 2, True),
        TradePost(WARRINGTON, 2, 5, 0, 0, 2, False),
        TradePost(NOTTINGHAM, 2, 0, 3, 0, 2, False),
    ]
}


# TRADEPOSTS: List[TradePost] = [
#     TradePost(WARRINGTON, 2, 3, 5, 0, 0, 2, False),
#     TradePost(NOTTINGHAM, 2, 4, 0, 3, 0, 2, False),
#     TradePost(SHREWBURY, 1, 2, 0, 4, 0, 2, False),
#     TradePost(OXFORD, 2, 2, 0, 0, 2, 2, False),
#     TradePost(GLOUCESTER, 2, 2, 0, 0, 2, 2, True),
# ]

ROAD_LOCATIONS: List[RoadLocation] = [
    RoadLocation([WARRINGTON, STOKE_ON_TRENT]),
    RoadLocation([STOKE_ON_TRENT, LEEK]),
    RoadLocation([LEEK, BELPER], False),
    RoadLocation([BELPER, DERBY]),
    RoadLocation([DERBY, NOTTINGHAM]),
    RoadLocation([DERBY, UTTOXETER], False),
    RoadLocation([DERBY, BURTON_UPON_TRENT]),
    RoadLocation([STOKE_ON_TRENT, STONE]),
    RoadLocation([STONE, UTTOXETER], False),
    RoadLocation([STONE, STAFFORD]),
    RoadLocation([STONE, BURTON_UPON_TRENT]),
    RoadLocation([STAFFORD, CANNOCK]),
    RoadLocation([CANNOCK, BURTON_UPON_TRENT], False),
    RoadLocation([TAMWORTH, BURTON_UPON_TRENT]),
    RoadLocation([WALSALL, BURTON_UPON_TRENT], canBuildRailroad=False),
    RoadLocation([BEER1, CANNOCK]),
    RoadLocation([WOLVERHAMPTON, CANNOCK]),
    RoadLocation([WALSALL, CANNOCK]),
    RoadLocation([WOLVERHAMPTON, COALBROOKDALE]),
    RoadLocation([SHREWBURY, COALBROOKDALE]),
    RoadLocation([KIDDERMINSTER, COALBROOKDALE]),
    RoadLocation([KIDDERMINSTER, DUDLEY]),
    RoadLocation([WOLVERHAMPTON, WALSALL]),
    RoadLocation([WOLVERHAMPTON, DUDLEY]),
    RoadLocation([TAMWORTH, WALSALL], False),
    RoadLocation([TAMWORTH, NUNEATON]),
    RoadLocation([NUNEATON, COVENTRY]),
    RoadLocation([BIRMINGHAM, WALSALL]),
    RoadLocation([BIRMINGHAM, TAMWORTH]),
    RoadLocation([BIRMINGHAM, NUNEATON], False),
    RoadLocation([BIRMINGHAM, COVENTRY]),
    RoadLocation([BIRMINGHAM, OXFORD]),
    RoadLocation([BIRMINGHAM, REDDITCH], False),
    RoadLocation([BIRMINGHAM, WORCESTER]),
    RoadLocation([BIRMINGHAM, DUDLEY]),
    RoadLocation([REDDITCH, OXFORD]),
    RoadLocation([REDDITCH, GLOUCESTER]),
    RoadLocation([WORCESTER, GLOUCESTER]),
    RoadLocation([WORCESTER, BEER2, KIDDERMINSTER]),
]

BUILDINGS: List[Building] = [
    MarketBuilding(BuildingName.goods, 1, 8, 1, 0, 1, 3, 5, 2, onlyPhaseOne=True),
    MarketBuilding(BuildingName.goods, 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(BuildingName.goods, 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(BuildingName.goods, 3, 12, 2, 0, 0, 4, 4, 0),
    MarketBuilding(BuildingName.goods, 4, 8, 0, 1, 1, 3, 6, 1),
    MarketBuilding(BuildingName.goods, 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(BuildingName.goods, 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(BuildingName.goods, 6, 20, 0, 0, 1, 7, 6, 1),
    MarketBuilding(BuildingName.goods, 7, 16, 1, 1, 0, 9, 4, 0),
    MarketBuilding(BuildingName.goods, 8, 20, 0, 2, 1, 11, 1, 1),
    MarketBuilding(BuildingName.cotton, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(BuildingName.cotton, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(BuildingName.cotton, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(BuildingName.cotton, 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(BuildingName.cotton, 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(BuildingName.cotton, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(BuildingName.cotton, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(BuildingName.cotton, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(BuildingName.cotton, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(BuildingName.cotton, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(BuildingName.cotton, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(
        BuildingName.pottery, 1, 17, 0, 1, 1, 10, 5, 1, canBeDeveloped=False
    ),
    MarketBuilding(BuildingName.pottery, 2, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(
        BuildingName.pottery, 3, 22, 2, 0, 2, 11, 5, 1, canBeDeveloped=False
    ),
    MarketBuilding(BuildingName.pottery, 4, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(BuildingName.pottery, 5, 24, 2, 0, 2, 20, 5, 1, onlyPhaseTwo=True),
    IndustryBuilding(BuildingName.iron, 1, 4, 5, 1, 0, 3, 3, 1, onlyPhaseOne=True),
    IndustryBuilding(BuildingName.iron, 2, 4, 7, 1, 0, 5, 3, 1),
    IndustryBuilding(BuildingName.iron, 3, 5, 9, 1, 0, 7, 2, 1),
    IndustryBuilding(BuildingName.iron, 4, 6, 12, 1, 0, 9, 1, 1),
    IndustryBuilding(BuildingName.beer, 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(BuildingName.beer, 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(
        BuildingName.beer, 2, 1, 7, 0, 1, 5, 5, 2
    ),  # add logic somewhere to add +1 beer to tier ^2 in second phase
    IndustryBuilding(BuildingName.beer, 2, 1, 7, 0, 1, 5, 5, 2),
    IndustryBuilding(BuildingName.beer, 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(BuildingName.beer, 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(BuildingName.beer, 4, 1, 9, 0, 1, 10, 5, 2),
    IndustryBuilding(BuildingName.coal, 1, 2, 5, 0, 0, 1, 4, 2, onlyPhaseOne=True),
    IndustryBuilding(BuildingName.coal, 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(BuildingName.coal, 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(BuildingName.coal, 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(BuildingName.coal, 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(BuildingName.coal, 4, 5, 10, 0, 1, 4, 5, 1),
    IndustryBuilding(BuildingName.coal, 4, 5, 10, 0, 1, 4, 5, 1),
]

"""
Starting deck

Key is (str) amount of players playing
"""
STARTING_CARDS: Dict[str, List[Card]] = {
    "2": [
        LocationCard(STAFFORD),
        LocationCard(STAFFORD),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(CANNOCK),
        LocationCard(CANNOCK),
        LocationCard(TAMWORTH),
        LocationCard(WALSALL),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(DUDLEY),
        LocationCard(DUDLEY),
        LocationCard(KIDDERMINSTER),
        LocationCard(KIDDERMINSTER),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WORCESTER),
        LocationCard(WORCESTER),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(NUNEATON),
        LocationCard(REDDITCH),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
    ],
    "3": [
        LocationCard(LEEK),
        LocationCard(LEEK),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STONE),
        LocationCard(STONE),
        LocationCard(UTTOXETER),
        LocationCard(STAFFORD),
        LocationCard(STAFFORD),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(CANNOCK),
        LocationCard(CANNOCK),
        LocationCard(TAMWORTH),
        LocationCard(WALSALL),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(DUDLEY),
        LocationCard(DUDLEY),
        LocationCard(KIDDERMINSTER),
        LocationCard(KIDDERMINSTER),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WORCESTER),
        LocationCard(WORCESTER),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(NUNEATON),
        LocationCard(REDDITCH),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.coal_mine),
        IndustryCard(BuildingName.cotton),
        IndustryCard(BuildingName.cotton),
        IndustryCard(BuildingName.cotton),
        IndustryCard(BuildingName.cotton),
        IndustryCard(BuildingName.cotton),
        IndustryCard(BuildingName.cotton),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
    ],
    "4": [
        LocationCard(BELPER),
        LocationCard(BELPER),
        LocationCard(DERBY),
        LocationCard(DERBY),
        LocationCard(DERBY),
        LocationCard(LEEK),
        LocationCard(LEEK),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STOKE_ON_TRENT),
        LocationCard(STONE),
        LocationCard(STONE),
        LocationCard(UTTOXETER),
        LocationCard(UTTOXETER),
        LocationCard(STAFFORD),
        LocationCard(STAFFORD),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(BURTON_UPON_TRENT),
        LocationCard(CANNOCK),
        LocationCard(CANNOCK),
        LocationCard(TAMWORTH),
        LocationCard(WALSALL),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(COALBROOKDALE),
        LocationCard(DUDLEY),
        LocationCard(DUDLEY),
        LocationCard(KIDDERMINSTER),
        LocationCard(KIDDERMINSTER),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WOLVERHAMPTON),
        LocationCard(WORCESTER),
        LocationCard(WORCESTER),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(BIRMINGHAM),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(COVENTRY),
        LocationCard(NUNEATON),
        LocationCard(REDDITCH),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.iron_works),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.coal_mine),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.man_goods_or_cotton),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.pottery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
        IndustryCard(CardName.brewery),
    ],
}
