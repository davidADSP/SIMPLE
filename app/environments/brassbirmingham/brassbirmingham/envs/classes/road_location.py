from ..python.id import id


class RoadLocation:
    """
    Road Location - Where a canal or railroad may be built

    :param networks: Networks to what Towns/TradePosts road is networked to, array of Towns/TradePosts
    :param canBuildCanal=True: is river
    :param canBuildRailroad=True: is railroad track
    """

    def __init__(self, networks, canBuildCanal=True, canBuildRailroad=True):
        self.id = id()
        self.networks = networks
        self.canBuildCanal = canBuildCanal
        self.canBuildRailroad = canBuildRailroad
        self.road = None
        self.isBuilt = False
        self.towns = []

    """
    addTown
    game init use only

    :param town: town
    """

    def addTown(self, town):
        self.towns.append(town)

    def build(self, road):
        self.road = road
        self.isBuilt = True

    def __str__(self):
        if len(self.towns) == 3:
            return f"{self.towns[0]} =={self.towns[1]}=={self.towns[2]}====3NETWORK"
        if len(self.towns) == 2:
            return f"{self.towns[0]} ==NETWORK=={self.towns[1]}"
        else:
            return str(self.towns)

    def __repr__(self):
        return str(self)
