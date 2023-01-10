import random
import uuid

class Player():
    def __init__(self, id):
        self.id = id
        self.hand = Hand()
        self.money = 17
        self.income = 0
        self.victoryPoints = 0
        self.spentThisTurn = 0
        self.buildingsAvailable = BUILDINGS #buildings available to build, array of Building objects
        self.roadsAvailable = [Canal(id())]*STARTING_ROADS #canals/railroads available to build, array of Road objects

"""
CARDS
"""
class Card():
    """
    Card object

    :param id: id
    :param type: any of ['location', 'industry', 'wild']
    :param name: name of location or industry
    """
    def __init__(self, id):
        self.id = id

class LocationCard(Card):
    def __init__(self, id, type, name):
        super(LocationCard, self).__init__(id)
        self.type = type
        self.name = name

class IndustryCard(Card):
    def __init__(self, id, type, name):
        super(IndustryCard, self).__init__(id)
        self.type = type
        self.name = name

class WildCard(Card):
    def __init__(self, id, type):
        super(WildCard, self).__init__(id)
        self.type = type

class Hand():
    """
    Hand object
    
    :param id: id
    :param deck: Deck object"""
    def __init__(self, id, deck):
        self.cards = []
        self.deck = deck

    def draw(self):
        self.cards.append(self.deck.draw())
    
    def spendCard(self, card):
        self.cards = list(filter(lambda x: x.id != card.id, self.cards)) #remove that card from hand
        self.deck.discardPile.append(card)

    """
    getTotal
    
    :return: amount of cards in hand
    """
    def getTotal(self):
        return len(self.cards)

class Deck():
    """
    Deck object
    
    :param id: id
    :param discardPile: array of discarded Card objects
    """
    def __init__(self, id, discardPile):
        self.cards = []
        self.discardPile = []

    def shuffle(self):
        self.cards = random.shuffle(self.cards)

    def draw(self):
        if len(self.cards > 0):
            return self.cards.pop()
        else:
            self.reset()

    def reset(self):
        self.cards = self.discardPile
        self.discardPile = []
        self.shuffle()

"""
BUILDINGS
"""
class Building():
    """
    Building object
    
    :param id: id
    :param name: any of [goods, cotton, pottery]
    :param tier: ex: 3
    :param cost: cost
    :param coalCost: ex: 1
    :param ironCost: ironCost
    :param victoryPointsGained: victory points gained from selling
    :param incomeGained: income gained from selling
    :param linkPoints: amount of points each road gets during counting step
    :param canBeDeveloped=True:
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """
    def __init__(self, id, type, name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, linkPoints, canBeDeveloped, onlyPhaseOne, onlyPhaseTwo):
        self.id = id
        self.type = type
        self.name = name
        self.tier = tier
        self.cost = cost
        self.coalCost = coalCost
        self.ironCost = ironCost
        self.victoryPointsGained = victoryPointsGained
        self.incomeGained = incomeGained
        self.linkPoints = linkPoints
        self.canBeDeveloped = canBeDeveloped
        self.onlyPhaseOne = onlyPhaseOne
        self.onlyPhaseTwo = onlyPhaseTwo
        self.canBeDeveloped = True
        self.onlyPhaseOne = False #can only be built during phase 1
        self.onlyPhaseTwo = False #can only be built during phase 2

        isActive = False # is on the board i.e., not bought yet
        isRetired = False # only used for retired buildings (tier 1's) in second phase
        
    
class MarketBuilding(Building):
    """
    Market Building
    
    :param id: id
    :param name: any of [goods, cotton, pottery]
    :param tier: ex: 3
    :param cost: cost
    :param coalCost: ex: 1
    :param ironCost: ironCost
    :param beerCostToSell: amount of beer required to sell
    :param victoryPointsGained: victory points gained from selling
    :param incomeGained: income gained from selling
    :param linkPoints: amount of points each road gets during counting step
    :param canBeDeveloped=True:
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """
    def __init__(self, id, name, tier, cost, coalCost, ironCost, beerCostToSell, victoryPointsGained, incomeGained, linkPoints, canBeDeveloped=True, onlyPhaseOne=False, onlyPhaseTwo=False):
        super(MarketBuilding, self).__init__(id, 'market', name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, linkPoints, canBeDeveloped, onlyPhaseOne, onlyPhaseTwo)
        self.beerCostToSell = beerCostToSell

class IndustryBuilding(Building):
    """
    Industry Building
    
    :param id: id
    :param name: any of [oil, coal, beer]
    :param tier: ex: 3
    :param resourceAmount: current resource amount on building
    :param cost: cost
    :param coalCost:
    :param ironCost:
    :param victoryPointsGained: victory points gained from flipping
    :param incomeGained: income gained from flipping
    :param linkPoints: amount of points each road gets during counting step
    :param onlyPhaseOne=False:
    :param onlyPhaseTwo=False:
    """
    def __init__(self, id, name, tier, resourceAmount, cost, coalCost, ironCost, victoryPointsGained, incomeGained, linkPoints, onlyPhaseOne=False, onlyPhaseTwo=False):
        super(IndustryBuilding, self).__init__(id, 'industry', name, tier, cost, coalCost, ironCost, victoryPointsGained, incomeGained, linkPoints, True, onlyPhaseOne, onlyPhaseTwo)
        self.resourceAmount = resourceAmount
        self.resourcesType = name

class Road():
    def __init__(self, id, type):
        self.id = id
        self.type = type

class Canal(Road):
    def __init__(self, id):
        super(Canal, self).__init__(id, 'canal')
        self.cost = 3

class Railroad(Road):
    def __init__(self, id):
        super(Railroad, self).__init__(id, 'railroad')
        #todo cost

"""
BOARD
"""
class Board():
    def __init__(self, id):
        self.id = id
        self.towns = [] #array of Town objects
        self.coalRemaining = 15 #is this right tyler? double check plz
        self.coalMarketPrice = 1
        self.ironRemaining = 8 #also this
        self.ironMarketPrice = 1
        self.players = [] #array of Player objects
    
    def addPlayer(self, player):
        self.players.append(player)

class Town():
    """
    Town
    
    :param id: id
    :param color: any of ['blue', 'green', 'red', 'yellow', 'purple']
    :param name: name
    :param buildLocation: array of BuildLocation objects"""
    def __init__(self, id, color, name, buildLocations):
        self.id = id
        self.color = color
        self.name = name
        self.buildLocations = buildLocations

class BuildLocation():
    """
    BuildLocation - Town may have multiple build locations

    :param id: id
    :param possibleBuilds: possible buildings which can be built, any array of [cotton, beer, coal, oil, pot, goods]
    """
    def __init__(self, id, possibleBuilds):
        self.id = id
        self.possibleBuilds = possibleBuilds
        self.isBuilt = False

class TradePost():
    """
    TradePost
    
    :param id: id
    :param name: name
    :param beerAmount: amount of starting beer
    :param possibleTrades: trades which are possible to make, array of Building object names 'oil', 'goods', etc...
    :param linkPoints: amount of points each road gets during counting step
    """
    def __init__(self, id, name, beerAmount, possibleTrades, linkPoints):
        self.id = id
        self.name = name
        self.beerAmount = beerAmount
        self.possibleTrades = possibleTrades
        self.linkPoints = linkPoints

def id():
    return uuid.uuid1()

STARTING_ROADS = 14
TOWNS = [
    Town(id(), 'blue', 'Leek', [BuildLocation(id(), ['cotton', 'goods']), BuildLocation(id(), ['cotton', 'coal'])]),
    Town(id(), 'blue', 'Stoke-On-Trent', [BuildLocation(id(), ['cotton', 'goods']), BuildLocation(id(), ['pottery', 'oil']), BuildLocation(id(), ['goods'])]),
    Town(id(), 'blue', 'Stone', [BuildLocation(id(), ['cotton', 'beer']), BuildLocation(id(), ['goods', 'coal'])]),
    Town(id(), 'blue', 'Uttoxeter', [BuildLocation(id(), ['goods', 'beer']), BuildLocation(id(), ['cotton', 'beer'])]),
    Town(id(), 'green', 'Belper', [BuildLocation(id(), ['cotton', 'goods']), BuildLocation(id(), ['coal']), BuildLocation(id(), ['pottery'])]),
    Town(id(), 'green', 'Derby', [BuildLocation(id(), ['cotton', 'beer']), BuildLocation(id(), ['cotton', 'goods']), BuildLocation(id(), ['oil'])]),
    Town(id(), 'red', 'Stafford', [BuildLocation(id(), ['goods', 'beer']), BuildLocation(id(), ['pottery'])]),
    Town(id(), 'red', 'Burton-Upon-Trent', [BuildLocation(id(), ['goods', 'coal']), BuildLocation(id(), ['beer'])]),
    Town(id(), 'beer1', '', [BuildLocation(id(), ['beer'])]),
    Town(id(), 'red', 'Cannock', [BuildLocation(id(), ['goods', 'coal']), BuildLocation(id(), ['coal'])]),
    Town(id(), 'red', 'Tamworth', [BuildLocation(id(), ['cotton', 'coal']), BuildLocation(id(), ['cotton', 'coal'])]),
    Town(id(), 'red', 'Walsall', [BuildLocation(id(), ['oil', 'goods']), BuildLocation(id(), ['goods', 'beer'])]),
    Town(id(), 'yellow', 'Coalbrookdale', [BuildLocation(id(), ['oil', 'beer']), BuildLocation(id(), ['oil']), BuildLocation(id(), ['coal'])]),
    Town(id(), 'yellow', 'Wolverhampton', [BuildLocation(id(), ['goods']), BuildLocation(id(), ['goods', 'coal'])]),
    Town(id(), 'yellow', 'Dudley', [BuildLocation(id(), ['coal']), BuildLocation(id(), ['oil'])]),
    Town(id(), 'yellow', 'Kidderminster', [BuildLocation(id(), ['cotton', 'coal']), BuildLocation(id(), ['cotton'])]),
    Town(id(), 'beer2', '', [BuildLocation(id(), ['beer'])]),
    Town(id(), 'yellow', 'Worcester', [BuildLocation(id(), ['cotton']), BuildLocation(id(), ['cotton'])]),
    Town(id(), 'purple', 'Birmingham', [BuildLocation(id(), ['cotton', 'goods']), BuildLocation(id(), ['goods']), BuildLocation(id(), ['oil']), BuildLocation(id(), ['goods'])]),
    Town(id(), 'purple', 'Nuneaton', [BuildLocation(id(), ['goods', 'beer']), BuildLocation(id(), ['cotton', 'coal'])]),
    Town(id(), 'purple', 'Coventry', [BuildLocation(id(), ['pottery']), BuildLocation(id(), ['goods', 'coal']), BuildLocation(id(), ['oil', 'goods'])]),
    Town(id(), 'purple', 'Redditch', [BuildLocation(id(), ['goods', 'coal']), BuildLocation(id(), ['oil'])])
]

BUILDINGS = [
    MarketBuilding(id(), 'goods', 1, 8, 1, 0, 1, 3, 5, 2, onlyPhaseOne=True),
    MarketBuilding(id(), 'goods', 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(id(), 'goods', 2, 10, 0, 1, 1, 5, 0, 1),
    MarketBuilding(id(), 'goods', 3, 12, 2, 0, 0, 4, 4, 0),
    MarketBuilding(id(), 'goods', 4, 8, 0, 1, 1, 3, 6, 1),
    MarketBuilding(id(), 'goods', 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(id(), 'goods', 5, 16, 1, 0, 2, 8, 2, 2),
    MarketBuilding(id(), 'goods', 6, 20, 0, 0, 1, 7, 6, 1),
    MarketBuilding(id(), 'goods', 7, 16, 1, 1, 0, 9, 4, 0),
    MarketBuilding(id(), 'goods', 8, 20, 0, 2, 1, 11, 1, 1),
    MarketBuilding(id(), 'cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(id(), 'cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(id(), 'cotton', 1, 12, 0, 0, 1, 5, 5, 1, onlyPhaseOne=True),
    MarketBuilding(id(), 'cotton', 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(id(), 'cotton', 2, 14, 1, 0, 1, 5, 4, 2),
    MarketBuilding(id(), 'cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(id(), 'cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(id(), 'cotton', 3, 16, 1, 1, 1, 9, 3, 1),
    MarketBuilding(id(), 'cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(id(), 'cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(id(), 'cotton', 4, 18, 1, 1, 1, 12, 2, 1),
    MarketBuilding(id(), 'pottery', 1, 17, 0, 1, 1, 10, 5, 1, canBeDeveloped=False),
    MarketBuilding(id(), 'pottery', 2, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(id(), 'pottery', 3, 22, 2, 0, 2, 11, 5, 1, canBeDeveloped=False),
    MarketBuilding(id(), 'pottery', 4, 0, 1, 0, 1, 1, 1, 1),
    MarketBuilding(id(), 'pottery', 5, 24, 2, 0, 2, 20, 5, 1, onlyPhaseTwo=True),
    IndustryBuilding(id(), 'oil', 1, 4, 5, 1, 0, 3, 3, 1, onlyPhaseOne=True),
    IndustryBuilding(id(), 'oil', 2, 4, 7, 1, 0, 5, 3, 1),
    IndustryBuilding(id(), 'oil', 3, 5, 9, 1, 0, 7, 2, 1),
    IndustryBuilding(id(), 'oil', 4, 6, 12, 1, 0, 9, 1, 1),
    IndustryBuilding(id(), 'beer', 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(id(), 'beer', 1, 1, 5, 0, 1, 4, 4, 2),
    IndustryBuilding(id(), 'beer', 2, 1, 7, 0, 1, 5, 5, 2), #add logic somewhere to add +1 beer to tier ^2 in second phase
    IndustryBuilding(id(), 'beer', 2, 1, 7, 0, 1, 5, 5, 2),
    IndustryBuilding(id(), 'beer', 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(id(), 'beer', 3, 1, 9, 0, 1, 7, 5, 2),
    IndustryBuilding(id(), 'beer', 4, 1, 9, 0, 1, 10, 5, 2),
    IndustryBuilding(id(), 'coal', 1, 2, 5, 0, 0, 1, 4, 2, onlyPhaseOne=True),
    IndustryBuilding(id(), 'coal', 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(id(), 'coal', 2, 3, 7, 0, 0, 2, 7, 1),
    IndustryBuilding(id(), 'coal', 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(id(), 'coal', 3, 4, 8, 0, 1, 3, 6, 1),
    IndustryBuilding(id(), 'coal', 4, 5, 10, 0, 1, 4, 5, 1),
    IndustryBuilding(id(), 'coal', 4, 5, 10, 0, 1, 4, 5, 1)
]