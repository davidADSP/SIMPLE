from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

import copy

from classes.hand import Hand
from classes.roads.canal import Canal
from consts import (
    BUILDINGS,
    CANAL_PRICE,
    ONE_RAILROAD_COAL_PRICE,
    ONE_RAILROAD_PRICE,
    STARTING_MONEY,
    STARTING_ROADS,
    TWO_RAILROAD_BEER_PRICE,
    TWO_RAILROAD_COAL_PRICE,
    TWO_RAILROAD_PRICE,
)
from python.id import id

from .build_location import BuildLocation
from .buildings.building import Building
from .road_location import RoadLocation


class Player:
    def __init__(self, name: str, board: Board):
        self.id = id()
        self.name = name
        self.board = board
        self.hand = Hand(self.board.deck)
        self.money = STARTING_MONEY
        self.income = 0
        self.victoryPoints = 0
        self.spentThisTurn = 0
        self.buildings = copy.deepcopy(
            BUILDINGS
        )  # buildings, array of Building objects
        for building in self.buildings:
            building.addOwner(self)

        self.roads = [
            Canal(self) for x in range(STARTING_ROADS)
        ]  # canals/railroads, array of Road objects
        self.board.addPlayer(self)

    def canAffordBuildingIndustryResources(
        self, buildLocation: BuildLocation, coalCost: int, ironCost: int
    ) -> bool:
        return (
            self.board.isCoalAvailableFromBuildings(buildLocation.town)
            or self.board.isCoalAvailableFromTradePosts(
                buildLocation.town, coalCost, self.money
            )
        ) and (
            self.board.isIronAvailableFromBuildings()
            or self.board.isIronAvailableFromTradePosts(ironCost, self.money)
        )

    def canAffordBuilding(self, building: Building) -> bool:
        return self.money >= building.cost

    def canPlaceBuilding(
        self, building: Building, buildLocation: BuildLocation
    ) -> bool:
        return buildLocation.isPossibleBuild(building)

    def totalBuildingCost(
        self, building: Building, coalCost: int, ironCost: int
    ) -> int:
        return (
            building.cost
            + coalCost
            * self.board.coalMarketPrice  # TODO Fix this (price is dependent)
            + ironCost * self.board.ironMarketPrice  # TODO Fix this
        )

    def canAffordCanal(self) -> bool:
        return self.money >= CANAL_PRICE

    def canPlaceCanal(self, roadLocation: RoadLocation) -> bool:
        return not roadLocation.isBuilt and roadLocation.canBuildCanal

    def canAffordOneRailroadIndustryResources(self) -> bool:
        return self.board.getAvailableCoalAmount() >= ONE_RAILROAD_COAL_PRICE
        # return self.board.isCoalAvailableFromBuildings(roadLocation.town) or self.board.isCoalAvailableFromTradePosts(roadLocation.town, ONE_RAILROAD_COAL_PRICE, self.money)

    def canAffordOneRailroad(self) -> bool:
        return self.money >= ONE_RAILROAD_PRICE

    def canPlaceOneRailroad(self, roadLocation: RoadLocation) -> bool:
        return not roadLocation.isBuilt and roadLocation.canBuildRailroad

    def canAffordTwoRailroadIndustryResources(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation
    ) -> bool:
        # todo - or for now, but may be incorrect
        return (
            self.board.getAvailableCoalAmount(roadLocation1) >= TWO_RAILROAD_COAL_PRICE
            and self.board.getAvailableBeerAmount(self, roadLocation2)
            >= TWO_RAILROAD_BEER_PRICE
            or self.board.getAvailableCoalAmount(roadLocation2)
            >= TWO_RAILROAD_COAL_PRICE
            and self.board.getAvailableBeerAmount(self, roadLocation2)
            >= TWO_RAILROAD_BEER_PRICE
        )

        # return (self.board.isCoalAvailableFromBuildings(roadLocation1.town) or self.board.isCoalAvailableFromTradePosts(roadLocation1.town, TWO_RAILROAD_COAL_PRICE, self.money)) and (self.board.isBeerAvailableFromBuildings(roadLocation1.town) or self.board.isBeerAvailableFromTradePosts(roadLocation1.town))\
        #         or\
        #         (self.board.isCoalAvailableFromBuildings(roadLocation2.town) or self.board.isCoalAvailableFromTradePosts(roadLocation2.town, TWO_RAILROAD_COAL_PRICE, self.money)) and (self.board.isBeerAvailableFromBuildings(roadLocation2.town) or self.board.isBeerAvailableFromTradePosts(roadLocation1.town))

    def canAffordTwoRailroads(self) -> bool:
        return self.money >= TWO_RAILROAD_PRICE

    def canPlaceTwoRailroads(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation
    ) -> bool:
        return self.canPlaceOneRailroad(roadLocation1) and self.canPlaceOneRailroad(
            roadLocation2
        )

    def canAffordSellBuilding(self, building: Building) -> bool:
        return building.beerCost <= self.board.getAvailableBeerAmount(
            self, building.town
        )

    """Possible Actions
    probably useful to separate into canX and doX functions for generating state and possible action array (?)"""
    # 1 BUILD
    def canBuildBuilding(
        self, building: Building, buildLocation: BuildLocation
    ) -> bool:
        return (
            self.canAffordBuildingIndustryResources(
                buildLocation, building.coalCost, building.ironCost
            )
            and self.canAffordBuilding(building)
            and self.canPlaceBuilding(building, buildLocation)
            and building.owner == self
        )

    # 2 NETWORK
    def canBuildCanal(self, roadLocation: RoadLocation) -> bool:
        return self.canAffordCanal() and self.canPlaceCanal(roadLocation)

    def canBuildOneRailroad(self, roadLocation: RoadLocation) -> bool:
        return (
            self.canAffordOneRailroad()
            and self.canPlaceOneRailroad(roadLocation)
            and self.canAffordOneRailroadIndustryResources()
        )

    def canBuildTwoRailroads(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation
    ) -> bool:
        return (
            self.canAffordTwoRailroads()
            and self.canAffordTwoRailroadIndustryResources(roadLocation1, roadLocation2)
            and self.canPlaceTwoRailroads(roadLocation1, roadLocation2)
        )

    # 3 DEVELOP
    def canDevelop(self, building1: Building, building2: Building) -> bool:
        return (
            not building1.isActive
            and not building1.isRetired
            and building1.canBeDeveloped
            and building1.owner == self
            and not building2.isActive
            and not building2.isRetired
            and building2.canBeDeveloped
            and building2.owner == self
        )

    # 4 SELL
    def canSell(self, building: Building, buildLocation: BuildLocation) -> bool:
        return (
            building.isActive
            and building.owner == self
            and self.canAffordSellBuilding(building)
            and buildLocation.building
        )

    # 5 LOAN
    # is there a limit to the amount of loans you can take out? minimum income? prob not

    # 6 SCOUT
    def canScout(self) -> bool:
        return (
            len(self.board.wildBuildingDeck) > 0
            and len(self.board.wildLocationDeck) > 0
        )

    """Actions"""
    # todo player discarding for actions
    # 1 BUILD
    def buildBuilding(self, building: Building, buildLocation: BuildLocation):
        assert self.canBuildBuilding(building, buildLocation)
        building.build(buildLocation)
        self.board.buildBuilding(building, buildLocation, self)

    # 2 NETWORK
    def buildCanal(self, roadLocation: RoadLocation):
        assert self.canBuildCanal(roadLocation)
        self.board.buildCanal(roadLocation, self)

    def buildOneRailroad(self, roadLocation: RoadLocation):
        assert self.canBuildOneRailroad(roadLocation)
        self.board.buildOneRailroad(roadLocation, self)

    def buildTwoRailroads(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation
    ):
        assert self.canBuildTwoRailroads(roadLocation1, roadLocation2)
        self.board.buildTwoRailroads(roadLocation1, roadLocation2, self)

    # 3 DEVELOP
    def develop(self, building1: Building, building2: Building):
        assert self.canDevelop(building1, building2)
        building1.isRetired = True
        building2.isRetired = True

    # 4 SELL
    def sell(self, building: Building, buildLocation: BuildLocation):
        assert self.canSell(building)
        self.board.sellBuilding(building, buildLocation, self)

    # 5 LOAN
    def loan(self):
        self.income -= 3
        self.money += 30

    # 6 SCOUT
    def scout(self):
        assert self.canScout()
        # todo add wilds to player hand
        self.hand.add(self.board.wildBuildingDeck.draw())
        self.hand.add(self.board.wildLocationDeck.draw())

    def __repr__(self) -> str:
        return self.name
