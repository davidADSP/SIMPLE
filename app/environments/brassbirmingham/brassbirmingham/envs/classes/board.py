import copy

from ..python.id import id
from .deck import Deck
from ..consts import (
    STARTING_CARDS,
    STARTING_WILD_BUILDING_CARDS,
    STARTING_WILD_LOCATION_CARDS,
    TOWNS,
    TRADEPOSTS,
    ROAD_LOCATIONS,
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
                if town.name in roadLocation.networks:
                    town.addNetwork(roadLocation)

    """
    addPlayer
    game init use only

    :param player: player
    """

    def addPlayer(self, player):
        self.players.append(player)

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
    getCoalBuildings
    
    :return: array of buildings which have coal resources"""

    def getCoalBuildings(self):
        l = []
        for building in self.buildings:
            for buildLocation in building.buildLocations:
                building = buildLocation.building
                if (
                    building
                    and building.type == "industry"
                    and building.resourceType == "coal"
                    and building.resourceAmount > 0
                ):
                    l.append(building)
                    break
        return l

    """
    getBeerBuildings
    
    :return: array of buildings which have beer resources"""

    def getBeerBuildings(self):
        l = []
        for building in self.buildings:
            for buildLocation in building.buildLocations:
                building = buildLocation.building
                if (
                    building
                    and building.type == "industry"
                    and building.resourceType == "beer"
                    and building.resourceAmount > 0
                ):
                    l.append(building)
                    break
        return l

    """
    getIronTowns
    
    :return: array of buildings which have iron resources"""

    def getIronTowns(self):
        l = []
        for building in self.buildings:
            for buildLocation in building.buildLocations:
                building = buildLocation.building
                if (
                    building
                    and building.type == "industry"
                    and building.resourceType == "iron"
                    and building.resourceAmount > 0
                ):
                    l.append(building)
                    break
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
    
    :param town: town where beer is required
    :param beerAmount: amount of beer required
    :param money: amount of money available to spend, if necessary
    :return: is there beer available from networked buildings
    """

    def isBeerAvailableFromBuildings(self, town):
        # areNetworked puts priority on closest buildings to pick from
        # todo add priority for own buildings (?)

        # check for towns with beer available
        beerBuildings = self.getBeerBuildings()
        for beerBuilding in beerBuildings:
            if self.areNetworked(town, beerBuilding):
                return True
        return False

    """
    isIronAvailableFromBuildings
    
    :param town: town where iron is required
    :param ironAmount: amount of iron required
    :param money: amount of money available to spend, if necessary
    :return: is there iron available from networked buildings
    """

    def isIronAvailableFromBuildings(self, town):
        # areNetworked puts priority on closest buildings to pick from
        # todo add priority for own buildings (?)

        # check for towns with iron available
        ironBuildings = self.getIronBuildings()
        if len(ironBuildings > 0):
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

    def isBeerAvailableFromTradePosts(self, town, beerAmount, money):
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
    :param coalAmount: amount of coal required
    :param money: amount of money available
    :return: amount of coal"""

    def getAvailableCoalAmount(self, town, coalAmount, money):
        coalBuildings = self.getCoalBuildings()
        amount = 0
        for coalBuilding in coalBuildings:
            if self.areNetworked(town, coalBuilding):
                amount += coalBuilding.resourceAmount
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                if (
                    money > coalAmount * self.coalMarketPrice
                    and self.coalMarketRemaining > 0
                ):
                    amount += self.coalMarketRemaining
                    break
        return amount

    """
    getAvailableBeerAmount
    
    :param town: town where beer is required
    :param beerAmount: amount of beer required
    :param money: amount of money available
    :return: amount of beer"""

    def getAvailableBeerAmount(self, town, beerAmount, money):
        beerBuildings = self.getBeerBuildings()
        amount = 0
        for beerBuilding in beerBuildings:
            if self.areNetworked(town, beerBuilding):
                amount += beerBuilding.resourceAmount
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                if self.beerAmount >= beerAmount:
                    amount += self.beerAmount
                    break
        return amount

    """
    getAvailableCoalBuildingsTradePosts
    
    :param town: town where coal is required
    :param coalAmount: amount of coal required
    :param money: amount of money available
    :return: buildings/tradeposts with coal"""

    def getAvailableCoalBuildingsTradePosts(self, town, coalAmount, money):
        coalBuildings = self.getCoalBuildings()
        l = []
        for coalBuilding in coalBuildings:
            if self.areNetworked(town, coalBuilding):
                l.append(coalBuilding)
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                if (
                    money > coalAmount * self.coalMarketPrice
                    and self.coalMarketRemaining > 0
                ):
                    l.append(tradePost)
        return l

    """
    getAvailableBeerBuildingsTradePosts
    
    :param town: town where beer is required
    :param beerAmount: amount of beer required
    :param money: amount of money available
    :return: buildings/tradeposts with beer"""

    def getAvailableBeerBuildingsTradePosts(self, town):
        beerBuildings = self.getBeerBuildings()
        l = []
        for beerBuilding in beerBuildings:
            if self.areNetworked(town, beerBuilding):
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

    def buildBuilding(self, building, buildLocation, money):
        availableCoal = self.getAvailableCoalBuildingsTradePosts(
            building.town, building.coalCost, money
        )
        coalCost = copy.deepcopy(building.coalCost)
        _available = availableCoal.pop(0)
        # take coal away from resources
        while coalCost > 0:
            coalCost -= 1
            if _available.type == "TradePost":
                if self.coalMarketRemaining > 0:
                    money -= self.coalMarketPrice
                    self.coalMarketRemaining -= 1
                else:
                    raise ValueError(
                        "Not enough coal in trade post, make sure we check there is enough before calling board.buildBuilding"
                    )
            else:
                _available.resourceAmount -= 1
                if _available.resourceAmount == 0:
                    _available = availableCoal.pop(0)

        # todo take iron away from resources

        # build building - link building and buildLocation to each other
        buildLocation.addBuilding(building)
        building.build(buildLocation)

    """
    sellBuilding
    
    Make sure all costs and placements are checked and considered before calling this function
    :param building: building to sell
    """

    def sellBuilding(self, building):
        availableBeer = self.getAvailableBeerBuildingsTradePosts(building.town)
        beerCost = copy.deepcopy(building.beerCost)
        _available = availableBeer.pop(0)
        # take beer away from resources
        while beerCost > 0:
            beerCost -= 1
            if _available.type == "TradePost":
                if _available.beerAmount > 0:
                    _available.beerAmount -= 1
                else:
                    raise ValueError(
                        "Not enough beer in trade post, make sure we check there is enough before calling board.sellBuilding"
                    )
            else:
                _available.resourceAmount -= 1
                if _available.resourceAmount == 0:
                    _available = availableBeer.pop(0)

        # todo sell building
