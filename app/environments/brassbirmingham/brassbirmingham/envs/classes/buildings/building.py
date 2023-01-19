from __future__ import annotations

from typing import TYPE_CHECKING

from python.id import id

if TYPE_CHECKING:
    from ..player import Player

from .enums import BuildingName, BuildingType


class Building:
    """
    Building object

    :param name: any of [goods, cotton, pottery]
    :param tier: ex: 3
    :param cost: cost
    :param coalCost: ex: 1
    :param ironCost: ironCost
    :param victoryPointsGained: victory points gained from selling
    :param incomeGained: income gained from selling
    :param networkPoints: amount of points each road gets during counting step
    :param canBeDeveloped=True:
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """

    def __init__(
        self,
        type: BuildingType,
        name: BuildingName,
        tier: int,
        cost: int,
        coalCost: int,
        ironCost: int,
        victoryPointsGained: int,
        incomeGained: int,
        networkPoints: int,
        canBeDeveloped: bool,
        onlyPhaseOne: bool,
        onlyPhaseTwo: bool,
    ):
        self.id = id()
        self.type = type
        self.name = name
        self.tier = tier
        self.cost = cost
        self.coalCost = coalCost
        self.ironCost = ironCost
        self.victoryPointsGained = victoryPointsGained
        self.incomeGained = incomeGained
        self.networkPoints = networkPoints
        self.canBeDeveloped = canBeDeveloped
        self.onlyPhaseOne = onlyPhaseOne  # can only be built during phase 1
        self.onlyPhaseTwo = onlyPhaseTwo  # can only be built during phase 2

        self.town = None
        self.isSold = False  # is sold/ran out of resources
        self.isActive = False  # is on the board i.e., not bought yet
        self.isRetired = (
            False  # only used for retired buildings (tier 1's) in second phase
        )

    """
    addOwner - add player/owner to building
    game init use only

    :param owner: player
    """

    def addOwner(self, owner: Player):
        self.owner = owner

    def build(self, buildLocation):
        self.isActive = True
        self.town = buildLocation.town

    def sell(self):
        self.isActive = False
        self.isSold = True
        # self.isRetired = True
        self.town = None

    def __repr__(self) -> str:
        return f"\nBuilding {self.tier}:{self.name}:: Owner: {self.owner}, Bought: {self.isActive}, Sold: {self.isSold} Retired: {self.isRetired}"
