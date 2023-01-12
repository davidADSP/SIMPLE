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
        self.isBuilt = False
        self.towns = []

    """
    addTown
    game init use only

    :param town: town
    """

    def addTown(self, town):
        self.towns.append(town)
