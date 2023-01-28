from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

import copy
import math

from classes.buildings.enums import BuildingType
from classes.cards.card import Card
from classes.cards.enums import CardName
from classes.enums import Era
from classes.cards.industry_card import IndustryCard
from classes.cards.location_card import LocationCard
from classes.hand import Hand
from consts import (BUILDINGS, CANAL_PRICE, ONE_RAILROAD_COAL_PRICE,
                    ONE_RAILROAD_PRICE, STARTING_MONEY,
                    STARTING_ROADS, TWO_RAILROAD_BEER_PRICE,
                    TWO_RAILROAD_COAL_PRICE, TWO_RAILROAD_PRICE)
from python.id import id

from .build_location import BuildLocation
from .buildings.building import Building
from .buildings.market_building import MarketBuilding
from .road_location import RoadLocation


class Player:
    def __init__(self, name: str, board: Board):
        self.id = id()
        self.name = name
        self.board = board
        self.hand = Hand(self.board.deck)
        self.money = STARTING_MONEY
        self.income = 10
        self.victoryPoints = 0
        self.spentThisTurn = 0
        self.buildings = copy.deepcopy(
            BUILDINGS
        )  # buildings, array of Building objects
        for building in self.buildings:
            building.addOwner(self)

        self.roadCount = STARTING_ROADS
        self.board.addPlayer(self)

    def incomeLevel(self):
        if self.income <= 10:
            return self.income - 10
        if self.income <= 30:
            return math.ceil((self.income - 10) / 2)
        if self.income <= 60:
            return math.ceil(self.income / 3)
        if self.income <= 96:
            return 20 + math.ceil((self.income - 60) / 4)
        return 30

    def decreaseIncomeLevel(self, levels: int):
        def decreaseLevel():
            if self.income <= 11:
                self.income -= 1
            elif self.income == 12:
                self.income -= 2
            elif self.income <= 32:
                self.income -= 3 - (self.income % 2)
            elif self.income == 33:
                self.income -= 4
            elif self.income <= 63:
                self.income -= (
                    3 if self.income % 3 == 1 else 4 if self.income % 3 == 2 else 5
                )
            elif self.income == 64:
                self.income -= 6
            elif self.income <= 96:
                self.income -= (
                    4
                    if self.income % 4 == 1
                    else 5
                    if self.income % 4 == 2
                    else 6
                    if self.income % 4 == 3
                    else 7
                )
            else:
                self.income = 93
            self.income = max(self.income, 0)

        for _ in range(levels):
            decreaseLevel()

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
        if building.onlyPhaseOne and self.board.era != Era.canal:
            return False
        if building.onlyPhaseTwo and self.board.era != Era.railroad:
            return False

        return buildLocation.isPossibleBuild(building)

    def totalBuildingCost(
        self, building: Building, coalCost: int, ironCost: int
    ) -> int:
        return (
            building.cost
            + self.board.priceForCoal(coalCost)
            + self.board.priceForIron(ironCost)
        )

    def canAffordCanal(self) -> bool:
        return self.money >= CANAL_PRICE

    def canPlaceCanal(self, roadLocation: RoadLocation) -> bool:
        return self.board.era == Era.canal and not roadLocation.isBuilt and roadLocation.canBuildCanal

    def canAffordOneRailroadIndustryResources(self) -> bool:
        return self.board.getAvailableCoalAmount() >= ONE_RAILROAD_COAL_PRICE
        # return self.board.isCoalAvailableFromBuildings(roadLocation.town) or self.board.isCoalAvailableFromTradePosts(roadLocation.town, ONE_RAILROAD_COAL_PRICE, self.money)

    def canAffordOneRailroad(self) -> bool:
        return self.money >= ONE_RAILROAD_PRICE

    def canPlaceOneRailroad(self, roadLocation: RoadLocation) -> bool:
        return self.board.era == Era.railroad and not roadLocation.isBuilt and roadLocation.canBuildRailroad

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

    def canAffordSellBuilding(self, building: MarketBuilding) -> bool:
        assert building.type == BuildingType.market
        return building.beerCost <= self.board.getAvailableBeerAmount(
            self, building.town
        )

    """Possible Actions
    probably useful to separate into canX and doX functions for generating state and possible action array (?)"""
    # 1 BUILD
    def canBuildBuilding(
        self, building: Building, buildLocation: BuildLocation
    ) -> bool:

        if self.board.era == Era.canal:
            # You may have a maximum of 1 Industry tile per location in Canal era
            for buildLocation_ in buildLocation.town.buildLocations:
                if buildLocation_.id != buildLocation.id:
                    if buildLocation_.building and buildLocation_.building.owner.id == self.id:
                        return False

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
        return (
            self.roadCount > 0
            and self.canAffordCanal()
            and self.canPlaceCanal(roadLocation)
        )

    def canBuildOneRailroad(self, roadLocation: RoadLocation) -> bool:
        return (
            self.roadCount > 0
            and self.canAffordOneRailroad()
            and self.canPlaceOneRailroad(roadLocation)
            and self.canAffordOneRailroadIndustryResources()
        )

    def canBuildTwoRailroads(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation
    ) -> bool:
        return (
            self.roadCount > 1
            and self.canAffordTwoRailroads()
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
    def canSell(self, building: MarketBuilding) -> bool:
        return (
            building.isActive
            and building.owner == self
            and self.canAffordSellBuilding(building)
        )

    # 5 LOAN
    def canLoan(self) -> bool:
        return self.income >= 3

    # 6 SCOUT
    def canScout(self, additionalDiscard: Card) -> bool:
        ownership = False
        for card in self.hand.cards:
            if card.name in [CardName.wild_location, CardName.wild_industry]:
                # No scouting if player has at least 1 wild card already
                return False
            if card.id == additionalDiscard.id:
                ownership = True

        return ownership

    # 7 PASS
    def canPassTurn(self) -> bool:
        return True

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
    def sell(self, building: MarketBuilding):
        assert self.canSell(building)
        self.board.sellBuilding(building, self)

    # 5 LOAN
    def loan(self):
        assert self.canLoan()
        self.decreaseIncomeLevel(3)
        self.money += 30

    # 6 SCOUT
    def scout(self, additionalDiscard: Card):
        assert self.canScout(additionalDiscard)
        self.hand.add(LocationCard(name=CardName.wild_location))
        self.hand.add(IndustryCard(name=CardName.wild_industry))
        self.hand.spendCard(additionalDiscard)

    # 7 PASS
    def passTurn(self):
        assert self.canPassTurn()
        return

    def __repr__(self) -> str:
        return self.name
