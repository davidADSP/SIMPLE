import uuid
import copy
import random
def prRed(skk): return ("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): return ("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): return ("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): return ("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): return ("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): return ("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): return ("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): return ("\033[98m {}\033[00m" .format(skk))

def id():
    return uuid.uuid1()

class Player():
    def __init__(self, name, board):
        self.id = id()
        self.name = name
        self.board = board
        self.hand = Hand(self.board.deck)
        self.money = STARTING_MONEY
        self.income = 0
        self.victoryPoints = 0
        self.spentThisTurn = 0
        self.buildings = copy.deepcopy(BUILDINGS) #buildings, array of Building objects
        for building in self.buildings:
            building.addOwner(self)
            
        self.roads = [Canal(self) for x in range(STARTING_ROADS)] #canals/railroads, array of Road objects
        self.board.addPlayer(self)

    def canAffordIndustryResources(self, buildLocation, coalCost, ironCost):
        return (self.board.isCoalAvailableFromBuildings(buildLocation.town) or self.board.isCoalAvailableFromTradePosts(buildLocation.town, coalCost, self.money)) and self.board.isIronAvailable(buildLocation.town, ironCost, self.money)
    
    def canAffordBuilding(self, building):
        return self.money >= building.cost

    def canPlaceBuilding(self, building, buildLocation):
        return buildLocation.possibleBuild(building)

    def totalBuildingCost(self, building, coalCost, ironCost):
        return building.cost + coalCost*self.board.coalMarketPrice + ironCost*self.board.ironMarketPrice

    def canAffordCanal(self, roadLocation, cost):
        pass #todo

    """Possible Actions"""
    def canBuildBuilding(self, building, buildLocation):
        return self.canAffordIndustryResources(buildLocation, building.coalCost, building.ironCost) and self.canAffordBuilding(building, buildLocation) and self.canPlaceBuilding(building, buildLocation)

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

"""
CARDS
"""
class Card():
    """
    Card object

    :param type: any of ['location', 'industry', 'wild']
    :param name: name of location or industry
    """
    def __init__(self, type):
        self.id = id()
        self.type = type
    
class LocationCard(Card):
    def __init__(self, name, isWild=False):
        super(LocationCard, self).__init__('location')
        self.name = name
        self.isWild = isWild
    
    def __str__(self):
        if self.isWild:
            return self.name

        if self.name in ['Stoke-On-Trent', 'Leek', 'Stone', 'Uttoxeter']:
            return prCyan(self.name)
        elif self.name in ['Belper', 'Derby']:
            return prGreen(self.name)
        elif self.name in ['Stafford', 'Cannock', 'Walsall', 'Burton-Upon-Trent', 'Tamworth']:
            return prRed(self.name)
        elif self.name in ['Wolverhampton', 'Coalbrookdale', 'Dudley', 'Kidderminster', 'Worcester']:
            return prYellow(self.name)
        elif self.name in ['Nuneaton', 'Birmingham', 'Coventry', 'Redditch']:
            return prPurple(self.name)
        elif self.name == 'beer1' or self.name == 'beer2':
            return prLightGray(self.name)
        return self.name

    def __repr__(self):
        return str(self)
 
    
class IndustryCard(Card):
    def __init__(self, name, isWild=False):
        super(IndustryCard, self).__init__('building')
        self.name = name
        self.isWild = isWild

    def __str__(self):
        if self.isWild:
            return self.name
        return prGreen(self.name)

    def __repr__(self):
        return str(self)

class Hand():
    """
    Hand object
    
    :param deck: Deck object"""
    def __init__(self, deck):
        self.id = id()
        self.cards = []
        self.deck = deck

    def draw(self):
        self.cards.append(self.deck.draw())
    
    def spendCard(self, card):
        self.cards = list(filter(lambda x: x.id != card.self.cards, self.cards)) #remove that card from hand
        self.deck.discardPile.append(card)

    """
    getTotal
    
    :return: amount of cards in hand
    """
    def getTotal(self):
        return len(self.cards)

    def __repr__(self):
        return self.cards

class Deck():
    """
    Deck object
    
    :param cards: array of Card objects
    """
    def __init__(self, cards):
        self.id = id()
        self.cards = cards
        self.discardPile = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards > 0):
            return self.cards.pop()
        else:
            self.reset()

    def reset(self):
        self.cards = self.discardPile
        self.discardPile = []
        self.shuffle()

    def __str__(self):
        return str(self.cards)

"""
BUILDINGS
"""
class Building():
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
    def __init__(self, type, name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, networkPoints, canBeDeveloped, onlyPhaseOne, onlyPhaseTwo):
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
        self.onlyPhaseOne = onlyPhaseOne #can only be built during phase 1
        self.onlyPhaseTwo = onlyPhaseTwo #can only be built during phase 2

        self.isSold = False # is sold/ran out of resources
        self.isActive = False # is on the board i.e., not bought yet
        self.isRetired = False # only used for retired buildings (tier 1's) in second phase

    """
    addOwner - add player/owner to building
    game init use only

    :param owner: player
    """
    def addOwner(self, owner):
        self.owner = owner
        
    def build(self, buildLocation):
        self.isActive = True
        self.town = buildLocation.town


    def __repr__(self):
        return f'\nBuilding {self.name}:: Owner: {self.owner}, Bought: {self.isActive}, Sold: {self.isSold} Retired: {self.isRetired}'
        
    
class MarketBuilding(Building):
    """
    Market Building
    
    :param name: any of [goods, cotton, pottery]
    :param tier: ex: 3
    :param cost: cost
    :param coalCost: ex: 1
    :param ironCost: ironCost
    :param beerCost: amount of beer required to sell
    :param victoryPointsGained: victory points gained from selling
    :param incomeGained: income gained from selling
    :param networkPoints: amount of points each road gets during counting step
    :param canBeDeveloped=True:
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """
    def __init__(self, name, tier, cost, coalCost, ironCost, beerCost, victoryPointsGained, incomeGained, networkPoints, canBeDeveloped=True, onlyPhaseOne=False, onlyPhaseTwo=False):
        super(MarketBuilding, self).__init__('market', name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, networkPoints, canBeDeveloped, onlyPhaseOne, onlyPhaseTwo)
        self.beerCost = beerCost

class IndustryBuilding(Building):
    """
    Industry Building
    
    :param name: any of [oil, coal, beer]
    :param tier: ex: 3
    :param resourceAmount: current resource amount on building
    :param cost: cost
    :param coalCost:
    :param ironCost:
    :param victoryPointsGained: victory points gained from flipping
    :param incomeGained: income gained from flipping
    :param networkPoints: amount of points each road gets during counting step
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """
    def __init__(self, name, tier, resourceAmount, cost, coalCost, ironCost, victoryPointsGained, incomeGained, networkPoints, onlyPhaseOne=False, onlyPhaseTwo=False):
        super(IndustryBuilding, self).__init__('industry', name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, networkPoints, True, onlyPhaseOne, onlyPhaseTwo)
        self.resourceAmount = resourceAmount
        self.resourcesType = name

class Road():
    def __init__(self, owner, type):
        self.id = id()
        self.type = type
        self.owner = owner

    def __repr__(self):
        return f'Owner: {self.owner}, {self.type}'

class Canal(Road):
    def __init__(self, owner):
        super(Canal, self).__init__(owner, 'canal')
        self.cost = 3

class Railroad(Road):
    def __init__(self, owner):
        super(Railroad, self).__init__(owner, 'railroad')
        #todo cost

"""
BOARD
"""
class Board():
    def __init__(self, NUM_PLAYERS):
        self.id = id()
        self.deck = Deck(STARTING_CARDS[str(NUM_PLAYERS)])
        self.wildBuildingDeck = Deck(STARTING_WILD_BUILDING_CARDS)
        self.wildLocationDeck = Deck(STARTING_WILD_LOCATION_CARDS)
        self.towns = TOWNS #array of Town objects
        self.tradePosts = TRADEPOSTS
        self.coalMarketRemaining = 15 #is this right tyler? double check plz
        self.coalMarketPrice = 1
        self.ironMarketRemaining = 8 #also this
        self.ironMarketPrice = 1
        self.players = [] #array of Player objects

        for town in self.towns:
            town.addBoard(self) #ref board to towns
        #network towns together
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
            town = q.pop(0) #bfs
            # town = q.pop() #dfs
            # get town neighbors, add to q
            for network in town.networks:
                if network.isBuilt:
                    for _town in network.towns:
                        if _town.id not in v:
                            q.append(_town)
                            v.append(_town.id)
                            print(f'{_town=}, {town2=}, isRoadBuilt? {network.isBuilt}')
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
                if building and building.type == 'industry' and building.resourceType == 'coal' and building.resourceAmount > 0:
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
                if building and building.type == 'industry' and building.resourceType == 'beer' and building.resourceAmount > 0:
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
                if building and building.type == 'industry' and building.resourceType == 'iron' and building.resourceAmount > 0:
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
        #areNetworked puts priority on closest buildings to pick from
        #todo add priority for own buildings (?)

        #check for towns with coal available
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
        #areNetworked puts priority on closest buildings to pick from
        #todo add priority for own buildings (?)

        #check for towns with beer available
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
        #areNetworked puts priority on closest buildings to pick from
        #todo add priority for own buildings (?)

        #check for towns with iron available
        ironBuildings = self.getIronBuildings()
        if len(ironBuildings > 0):
            #todo non player-owned need network
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
        #check for connection to tradeposts
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                #enough money for coal amount?
                #tyler double check sale price on this
                if money > coalAmount*self.coalMarketPrice and self.coalMarketRemaining > 0:
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
        #check for connection to tradeposts
        for tradePost in self.tradePosts:
            if self.areNetworked(town, tradePost):
                #enough money for beer amount?
                #tyler double check sale price on this
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
        #enough money for iron amount?
        #tyler double check sale price on this
        return money > ironAmount*self.ironMarketPrice and self.ironMarketRemaining > 0

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
                if money > coalAmount*self.coalMarketPrice and self.coalMarketRemaining > 0:
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
                if money > coalAmount*self.coalMarketPrice and self.coalMarketRemaining > 0:
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
        availableCoal = self.getAvailableCoalBuildingsTradePosts(building.town, building.coalCost, money)
        coalCost = copy.deepcopy(building.coalCost)
        _available = availableCoal.pop(0)
        #take coal away from resources
        while coalCost > 0:
            coalCost -= 1
            if _available.type == "TradePost":
                if self.coalMarketRemaining > 0:
                    money -= self.coalMarketPrice
                    self.coalMarketRemaining -= 1
                else:
                    raise ValueError("Not enough coal in trade post, make sure we check there is enough before calling board.buildBuilding")
            else:
                _available.resourceAmount -= 1
                if _available.resourceAmount == 0:
                    _available = availableCoal.pop(0)

        # todo take iron away from resources

        #build building - link building and buildLocation to each other
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
        #take beer away from resources
        while beerCost > 0:
            beerCost -= 1
            if _available.type == "TradePost":
                if _available.beerAmount > 0:
                    _available.beerAmount -= 1
                else:
                    raise ValueError("Not enough beer in trade post, make sure we check there is enough before calling board.sellBuilding")
            else:
                _available.resourceAmount -= 1
                if _available.resourceAmount == 0:
                    _available = availableBeer.pop(0)

        #todo sell building

class Town():
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
        self.networks = [] #networks to other towns ex: Town('Leek') would have [Town('Stoke-On-Trent'), Town('Belper')]

    """
    addBoard
    game init use only

    :param board: board
    """
    def addBoard(self, board):
        self.board = board
        
    """
    addNetwork
    game init use only

    :param network: network
    """
    def addNetwork(self, network):
        network.addTown(self)
        self.networks.append(network)

    def __str__(self):
        returnStr = ''
        if self.color == 'blue':
            returnStr = prCyan(self.name)
        elif self.color == 'green':
            returnStr = prGreen(self.name)
        elif self.color == 'red':
            returnStr = prRed(self.name)
        elif self.color == 'yellow':
            returnStr = prYellow(self.name)
        elif self.color == 'purple':
            returnStr = prPurple(self.name)
        elif self.color == 'beer1' or self.color == 'beer2':
            returnStr = prLightGray(self.color)
        return str(returnStr)

    def __repr__(self):
        return str(self)
 

class BuildLocation():
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

class RoadLocation():
    """
    Road Location - Where a canal or railroad may be built
    
    :param networks: Networks to what Towns/TradePosts road is networked to, array of Towns/TradePosts
    :param canBuildCanal=True: is river
    :param canBuildRailroad=True: is railroad track
    """
    def __init__(self, networks, canBuildCanal=True, canBuildRailroad=True):
        self.id = id()
        self.networks = networks
        self.canBuildCanal = canBuildCanal
        self.canBuildRailroad = canBuildRailroad
        self.isBuilt = False
        self.towns = []
    
    """
    addTown
    game init use only

    :param town: town
    """
    def addTown(self, town):
        self.towns.append(town)

class TradePost():
    """
    TradePost
    
    :param name: name
    :param beerAmount: amount of starting beer
    :param moneyGained: money gained from first trade
    :param victoryPointsGained: victory points gained from first trade
    :param incomeGained: income gained from first trade
    :param networkPoints: amount of points each road gets during counting step
    :param canDevelop: can develop after first trade
    """
    def __init__(self, name, beerAmount, moneyGained, victoryPointsGained, incomeGained, networkPoints, canDevelop):
        self.id = id()
        self.type = "TradePost"
        self.name = name
        self.beerAmount = beerAmount
        self.moneyGained = moneyGained
        self.victoryPointsGained = victoryPointsGained
        self.incomeGained = incomeGained
        self.possibleTrades = []
        self.networkPoints = networkPoints
        self.canDevelop = canDevelop
    
    """
    addPossibleTrade
    game init use only
    trades which are possible to make, array of Building object names 'oil', 'goods', etc...

    :param possibleTrade: possibleTrade
    """
    def addPossibleTrade(self, possibleTrade):
        self.possibleTrades.append(possibleTrade)

STARTING_ROADS = 14
STARTING_MONEY = 17
# TOTAL_COAL = 30
# TOTAL_IRON = 18
# TOTAL_BEER = 15
#amt of tokens doesn't matter actually

TOWNS = [
    Town('blue', 'Leek', [BuildLocation(['cotton', 'goods']), BuildLocation(['cotton', 'coal'])]),
    Town('blue', 'Stoke-On-Trent', [BuildLocation(['cotton', 'goods']), BuildLocation(['pottery', 'oil']), BuildLocation(['goods'])]),
    Town('blue', 'Stone', [BuildLocation(['cotton', 'beer']), BuildLocation(['goods', 'coal'])]),
    Town('blue', 'Uttoxeter', [BuildLocation(['goods', 'beer']), BuildLocation(['cotton', 'beer'])]),
    Town('green', 'Belper', [BuildLocation(['cotton', 'goods']), BuildLocation(['coal']), BuildLocation(['pottery'])]),
    Town('green', 'Derby', [BuildLocation(['cotton', 'beer']), BuildLocation(['cotton', 'goods']), BuildLocation(['oil'])]),
    Town('red', 'Stafford', [BuildLocation(['goods', 'beer']), BuildLocation(['pottery'])]),
    Town('red', 'Burton-Upon-Trent', [BuildLocation(['goods', 'coal']), BuildLocation(['beer'])]),
    Town('beer1', '', [BuildLocation(['beer'])]),
    Town('red', 'Cannock', [BuildLocation(['goods', 'coal']), BuildLocation(['coal'])]),
    Town('red', 'Tamworth', [BuildLocation(['cotton', 'coal']), BuildLocation(['cotton', 'coal'])]),
    Town('red', 'Walsall', [BuildLocation(['oil', 'goods']), BuildLocation(['goods', 'beer'])]),
    Town('yellow', 'Coalbrookdale', [BuildLocation(['oil', 'beer']), BuildLocation(['oil']), BuildLocation(['coal'])]),
    Town('yellow', 'Wolverhampton', [BuildLocation(['goods']), BuildLocation(['goods', 'coal'])]),
    Town('yellow', 'Dudley', [BuildLocation(['coal']), BuildLocation(['oil'])]),
    Town('yellow', 'Kidderminster', [BuildLocation(['cotton', 'coal']), BuildLocation(['cotton'])]),
    Town('beer2', '', [BuildLocation(['beer'])]),
    Town('yellow', 'Worcester', [BuildLocation(['cotton']), BuildLocation(['cotton'])]),
    Town('purple', 'Birmingham', [BuildLocation(['cotton', 'goods']), BuildLocation(['goods']), BuildLocation(['oil']), BuildLocation(['goods'])]),
    Town('purple', 'Nuneaton', [BuildLocation(['goods', 'beer']), BuildLocation(['cotton', 'coal'])]),
    Town('purple', 'Coventry', [BuildLocation(['pottery']), BuildLocation(['goods', 'coal']), BuildLocation(['oil', 'goods'])]),
    Town('purple', 'Redditch', [BuildLocation(['goods', 'coal']), BuildLocation(['oil'])])
]

TRADEPOSTS = [
    TradePost('Warrington', 2, 5, 0, 0, 2, False), 
    TradePost('Nottingham', 2, 0, 3, 0, 2, False),
    TradePost('Shrewbury', 1, 0, 4, 0, 2, False),
    TradePost('Oxford', 2, 0, 0, 2, 2, False),
    TradePost('Gloucester', 2, 0, 0, 2, 2, True),
]

ROAD_LOCATIONS = [
    RoadLocation(['Warrington', 'Stoke-On-Trent']),
    RoadLocation(['Stoke-On-Trent', 'Leek']),
    RoadLocation(['Leek', 'Belper'], False),
    RoadLocation(['Belper', 'Derby']),
    RoadLocation(['Derby', 'Nottingham']),
    RoadLocation(['Derby', 'Uttoxeter'], False),
    RoadLocation(['Derby', 'Burton-Upon-Trent']),
    RoadLocation(['Stoke-On-Trent', 'Stone']),
    RoadLocation(['Stone', 'Uttoxeter'], False),
    RoadLocation(['Stone', 'Stafford']),
    RoadLocation(['Stone', 'Burton-Upon-Trent']),
    RoadLocation(['Stafford', 'Cannock']),
    RoadLocation(['Cannock', 'Burton-Upon-Trent'], False),
    RoadLocation(['Tamworth', 'Burton-Upon-Trent']),
    RoadLocation(['Walsall', 'Burton-Upon-Trent'], canBuildRailroad=False),
    RoadLocation(['beer1', 'Cannock']),
    RoadLocation(['Wolverhampton', 'Cannock']),
    RoadLocation(['Walsall', 'Cannock']),
    RoadLocation(['Wolverhampton', 'Coalbrookdale']),
    RoadLocation(['Shrewbury', 'Coalbrookdale']),
    RoadLocation(['Kidderminster', 'Coalbrookdale']),
    RoadLocation(['Kidderminster', 'Dudley']),
    RoadLocation(['Wolverhampton', 'Walsall']),
    RoadLocation(['Wolverhampton', 'Dudley']),
    RoadLocation(['Tamworth', 'Walsall'], False),
    RoadLocation(['Nuneaton', 'Walsall']),
    RoadLocation(['Nuneaton', 'Coventry']),
    RoadLocation(['Cannock', 'Walsall']),
    RoadLocation(['Birmingham', 'Walsall']),
    RoadLocation(['Birmingham', 'Tamworth']),
    RoadLocation(['Birmingham', 'Nuneaton'], False),
    RoadLocation(['Birmingham', 'Coventry']),
    RoadLocation(['Birmingham', 'Oxford']),
    RoadLocation(['Birmingham', 'Redditch'], False),
    RoadLocation(['Birmingham', 'Worcester']),
    RoadLocation(['Birmingham', 'Dudley']),
    RoadLocation(['Redditch', 'Oxford']),
    RoadLocation(['Redditch', 'Gloucester']),
    RoadLocation(['Worcester', 'Gloucester']),
    RoadLocation(['Worcester', 'beer2', 'Kidderminster']),
]

BUILDINGS = [
    MarketBuilding('goods', 1, 8, 1, 0, 1, 3, 5, 2, onlyPhaseOne=True),
    MarketBuilding('goods', 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding('goods', 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding('goods', 3, 12, 2, 0, 0, 4, 4, 0),
    MarketBuilding('goods', 4, 8, 0, 1, 1, 3, 6, 1),
    MarketBuilding('goods', 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding('goods', 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding('goods', 6, 20, 0, 0, 1, 7, 6, 1),
    MarketBuilding('goods', 7, 16, 1, 1, 0, 9, 4, 0),
    MarketBuilding('goods', 8, 20, 0, 2, 1, 11, 1, 1),
    MarketBuilding('cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding('cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding('cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding('cotton', 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding('cotton', 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding('cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding('cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding('cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding('cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding('cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding('cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding('pottery', 1, 17, 0, 1, 1, 10, 5, 1, canBeDeveloped=False),
    MarketBuilding('pottery', 2, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding('pottery', 3, 22, 2, 0, 2, 11, 5, 1, canBeDeveloped=False),
    MarketBuilding('pottery', 4, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding('pottery', 5, 24, 2, 0, 2, 20, 5, 1, onlyPhaseTwo=True),
    IndustryBuilding('oil', 1, 4, 5, 1, 0, 3, 3, 1, onlyPhaseOne=True),
    IndustryBuilding('oil', 2, 4, 7, 1, 0, 5, 3, 1),
    IndustryBuilding('oil', 3, 5, 9, 1, 0, 7, 2, 1),
    IndustryBuilding('oil', 4, 6, 12, 1, 0, 9, 1, 1),
    IndustryBuilding('beer', 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding('beer', 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding('beer', 2, 1, 7, 0, 1, 5, 5, 2), #add logic somewhere to add +1 beer to tier ^2 in second phase
    IndustryBuilding('beer', 2, 1, 7, 0, 1, 5, 5, 2),
    IndustryBuilding('beer', 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding('beer', 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding('beer', 4, 1, 9, 0, 1, 10, 5, 2),
    IndustryBuilding('coal', 1, 2, 5, 0, 0, 1, 4, 2, onlyPhaseOne=True),
    IndustryBuilding('coal', 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding('coal', 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding('coal', 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding('coal', 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding('coal', 4, 5, 10, 0, 1, 4, 5, 1),
    IndustryBuilding('coal', 4, 5, 10, 0, 1, 4, 5, 1)
]

"""
Starting deck

Key is (str) amount of players playing
"""
STARTING_CARDS = {
    '2': [
        LocationCard('Stafford'),
        LocationCard('Stafford'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Cannock'),
        LocationCard('Cannock'),
        LocationCard('Tamworth'),
        LocationCard('Walsall'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Dudley'),
        LocationCard('Dudley'),
        LocationCard('Kidderminster'),
        LocationCard('Kidderminster'),
        LocationCard('Wolverhampton'),
        LocationCard('Wolverhampton'),
        LocationCard('Worcester'),
        LocationCard('Worcester'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Nuneaton'),
        LocationCard('Redditch'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Coal Mine'),
        IndustryCard('Coal Mine'),
        IndustryCard('Pottery'),
        IndustryCard('Pottery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery')
    ],
    '3': [
        LocationCard('Leek'),
        LocationCard('Leek'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stone'),
        LocationCard('Stone'),
        LocationCard('Uttoxeter'),
        LocationCard('Stafford'),
        LocationCard('Stafford'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Cannock'),
        LocationCard('Cannock'),
        LocationCard('Tamworth'),
        LocationCard('Walsall'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Dudley'),
        LocationCard('Dudley'),
        LocationCard('Kidderminster'),
        LocationCard('Kidderminster'),
        LocationCard('Wolverhampton'),
        LocationCard('Wolverhampton'),
        LocationCard('Worcester'),
        LocationCard('Worcester'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Nuneaton'),
        LocationCard('Redditch'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Coal Mine'),
        IndustryCard('Coal Mine'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Pottery'),
        IndustryCard('Pottery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery')
    ],
    '4': [
        LocationCard('Belper'),
        LocationCard('Belper'),
        LocationCard('Derby'),
        LocationCard('Derby'),
        LocationCard('Derby'),
        LocationCard('Leek'),
        LocationCard('Leek'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stoke-On-Trent'),
        LocationCard('Stone'),
        LocationCard('Stone'),
        LocationCard('Uttoxeter'),
        LocationCard('Uttoxeter'),
        LocationCard('Stafford'),
        LocationCard('Stafford'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Burton-Upon-Trent'),
        LocationCard('Cannock'),
        LocationCard('Cannock'),
        LocationCard('Tamworth'),
        LocationCard('Walsall'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Coalbrookdale'),
        LocationCard('Dudley'),
        LocationCard('Dudley'),
        LocationCard('Kidderminster'),
        LocationCard('Kidderminster'),
        LocationCard('Wolverhampton'),
        LocationCard('Wolverhampton'),
        LocationCard('Worcester'),
        LocationCard('Worcester'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Birmingham'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Coventry'),
        LocationCard('Nuneaton'),
        LocationCard('Redditch'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Iron Works'),
        IndustryCard('Coal Mine'),
        IndustryCard('Coal Mine'),
        IndustryCard('Coal Mine'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Cotton'),
        IndustryCard('Pottery'),
        IndustryCard('Pottery'),
        IndustryCard('Pottery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery'),
        IndustryCard('Brewery')
    ]
}

STARTING_WILD_LOCATION_CARDS = [
    #idk how many wilds there are
    LocationCard('Wild location', True),
    LocationCard('Wild location', True),
    LocationCard('Wild location', True),
    LocationCard('Wild location', True),
    LocationCard('Wild location', True),
]

STARTING_WILD_BUILDING_CARDS = [
    IndustryCard('Wild building', True),
    IndustryCard('Wild building', True),
    IndustryCard('Wild building', True),
    IndustryCard('Wild building', True),
    IndustryCard('Wild building', True),
]