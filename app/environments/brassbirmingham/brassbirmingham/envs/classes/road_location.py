from typing import List, Optional

from python.id import id

from .roads.road import Road
from .town import Town
from .trade_post import TradePost


class RoadLocation:
    """
    Road Location - Where a canal or railroad may be built

    :param networks: Networks to what Towns/TradePosts road is networked to, array of Towns/TradePosts
    :param canBuildCanal=True: is river
    :param canBuildRailroad=True: is railroad track
    """

    def __init__(
        self,
        networks: List[Town | TradePost],
        canBuildCanal=True,
        canBuildRailroad=True,
    ):
        self.id = id()
        self.networks = networks
        self.canBuildCanal = canBuildCanal
        self.canBuildRailroad = canBuildRailroad
        self.road: Optional[Road] = None
        self.isBuilt = False
        self.towns: List[Town] = []

    """
    addTown
    game init use only

    :param town: town
    """

    def addTown(self, town: Town):
        self.towns.append(town)

    def build(self, road: Road):
        self.road = road
        self.isBuilt = True

    def __str__(self) -> str:
        if len(self.towns) == 3:
            return f"{self.towns[0]} =={self.towns[1]}=={self.towns[2]}====3NETWORK"
        if len(self.towns) == 2:
            return f"{self.towns[0]} ==NETWORK=={self.towns[1]}"
        else:
            return str(self.towns)

    def __repr__(self) -> str:
        return str(self)
