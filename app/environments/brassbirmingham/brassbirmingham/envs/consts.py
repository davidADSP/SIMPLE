from classes.buildings.industry_building import IndustryBuilding
from classes.buildings.market_building import MarketBuilding
from classes.town import Town
from classes.build_location import BuildLocation
from classes.trade_post import TradePost
from classes.road_location import RoadLocation
from classes.cards.location_card import LocationCard
from classes.cards.industry_card import IndustryCard

STARTING_ROADS = 14
STARTING_MONEY = 17
CANAL_PRICE = 3
ONE_RAILROAD_PRICE = 5
ONE_RAILROAD_COAL_PRICE = 1
TWO_RAILROAD_PRICE = 15
TWO_RAILROAD_COAL_PRICE = 2
TWO_RAILROAD_BEER_PRICE = 2
# TOTAL_COAL = 30
# TOTAL_IRON = 18
# TOTAL_BEER = 15
# amt of tokens doesn't matter actually


#towns
LEEK = 'Leek'
STOKE_ON_TRENT = 'Stoke-On-Trent'
STONE = 'Stone'
CANNOCK = 'Cannock'
UTTOXETER = 'Uttoxeter'
BELPER = 'Belper'
DERBY = 'Derby'
STAFFORD = 'Stafford'
BURTON_UPON_TRENT = 'Burton-Upon-Trent'
BEER1 = 'beer1'
TAMWORTH = 'Tamworth'
WALSALL = 'Walsall'
DUDLEY = 'Dudley'
WORCESTER = 'Worcester'
COALBROOKDALE = 'Coalbrookdale'
WOLVERHAMPTON = 'Wolverhampton'
KIDDERMINSTER = 'Kidderminster'
BEER2 = 'beer2'
BIRMINGHAM = 'Birmingham'
NUNEATON = 'Nuneaton'
COVENTRY = 'Coventry'
REDDITCH = 'Redditch'

#trade posts
WARRINGTON = 'Warrington'
NOTTINGHAM = 'Nottingham'
SHREWBURY = 'Shrewbury'
OXFORD = 'Oxford'
GLOUCESTER = 'Gloucester'

#CARD NAMES
IRON_WORKS = 'Iron Works'
COAL_MINE = 'Coal Mine'
BREWERY = 'Brewery'
POTTERY = 'Pottery'
MAN_GOODS__COTTON = 'Man. Goods / Cotton Mill'

#industry
GOODS = 'goods'
OIL = 'oil'
BEER = 'beer'
COTTON = 'cotton'
# POTTERY = ''
COAL = 'coal'
IRON = 'iron'

TOWNS = [
    Town(
        "blue",
        LEEK,
        [BuildLocation([COTTON, GOODS]), BuildLocation([COTTON, COAL])],
    ),
    Town(
        "blue",
        STOKE_ON_TRENT,
        [
            BuildLocation([COTTON, GOODS]),
            BuildLocation([POTTERY, OIL]),
            BuildLocation([GOODS]),
        ],
    ),
    Town(
        "blue",
        STONE,
        [BuildLocation([COTTON, BEER]), BuildLocation([GOODS, COAL])],
    ),
    Town(
        "blue",
        UTTOXETER,
        [BuildLocation([GOODS, BEER]), BuildLocation([COTTON, BEER])],
    ),
    Town(
        "green",
        BELPER,
        [
            BuildLocation([COTTON, GOODS]),
            BuildLocation([COAL]),
            BuildLocation([POTTERY]),
        ],
    ),
    Town(
        "green",
        DERBY,
        [
            BuildLocation([COTTON, BEER]),
            BuildLocation([COTTON, GOODS]),
            BuildLocation([OIL]),
        ],
    ),
    Town(
        "red",
        STAFFORD,
        [BuildLocation([GOODS, BEER]), BuildLocation([POTTERY])],
    ),
    Town(
        "red",
        BURTON_UPON_TRENT,
        [BuildLocation([GOODS, COAL]), BuildLocation([BEER])],
    ),
    Town(BEER1, "", [BuildLocation([BEER])]),
    Town("red", "Cannock", [BuildLocation([GOODS, COAL]), BuildLocation([COAL])]),
    Town(
        "red",
        TAMWORTH,
        [BuildLocation([COTTON, COAL]), BuildLocation([COTTON, COAL])],
    ),
    Town(
        "red",
        WALSALL,
        [BuildLocation([OIL, GOODS]), BuildLocation([GOODS, BEER])],
    ),
    Town(
        "yellow",
        COALBROOKDALE,
        [
            BuildLocation([OIL, BEER]),
            BuildLocation([OIL]),
            BuildLocation([COAL]),
        ],
    ),
    Town(
        "yellow",
        WOLVERHAMPTON,
        [BuildLocation([GOODS]), BuildLocation([GOODS, COAL])],
    ),
    Town("yellow", DUDLEY, [BuildLocation([COAL]), BuildLocation([OIL])]),
    Town(
        "yellow",
        KIDDERMINSTER,
        [BuildLocation([COTTON, COAL]), BuildLocation([COTTON])],
    ),
    Town(BEER2, "", [BuildLocation([BEER])]),
    Town("yellow", WORCESTER, [BuildLocation([COTTON]), BuildLocation([COTTON])]),
    Town(
        "purple",
        BIRMINGHAM,
        [
            BuildLocation([COTTON, GOODS]),
            BuildLocation([GOODS]),
            BuildLocation([OIL]),
            BuildLocation([GOODS]),
        ],
    ),
    Town(
        "purple",
        NUNEATON,
        [BuildLocation([GOODS, BEER]), BuildLocation([COTTON, COAL])],
    ),
    Town(
        "purple",
        COVENTRY,
        [
            BuildLocation([POTTERY]),
            BuildLocation([GOODS, COAL]),
            BuildLocation([OIL, GOODS]),
        ],
    ),
    Town(
        "purple", REDDITCH, [BuildLocation([GOODS, COAL]), BuildLocation([OIL])]
    ),
]

TRADEPOSTS = [
    TradePost(WARRINGTON, 2, 5, 0, 0, 2, False),
    TradePost(NOTTINGHAM, 2, 0, 3, 0, 2, False),
    TradePost(SHREWBURY, 1, 0, 4, 0, 2, False),
    TradePost(OXFORD, 2, 0, 0, 2, 2, False),
    TradePost(GLOUCESTER, 2, 0, 0, 2, 2, True),
]

ROAD_LOCATIONS = [
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
    RoadLocation([NUNEATON, WALSALL]),
    RoadLocation([NUNEATON, COVENTRY]),
    RoadLocation([CANNOCK, WALSALL]),
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

BUILDINGS = [
    MarketBuilding(GOODS, 1, 8, 1, 0, 1, 3, 5, 2, onlyPhaseOne=True),
    MarketBuilding(GOODS, 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(GOODS, 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(GOODS, 3, 12, 2, 0, 0, 4, 4, 0),
    MarketBuilding(GOODS, 4, 8, 0, 1, 1, 3, 6, 1),
    MarketBuilding(GOODS, 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(GOODS, 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(GOODS, 6, 20, 0, 0, 1, 7, 6, 1),
    MarketBuilding(GOODS, 7, 16, 1, 1, 0, 9, 4, 0),
    MarketBuilding(GOODS, 8, 20, 0, 2, 1, 11, 1, 1),
    MarketBuilding(COTTON, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(COTTON, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(COTTON, 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(COTTON, 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(COTTON, 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(COTTON, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(COTTON, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(COTTON, 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(COTTON, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(COTTON, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(COTTON, 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(POTTERY, 1, 17, 0, 1, 1, 10, 5, 1, canBeDeveloped=False),
    MarketBuilding(POTTERY, 2, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(POTTERY, 3, 22, 2, 0, 2, 11, 5, 1, canBeDeveloped=False),
    MarketBuilding(POTTERY, 4, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(POTTERY, 5, 24, 2, 0, 2, 20, 5, 1, onlyPhaseTwo=True),
    IndustryBuilding(OIL, 1, 4, 5, 1, 0, 3, 3, 1, onlyPhaseOne=True),
    IndustryBuilding(OIL, 2, 4, 7, 1, 0, 5, 3, 1),
    IndustryBuilding(OIL, 3, 5, 9, 1, 0, 7, 2, 1),
    IndustryBuilding(OIL, 4, 6, 12, 1, 0, 9, 1, 1),
    IndustryBuilding(BEER, 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(BEER, 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(
        BEER, 2, 1, 7, 0, 1, 5, 5, 2
    ),  # add logic somewhere to add +1 beer to tier ^2 in second phase
    IndustryBuilding(BEER, 2, 1, 7, 0, 1, 5, 5, 2),
    IndustryBuilding(BEER, 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(BEER, 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(BEER, 4, 1, 9, 0, 1, 10, 5, 2),
    IndustryBuilding(COAL, 1, 2, 5, 0, 0, 1, 4, 2, onlyPhaseOne=True),
    IndustryBuilding(COAL, 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(COAL, 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(COAL, 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(COAL, 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(COAL, 4, 5, 10, 0, 1, 4, 5, 1),
    IndustryBuilding(COAL, 4, 5, 10, 0, 1, 4, 5, 1),
]

"""
Starting deck

Key is (str) amount of players playing
"""
STARTING_CARDS = {
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
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(COAL_MINE),
        IndustryCard(COAL_MINE),
        IndustryCard(POTTERY),
        IndustryCard(POTTERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
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
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(COAL_MINE),
        IndustryCard(COAL_MINE),
        IndustryCard(COTTON),
        IndustryCard(COTTON),
        IndustryCard(COTTON),
        IndustryCard(COTTON),
        IndustryCard(COTTON),
        IndustryCard(COTTON),
        IndustryCard(POTTERY),
        IndustryCard(POTTERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
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
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(IRON_WORKS),
        IndustryCard(COAL_MINE),
        IndustryCard(COAL_MINE),
        IndustryCard(COAL_MINE),
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(MAN_GOODS__COTTON), #Manufactured goods OR Cotton
        IndustryCard(POTTERY),
        IndustryCard(POTTERY),
        IndustryCard(POTTERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
        IndustryCard(BREWERY),
    ],
}

STARTING_WILD_LOCATION_CARDS = [
    # idk how many wilds there are
    LocationCard("Wild location", True),
    LocationCard("Wild location", True),
    LocationCard("Wild location", True),
    LocationCard("Wild location", True),
    LocationCard("Wild location", True),
]

STARTING_WILD_BUILDING_CARDS = [
    IndustryCard("Wild building", True),
    IndustryCard("Wild building", True),
    IndustryCard("Wild building", True),
    IndustryCard("Wild building", True),
    IndustryCard("Wild building", True),
]
