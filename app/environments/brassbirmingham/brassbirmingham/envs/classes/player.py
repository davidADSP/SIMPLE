import copy
from ..python.id import id
from ..classes.hand import Hand
from ..classes.roads.canal import Canal
from ..consts import STARTING_MONEY, BUILDINGS, STARTING_ROADS


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

    def canAffordIndustryResources(self, buildLocation, coalCost, ironCost):
        return (
            self.board.isCoalAvailableFromBuildings(buildLocation.town)
            or self.board.isCoalAvailableFromTradePosts(
                buildLocation.town, coalCost, self.money
            )
        ) and self.board.isIronAvailable(buildLocation.town, ironCost, self.money)

    def canAffordBuilding(self, building):
        return self.money >= building.cost

    def canPlaceBuilding(self, building, buildLocation):
        return buildLocation.possibleBuild(building)

    def totalBuildingCost(self, building, coalCost, ironCost):
        return (
            building.cost
            + coalCost * self.board.coalMarketPrice
            + ironCost * self.board.ironMarketPrice
        )

    def canAffordCanal(self, roadLocation, cost):
        pass  # todo

    """Possible Actions"""

    def canBuildBuilding(self, building, buildLocation):
        return (
            self.canAffordIndustryResources(
                buildLocation, building.coalCost, building.ironCost
            )
            and self.canAffordBuilding(building, buildLocation)
            and self.canPlaceBuilding(building, buildLocation)
        )

    # def canBuildRoad)

    # def canNetwork(self, roadLocation):
    #     for building in self.buildings:
    #         if building.isActive:
    #             for

    def canDevelop(self, building):
        return not building.isActive and building.canBeDeveloped

    """Actions"""

    def buildBuilding(self, building, buildLocation):
        self.board.buildBuilding(building, buildLocation, self.money)
        # self.money -= totalCost
        building.build(buildLocation)

    def __repr__(self):
        return self.name
