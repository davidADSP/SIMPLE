from typing import List

from python.id import id
from python.print_colors import prLightPurple

from .road_location import RoadLocation
from .town import Town


class TradePost:
    """
    TradePost

    :param name: name
    :param beerAmount: amount of starting beer
    :param moneyGained: money gained from first trade
    :param victoryPointsGained: victory points gained from first trade
    :param incomeGained: income gained from first trade
    :param networkPoints: amount of points each road gets during counting step
    :param canDevelop: can develop after first trade
    """

    def __init__(
        self,
        name: str,
        beerAmount: int,
        moneyGained: int,
        victoryPointsGained: int,
        incomeGained: int,
        networkPoints: int,
        canDevelop: bool,
    ):
        self.id = id()
        self.type = "TradePost"
        self.name = name
        self.beerAmount = beerAmount
        self.moneyGained = moneyGained
        self.victoryPointsGained = victoryPointsGained
        self.incomeGained = incomeGained
        self.possibleTrades = []
        self.networkPoints = networkPoints
        self.canDevelop = canDevelop
        self.networks: List[RoadLocation] = []

    """
    addPossibleTrade
    game init use only
    trades which are possible to make, array of Building object names 'oil', 'goods', etc...

    :param possibleTrade: possibleTrade
    """

    def addPossibleTrade(self, possibleTrade):
        self.possibleTrades.append(possibleTrade)

    """
    addRoadLocation
    game init use only

    :param roadLocation: roadLocation
    """

    def addRoadLocation(self, roadLocation: RoadLocation):
        roadLocation.addTown(self)
        self.networks.append(roadLocation)

    def __str__(self) -> str:
        return f"TP({prLightPurple(self.name)})"
