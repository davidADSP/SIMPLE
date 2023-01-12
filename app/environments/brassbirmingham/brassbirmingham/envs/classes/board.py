import copy

from ..python.id import id
from ..python.print_colors import *
from .deck import Deck
from .roads import Canal, Railroad
from ..consts import (
    CANAL_PRICE,
    ONE_RAILROAD_COAL_PRICE,
    ONE_RAILROAD_PRICE,
    STARTING_CARDS,
    STARTING_WILD_BUILDING_CARDS,
    STARTING_WILD_LOCATION_CARDS,
    TOWNS,
    TRADEPOSTS,
    ROAD_LOCATIONS,
    TWO_RAILROAD_COAL_PRICE,
    TWO_RAILROAD_PRICE,
)


class Board:
    def __init__(self, NUM_PLAYERS):
        self.id = id()
        self.deck = Deck(STARTING_CARDS[str(NUM_PLAYERS)])
        self.wildBuildingDeck = Deck(STARTING_WILD_BUILDING_CARDS)
        self.wildLocationDeck = Deck(STARTING_WILD_LOCATION_CARDS)
        self.towns = TOWNS  # array of Town objects
        self.tradePosts = TRADEPOSTS
        self.coalMarketRemaining = 15  # is this right tyler? double check plz
        self.coalMarketPrice = 1
        self.ironMarketRemaining = 8  # also this
        self.ironMarketPrice = 1
        self.players = []  # array of Player objects

        for town in self.towns:
            town.addBoard(self)  # ref board to towns
        # network towns together
        for town in self.towns:
            for roadLocation in ROAD_LOCATIONS:
                print(roadLocation.networks)
                if town.name in roadLocation.networks:
                    print(f"adding {town.name}")
                    town.addRoadLocation(roadLocation)
        for tradePost in self.tradePosts:
            for roadLocation in ROAD_LOCATIONS:
                if tradePost.name in roadLocation.networks:
                    tradePost.addRoadLocation(roadLocation)

    """
    addPlayer
    game init use only

    :param player: player
    """

    def addPlayer(self, player):
        self.players.append(player)

    def getAllBuildings(self):
        l = []
        for town in self.towns:
            for buildLocation in town.buildLocations:
                if buildLocation.building:
                    l.append(buildLocation.building)
        return l

    """
    areNetworked
    
    :param town1: Town
    :param town2: Town
    :return: whether there is a road network built between towns
    """

    def areNetworked(self, town1, town2):
        print(f"Is there a network from {town1} to {town2}?")
        q = [town1]
        v = [town1.id]

        while q:
            town = q.pop(0)  # bfs
            # town = q.pop() #dfs
            # get town neighbors, add to q
            for network in town.networks:
                if network.isBuilt:
                    for _town in network.towns:
                        if _town.id not in v:
                            q.append(_town)
                            v.append(_town.id)
                            print(f"{_town=}, {town2=}, isRoadBuilt? {network.isBuilt}")
                            if _town.id == town2.id:
                                return True
        return False

    """
    removeXCoal
    
    :param X: amount of coal to remove
    :param towns: towns to search from, must be array [town]
    :param player: player to remove money from (if necessary)"""

    def removeXCoal(self, X, towns, player):
        for town in towns:
            availableCoal = self.getAvailableCoalBuildingsTradePosts(town)
            if availableCoal == 0:
                continue

            _available = availableCoal.pop(
                0
            )  # todo assert these changes to resourceAmount are actually affecting the building
            # take coal away from resources
            while X > 0:
                X -= 1
                if _available.type == "TradePost":
                    if self.coalMarketRemaining > 0:
                        player.money -= (
                            self.coalMarketPrice
                        )  # todo assert this changes player's money
                        self.coalMarketRemaining -= 1
                    else:
                        raise ValueError(
                            "Not enough coal in trade post, make sure we check there is enough before calling board.buildBuilding"
                        )
                else:
                    _available.resourceAmount -= 1
                    if _available.resourceAmount == 0:
                        _available = availableCoal.pop(0)
            return

    """
    removeXBeer
    
    :param X: amount of beer to remove
    :param towns: towns to search from, must be array [town]
    :param player: player to remove money from (if necessary)"""

    def removeXBeer(self, X, towns, player):
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
                    _available.resourceAmount -= 1
                    if _available.resourceAmount == 0:
                        _available = availableBeer.pop(0)
            return

    """
    getCoalBuildings
    
    :return: array of buildings which have coal resources"""

    def getCoalBuildings(self):
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == "industry"
                and building.resourceType == "coal"
                and building.resourceAmount > 0
            ):
                l.append(building)
        return l

    """
    getBeerBuildings
    
    :return: array of buildings which have beer resources"""

    def getBeerBuildings(self):
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == "industry"
                and building.resourceType == "beer"
                and building.resourceAmount > 0
            ):
                l.append(building)
        return l

    """
    getIronBuildings
    
    :return: array of buildings which have iron resources"""

    def getIronBuildings(self):
        l = []
        for building in self.getAllBuildings():
            if (
                building
                and building.type == "industry"
                and building.resourceType == "iron"
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

    def isCoalAvailableFromBuildings(self, town):
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

    def isBeerAvailableFromBuildings(self, player, town):
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

    def isIronAvailableFromBuildings(self):
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

    def isCoalAvailableFromTradePosts(self, town, coalAmount, money):
        # check for connection to tradeposts
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                # enough money for coal amount?
                # tyler double check sale price on this
                if (
                    money > coalAmount * self.coalMarketPrice
                    and self.coalMarketRemaining > 0
                ):
                    return True
        return False

    """
    isBeerAvailableFromTradePosts
    
    :param town: town where beer is required
    :param beerAmount: amount of beer required
    :param money: amount of money available
    :return: is there beer available from networked trade posts
    """

    def isBeerAvailableFromTradePosts(self, town):
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

    def isIronAvailableFromTradePosts(self, ironAmount, money):
        # enough money for iron amount?
        # tyler double check sale price on this
        return (
            money > ironAmount * self.ironMarketPrice and self.ironMarketRemaining > 0
        )

    """
    getAvailableCoalAmount
    
    :param town: town where coal is required
    :return: amount of coal"""

    def getAvailableCoalAmount(self, town):
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

    def getAvailableBeerAmount(self, player, town):
        beerBuildings = self.getBeerBuildings()
        amount = 0
        for beerBuilding in beerBuildings:
            if beerBuilding.owner == player or self.areNetworked(town, beerBuilding):
                amount += beerBuilding.resourceAmount
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                amount += self.beerAmount
                break
        return amount

    """
    getAvailableIronAmount
    
    :param player: player inquiring
    :param town: town where iron is required
    :return: amount of iron"""

    def getAvailableIronAmount(self):
        ironBuildings = self.getIronBuildings()
        amount = 0
        for ironBuilding in ironBuildings:
            amount += ironBuilding.resourceAmount
        # trade post
        amount += self.ironAmount
        return amount

    """
    getAvailableCoalBuildingsTradePosts
    
    :param town: town where coal is required
    :return: buildings/tradeposts with coal"""

    def getAvailableCoalBuildingsTradePosts(self, town):
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

    def getAvailableBeerBuildingsTradePosts(self, player, town):
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

    def buildBuilding(self, building, buildLocation, player):
        self.removeXCoal(building.coalCost, [building.town], player)
        player.money -= building.cost
        # todo take iron away from resources

        # build building - link building and buildLocation to each other
        buildLocation.addBuilding(building)
        building.build(buildLocation)

    def buildCanal(self, roadLocation, player):
        player.money -= CANAL_PRICE
        roadLocation.build(Canal(player))

    def buildOneRailroad(self, roadLocation, player):
        player.money -= ONE_RAILROAD_PRICE
        self.removeXCoal(ONE_RAILROAD_COAL_PRICE, roadLocation.towns, player)
        roadLocation.build(Railroad(player))

    def buildTwoRailroads(self, roadLocation1, roadLocation2, player):
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

    def sellBuilding(self, building, buildLocation, player):
        self.removeXBeer(building.sell, [building.town], player)
        building.sell(buildLocation)
        buildLocation.sellBuilding()


class Town:
    """
    Town

    :param color: any of ['blue', 'green', 'red', 'yellow', 'purple']
    :param name: name
    :param buildLocation: array of BuildLocation objects"""

    def __init__(self, color, name, buildLocations):
        self.id = id()
        self.color = color
        self.name = name
        self.buildLocations = buildLocations
        for buildLocation in self.buildLocations:
            buildLocation.addTown(self)
        self.networks = (
            []
        )  # networks to other towns ex: Town('Leek') would have [Town('Stoke-On-Trent'), Town('Belper')]

    """
    addBoard
    game init use only

    :param board: board
    """

    def addBoard(self, board):
        self.board = board

    """
    addRoadLocation
    game init use only

    :param roadLocation: roadLocation
    """

    def addRoadLocation(self, roadLocation):
        roadLocation.addTown(self)
        self.networks.append(roadLocation)

    def __str__(self):
        returnStr = ""
        if self.color == "blue":
            returnStr = prCyan(self.name)
        elif self.color == "green":
            returnStr = prGreen(self.name)
        elif self.color == "red":
            returnStr = prRed(self.name)
        elif self.color == "yellow":
            returnStr = prYellow(self.name)
        elif self.color == "purple":
            returnStr = prPurple(self.name)
        elif self.color == "beer1" or self.color == "beer2":
            returnStr = prLightGray(self.color)
        return f"Town({returnStr})"

    def __repr__(self):
        return str(self)
