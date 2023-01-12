from ..python.id import id


class BuildLocation:
    """
    BuildLocation - Town may have multiple build locations

    :param possibleBuilds: possible buildings which can be built, any array of [cotton, beer, coal, oil, pot, goods]
    :param town: town
    """

    def __init__(self, possibleBuilds):
        self.id = id()
        self.possibleBuilds = possibleBuilds
        self.building = None

    """
    addTown
    game init use only

    :param town: town
    """

    def addTown(self, town):
        self.town = town

    def addBuilding(self, building):
        self.building = building

    def retireBuilding(self, building):
        self.building.isRetired = True
        self.building = None

    """
    possibleBuild
    
    :param building: building the player would like to place
    :param buildLocation: location the player would like to build on
    :return: whether player can build there (does NOT factor in cost)
    """

    def possibleBuild(self, building):
        return not self.isBuilt and building.name in self.possibleBuilds
