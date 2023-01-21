from .building import Building
from .enums import BuildingName, BuildingType


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

    def __init__(
        self,
        name: BuildingName,
        tier: int,
        cost: int,
        coalCost: int,
        ironCost: int,
        beerCost: int,
        victoryPointsGained: int,
        incomeGained: int,
        networkPoints: int,
        canBeDeveloped=True,
        onlyPhaseOne=False,
        onlyPhaseTwo=False,
    ):
        super(MarketBuilding, self).__init__(
            BuildingType.market,
            name,
            tier,
            cost,
            coalCost,
            ironCost,
            victoryPointsGained,
            incomeGained,
            networkPoints,
            canBeDeveloped,
            onlyPhaseOne,
            onlyPhaseTwo,
        )
        self.beerCost = beerCost

    def sell(self):
        self.isActive = False
        self.isSold = True
        self.town = None
        self.isFlipped = True
