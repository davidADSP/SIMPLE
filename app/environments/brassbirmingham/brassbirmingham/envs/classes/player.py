import copy
from python.id import id
from classes.hand import Hand
from classes.roads.canal import Canal
from consts import (
    STARTING_MONEY,
    BUILDINGS,
    STARTING_ROADS,
    CANAL_PRICE,
    ONE_RAILROAD_PRICE,
    ONE_RAILROAD_COAL_PRICE,
    TWO_RAILROAD_PRICE,
    TWO_RAILROAD_COAL_PRICE,
    TWO_RAILROAD_BEER_PRICE,
)


class Player:
    def __init__(self, name, board):
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

    def canAffordBuildingIndustryResources(self, buildLocation, coalCost, ironCost):
        return (
            self.board.isCoalAvailableFromBuildings(buildLocation.town)
            or self.board.isCoalAvailableFromTradePosts(
                buildLocation.town, coalCost, self.money
            )
        ) and (
            self.board.isIronAvailableFromBuildings()
            or self.board.isIronAvailableFromTradePosts(ironCost, self.money)
        )

    def canAffordBuilding(self, building):
        return self.money >= building.cost

    def canPlaceBuilding(self, building, buildLocation):
        return buildLocation.isPossibleBuild(building)

    def totalBuildingCost(self, building, coalCost, ironCost):
        return (
            building.cost
            + coalCost * self.board.coalMarketPrice
            + ironCost * self.board.ironMarketPrice
        )

    def canAffordCanal(self):
        return self.money >= CANAL_PRICE

    def canPlaceCanal(self, roadLocation):
        return not roadLocation.isBuilt and roadLocation.canBuildCanal

    def canAffordOneRailroadIndustryResources(self):
        return self.board.getAvailableCoalAmount() >= ONE_RAILROAD_COAL_PRICE
        # return self.board.isCoalAvailableFromBuildings(roadLocation.town) or self.board.isCoalAvailableFromTradePosts(roadLocation.town, ONE_RAILROAD_COAL_PRICE, self.money)

    def canAffordOneRailroad(self):
        return self.money >= ONE_RAILROAD_PRICE

    def canPlaceOneRailroad(self, roadLocation):
        return not roadLocation.isBuilt and roadLocation.canBuildRailroad

    def canAffordTwoRailroadIndustryResources(self, roadLocation1, roadLocation2):
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

    def canAffordTwoRailroads(self):
        return self.money >= TWO_RAILROAD_PRICE

    def canPlaceTwoRailroads(self, roadLocation1, roadLocation2):
        return self.canPlaceOneRailroad(roadLocation1) and self.canPlaceOneRailroad(
            roadLocation2
        )

    def canAffordSellBuilding(self, building):
        return building.beerCost <= self.board.getAvailableBeerAmount(
            self, building.town
        )

    """Possible Actions
    probably useful to separate into canX and doX functions for generating state and possible action array (?)"""
    # 1 BUILD
    def canBuildBuilding(self, building, buildLocation):
        return (
            self.canAffordBuildingIndustryResources(
                buildLocation, building.coalCost, building.ironCost
            )
            and self.canAffordBuilding(building)
            and self.canPlaceBuilding(building, buildLocation)
            and building.owner == self
        )

    # 2 NETWORK
    def canBuildCanal(self, roadLocation):
        return self.canAffordCanal() and self.canPlaceCanal(roadLocation)

    def canBuildOneRailroad(self, roadLocation):
        return (
            self.canAffordOneRailroad()
            and self.canPlaceOneRailroad(roadLocation)
            and self.canAffordOneRailroadIndustryResources()
        )

    def canBuildTwoRailroads(self, roadLocation1, roadLocation2):
        return (
            self.canAffordTwoRailroads()
            and self.canAffordTwoRailroadIndustryResources(roadLocation1, roadLocation2)
            and self.canPlaceTwoRailroads(roadLocation1, roadLocation2)
        )

    # 3 DEVELOP
    def canDevelop(self, building1, building2):
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
    def canSell(self, building, buildLocation):
        return (
            building.isActive
            and building.owner == self
            and self.canAffordSellBuilding(building)
            and buildLocation.building
        )

    # 5 LOAN
    # is there a limit to the amount of loans you can take out? minimum income? prob not

    # 6 SCOUT
    def canScout(self):
        return (
            len(self.board.wildBuildingDeck) > 0
            and len(self.board.wildLocationDeck) > 0
        )

    """Actions"""
    # todo player discarding for actions
    # 1 BUILD
    def buildBuilding(self, building, buildLocation):
        assert self.canBuildBuilding(building, buildLocation)
        building.build(buildLocation)
        self.board.buildBuilding(building, buildLocation, self)

    # 2 NETWORK
    def buildCanal(self, roadLocation):
        assert self.canBuildCanal(roadLocation)
        self.board.buildCanal(roadLocation, self)

    def buildOneRailroad(self, roadLocation):
        assert self.canBuildOneRailroad(roadLocation)
        self.board.buildOneRailroad(roadLocation, self)

    def buildTwoRailroads(self, roadLocation1, roadLocation2):
        assert self.canBuildTwoRailroads(roadLocation1, roadLocation2)
        self.board.buildTwoRailroads(roadLocation1, roadLocation2, self)

    # 3 DEVELOP
    def develop(self, building1, building2):
        assert self.canDevelop(building1, building2)
        building1.isRetired = True
        building2.isRetired = True

    # 4 SELL
    def sell(self, building, buildLocation):
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

    def __repr__(self):
        return self.name
