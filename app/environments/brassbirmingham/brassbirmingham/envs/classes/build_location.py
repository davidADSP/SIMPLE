from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from python.id import id

from .buildings.building import Building
from .buildings.enums import BuildingName

if TYPE_CHECKING:
    from .town import Town


class BuildLocation:
    """
    BuildLocation - Town may have multiple build locations

    :param possibleBuilds: possible buildings which can be built, any array of [cotton, beer, coal, oil, pot, goods]
    :param town: town
    """

    def __init__(self, possibleBuilds: List[BuildingName]):
        self.id = id()
        self.possibleBuilds = possibleBuilds
        self.building: Optional[Building] = None

    """
    addTown
    game init use only

    :param town: town
    """

    def addTown(self, town: Town):
        self.town = town

    def addBuilding(self, building: Building):
        self.building = building

    def retireBuilding(self):
        self.building = None

    """
    isPossibleBuild
    
    :param building: building the player would like to place
    :param buildLocation: location the player would like to build on
    :return: whether player can build there (does NOT factor in cost)
    """

    def isPossibleBuild(self, building: Building):
        return not self.building and building.name in self.possibleBuilds

    def __str__(self) -> str:
        returnStr = "BuildingTile:|"
        for possibleBuild in self.possibleBuilds:
            returnStr += f"{possibleBuild} "
        return returnStr + "|"

    def __repr__(self) -> str:
        return str(self)
