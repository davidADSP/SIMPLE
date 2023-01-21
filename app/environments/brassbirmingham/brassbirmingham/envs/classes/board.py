from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Dict, List

from consts import (CANAL_PRICE, MAX_MARKET_COAL, MAX_MARKET_IRON,
                    ONE_RAILROAD_COAL_PRICE, ONE_RAILROAD_PRICE,
                    ROAD_LOCATIONS, STARTING_CARDS, TOWNS, TRADEPOSTS,
                    TWO_RAILROAD_COAL_PRICE, TWO_RAILROAD_PRICE)
from python.id import id
from python.print_colors import *

from .build_location import BuildLocation
from .buildings.building import Building
from .buildings.enums import BuildingName, BuildingType
from .buildings.industry_building import IndustryBuilding
from .buildings.market_building import MarketBuilding
from .deck import Deck
from .enums import Era
from .road_location import RoadLocation
from .roads.canal import Canal
from .roads.railroad import Railroad
from .roads.road import Road
from .town import Town
from .trade_post import TradePost

if TYPE_CHECKING:
    from .player import Player


class Board:
    def __init__(self, numPlayers: int):
        self.id = id()
        self.era = Era.canal
        self.deck = Deck(STARTING_CARDS[str(numPlayers)])
        self.towns = copy.deepcopy(TOWNS)  # array of Town objects
        self.townDict = {}
        self.tradePosts = copy.deepcopy(TRADEPOSTS)
        self.coalMarketRemaining = MAX_MARKET_COAL - 1  # coal market missing 1
        self.ironMarketRemaining = MAX_MARKET_IRON - 2  # iron market missing 1
        self.roadLocations = copy.deepcopy(ROAD_LOCATIONS)
        self.players: List[Player] = []  # array of Player objects

        for town in self.towns:
            town.addBoard(self)  # ref board to towns

        for town in self.towns:
            self.townDict[town.name] = town
        # network towns together
        for town in self.towns:
            for roadLocation in self.roadLocations:
                if town.name in roadLocation.networks:
                    town.addRoadLocation(roadLocation)
        for tradePost in self.tradePosts:
            for roadLocation in self.roadLocations:
                if tradePost.name in roadLocation.networks:
                    tradePost.addRoadLocation(roadLocation)

    """
    addPlayer
    game init use only

    :param player: player
    """

    def addPlayer(self, player: Player):
        self.players.append(player)

    def getAllBuildings(self) -> List[Building]:
        l = []
        for town in self.towns:
            for buildLocation in town.buildLocations:
                if buildLocation.building:
                    l.append(buildLocation.building)
        return l

    def priceForCoal(self, coalNeeded: int) -> int:
        price = 0
        currCoalRemaining = self.coalMarketRemaining
        for _ in range(coalNeeded):
            if currCoalRemaining <= 0:
                price += 8
            elif currCoalRemaining == 1 or currCoalRemaining == 2:
                price += 7
            elif currCoalRemaining == 3 or currCoalRemaining == 4:
                price += 6
            elif currCoalRemaining == 5 or currCoalRemaining == 6:
                price += 5
            elif currCoalRemaining == 7 or currCoalRemaining == 8:
                price += 4
            elif currCoalRemaining == 9 or currCoalRemaining == 10:
                price += 3
            elif currCoalRemaining == 11 or currCoalRemaining == 12:
                price += 2
            elif currCoalRemaining >= 13:
                price += 1
            currCoalRemaining = max(currCoalRemaining - 1, 0)
        return price

    def priceForIron(self, ironNeeded: int) -> int:
        price = 0
        currIronRemaining = self.ironMarketRemaining
        for _ in range(ironNeeded):
            if currIronRemaining <= 0:
                price += 6
            elif currIronRemaining == 1 or currIronRemaining == 2:
                price += 5
            elif currIronRemaining == 3 or currIronRemaining == 4:
                price += 4
            elif currIronRemaining == 5 or currIronRemaining == 6:
                price += 3
            elif currIronRemaining == 7 or currIronRemaining == 8:
                price += 2
            elif currIronRemaining >= 13:
                price += 1
            currIronRemaining = max(currIronRemaining - 1, 0)
        return price

    """
    areNetworked
    
    :param town1: Town
    :param town2: Town
    :return: whether there is a road network built between towns
    """

    def areNetworked(
        self, town1: Town | Building | TradePost, town2: Town | Building | TradePost
    ) -> bool:
        q = [town1]
        v = [town1.id]

        while q:
            town = q.pop(0)  # bfs
            # get town neighbors, add to q
            for roadLocation in town.networks:
                if roadLocation.isBuilt:
                    for _town in roadLocation.towns:
                        if _town.id not in v:
                            q.append(_town)
                            v.append(_town.id)
                            if _town.id == town2.id:
                                return True
        return False

    """
    removeXCoal
    
    :param X: amount of coal to remove
    :param towns: towns to search from, must be array [town]
    :param player: player to remove money from (if necessary)"""

    def removeXCoal(self, X: int, towns: List[Town], player: Player):
        for town in towns:
            availableCoal = self.getAvailableCoalBuildingsTradePosts(town)
            if availableCoal == 0:
                continue

            _available = availableCoal.pop(
                0
            )  # todo assert these changes to resourceAmount are actually affecting the building
            # take coal away from resources
            while X > 0:
                if _available.type == "TradePost":
                    cost = self.priceForCoal(X)
                    player.money -= cost  # todo assert this changes player's money
                    self.coalMarketRemaining -= X
                    return
                else:
                    _available.decreaseResourceAmount(1)
                    if _available.resourceAmount == 0:
                        _available = availableCoal.pop(0)
                X -= 1
            return

    """
    removeXBeer
    
    :param X: amount of beer to remove
    :param towns: towns to search from, must be array [town]
    :param player: player to remove money from (if necessary)"""

    def removeXBeer(self, X: int, towns: List[Town], player: Player):
        for town in towns:
            availableBeer = self.getAvailableBeerBuildingsTradePosts(player, town)
            if availableBeer == 0:
                continue

            _available = availableBeer.pop(
                0
            )  # todo assert these changes to resourceAmount are actually affecting the building
            # take beer away from resources
            while X > 0:
                X -= 1
                if _available.type == "TradePost":
                    if _available.beerAmount > 0:
                        _available.beerAmount -= 1
                    else:
                        raise ValueError(
                            "Not enough beer in trade post, make sure we check there is enough before calling board.buildBuilding"
                        )
                else:
                    _available.decreaseResourceAmount(1)
                    if _available.resourceAmount == 0:
                        _available = availableBeer.pop(0)
            return

    """
    getCoalBuildings
    
    :return: array of buildings which have coal resources"""

    def getCoalBuildings(self) -> List[IndustryBuilding]:
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == BuildingType.industry
                and building.name == BuildingName.coal
                and building.resourceAmount > 0
            ):
                l.append(building)
        return l

    """
    getBeerBuildings
    
    :return: array of buildings which have beer resources"""

    def getBeerBuildings(self) -> List[IndustryBuilding]:
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == BuildingType.industry
                and building.name == BuildingName.coal
                and building.resourceAmount > 0
            ):
                l.append(building)
        return l

    """
    getIronBuildings
    
    :return: array of buildings which have iron resources"""

    def getIronBuildings(self) -> List[IndustryBuilding]:
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == BuildingType.industry
                and building.name == BuildingName.coal
                and building.resourceAmount > 0
            ):
                l.append(building)
        return l

    """
    isCoalAvailableFromBuildings
    
    :param town: town where coal is required
    :param coalAmount: amount of coal required
    :param money: amount of money available to spend, if necessary
    :return: is there coal available from networked buildings
    """

    def isCoalAvailableFromBuildings(self, town: Town) -> bool:
        # areNetworked puts priority on closest buildings to pick from
        # todo add priority for own buildings (?)

        # check for towns with coal available
        coalBuildings = self.getCoalBuildings()
        for coalBuilding in coalBuildings:
            if self.areNetworked(town, coalBuilding):
                return True
        return False

    """
    isBeerAvailableFromBuildings
    
    :param player: player inquiring
    :param town: town where beer is required
    :return: is there beer available from networked buildings
    """

    def isBeerAvailableFromBuildings(self, player: Player, town: Town) -> bool:
        # areNetworked puts priority on closest buildings to pick from
        # todo add priority for own buildings (?)

        # check for towns with beer available
        beerBuildings = self.getBeerBuildings()
        for beerBuilding in beerBuildings:
            if beerBuilding.owner == player or self.areNetworked(town, beerBuilding):
                return True
        return False

    """
    isIronAvailableFromBuildings
    
    :return: is there iron available from buildings
    """

    def isIronAvailableFromBuildings(self) -> bool:
        # areNetworked puts priority on closest buildings to pick from
        # todo add priority for own buildings (?)

        # check for towns with iron available
        ironBuildings = self.getIronBuildings()
        if len(ironBuildings) > 0:
            # todo non player-owned need network
            return True
        return False

    """
    isCoalAvailableFromTradePosts
    
    :param town: town where coal is required
    :param coalAmount: amount of coal required
    :param money: amount of money available
    :return: is there coal available from networked trade posts
    """

    def isCoalAvailableFromTradePosts(
        self, town: Town, coalAmount: int, money: int
    ) -> bool:
        # check for connection to tradeposts
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                cost = self.priceForCoal(coalAmount)
                if money > cost:
                    return True
        return False

    """
    isBeerAvailableFromTradePosts
    
    :param town: town where beer is required
    :param beerAmount: amount of beer required
    :param money: amount of money available
    :return: is there beer available from networked trade posts
    """

    def isBeerAvailableFromTradePosts(self, town: Town) -> bool:
        # check for connection to tradeposts
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                # enough money for beer amount?
                # tyler double check sale price on this
                if tradePost.beerAmount > 0:
                    return True
        return False

    """
    isIronAvailableFromTradePosts
    
    :param ironAmount: amount of iron required
    :param money: amount of money available
    :return: is there iron available from networked trade posts
    """

    def isIronAvailableFromTradePosts(self, ironAmount: int, money: int) -> bool:
        return money > self.priceForIron(ironAmount)

    """
    getAvailableCoalAmount
    
    :param town: town where coal is required
    :return: amount of coal"""

    def getAvailableCoalAmount(self, town: Town) -> int:
        coalBuildings = self.getCoalBuildings()
        amount = 0
        for coalBuilding in coalBuildings:
            if self.areNetworked(town, coalBuilding):
                amount += coalBuilding.resourceAmount
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                amount += self.coalMarketRemaining
                break
        return amount

    """
    getAvailableBeerAmount
    
    :param player: player inquiring
    :param town: town where beer is required
    :return: amount of beer"""

    def getAvailableBeerAmount(self, player: Player, town: Town) -> int:
        beerBuildings = self.getBeerBuildings()
        amount = 0
        for beerBuilding in beerBuildings:
            if beerBuilding.owner == player or self.areNetworked(town, beerBuilding):
                amount += beerBuilding.resourceAmount
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                amount += tradePost.beerAmount
                break
        return amount

    """
    getAvailableCoalBuildingsTradePosts
    
    :param town: town where coal is required
    :return: buildings/tradeposts with coal"""

    def getAvailableCoalBuildingsTradePosts(
        self, town: Town
    ) -> List[IndustryBuilding | TradePost]:
        coalBuildings = self.getCoalBuildings()
        l = []
        for coalBuilding in coalBuildings:
            if self.areNetworked(town, coalBuilding):
                l.append(coalBuilding)
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                if self.coalMarketRemaining > 0:
                    l.append(tradePost)
        return l

    """
    getAvailableBeerBuildingsTradePosts
    
    :param player: player inquiring
    :param town: town where beer is required
    :return: buildings/tradeposts with beer"""

    def getAvailableBeerBuildingsTradePosts(
        self, player: Player, town: Town
    ) -> List[Building | TradePost]:
        beerBuildings = self.getBeerBuildings()
        l = []
        for beerBuilding in beerBuildings:
            if beerBuilding.owner == player or self.areNetworked(town, beerBuilding):
                l.append(beerBuilding)
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                if tradePost.beerAmount > 0:
                    l.append(tradePost)
        return l

    """
    isIronAvailable
    
    :param ironAmount: amount of iron required
    :param money: amount of money available to spend, if necessary
    """
    # def isIronAvailable(self, town, ironAmount, money): todo

    """
    buildBuilding
    
    Make sure all costs and placements are checked and considered before calling this function
    :param building: building to build
    :param buildLocation: where to build building
    :param money: player's money
    """

    def buildBuilding(
        self, building: Building, buildLocation: BuildLocation, player: Player
    ):
        self.removeXCoal(building.coalCost, [building.town], player)
        player.money -= building.cost
        # todo take iron away from resources

        # build building - link building and buildLocation to each other
        buildLocation.addBuilding(building)
        building.build(buildLocation)

    def buildCanal(self, roadLocation: RoadLocation, player: Player):
        player.money -= CANAL_PRICE
        roadLocation.build(Canal(player))

    def buildOneRailroad(self, roadLocation: RoadLocation, player: Player):
        player.money -= ONE_RAILROAD_PRICE
        self.removeXCoal(ONE_RAILROAD_COAL_PRICE, roadLocation.towns, player)
        roadLocation.build(Railroad(player))

    def buildTwoRailroads(
        self, roadLocation1: RoadLocation, roadLocation2: RoadLocation, player: Player
    ):
        player.money -= TWO_RAILROAD_PRICE
        self.removeXCoal(
            TWO_RAILROAD_COAL_PRICE,
            [*roadLocation1.towns, *roadLocation2.towns],
            player,
        )
        roadLocation1.build(Railroad(player))
        roadLocation2.build(Railroad(player))

    """
    sellBuilding
    
    Make sure all costs and placements are checked and considered before calling this function
    :param building: building to sell
    """

    def sellBuilding(self, building: MarketBuilding, player: Player):
        self.removeXBeer(building.beerCost, [building.town], player)
        building.sell()

    def getVictoryPoints(self) -> Dict[str, int]:
        points = {player.id: player.victoryPoints for player in self.players}

        for building in self.getAllBuildings():
            if building.isFlipped:
                points[building.owner.id] += building.victoryPointsGained

        for town in self.towns:
            for network in town.networks:
                if network.road and network.isBuilt:
                    points[network.road.owner.id] += town.getNetworkVictoryPoints()

        for tradePost in self.tradePosts:
            for network in tradePost.networks:
                if network.road and network.isBuilt:
                    points[network.road.owner.id] += tradePost.networkPoints

        return points
