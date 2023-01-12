from .building import Building


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
        name,
        tier,
        cost,
        coalCost,
        ironCost,
        beerCost,
        victoryPointsGained,
        incomeGained,
        networkPoints,
        canBeDeveloped=True,
        onlyPhaseOne=False,
        onlyPhaseTwo=False,
    ):
        super(MarketBuilding, self).__init__(
            "market",
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
