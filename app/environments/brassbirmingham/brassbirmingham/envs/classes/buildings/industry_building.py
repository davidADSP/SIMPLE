from .building import Building


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

    def __init__(
        self,
        name,
        tier,
        resourceAmount,
        cost,
        coalCost,
        ironCost,
        victoryPointsGained,
        incomeGained,
        networkPoints,
        onlyPhaseOne=False,
        onlyPhaseTwo=False,
    ):
        super(IndustryBuilding, self).__init__(
            "industry",
            name,
            tier,
            cost,
            coalCost,
            ironCost,
            victoryPointsGained,
            incomeGained,
            networkPoints,
            True,
            onlyPhaseOne,
            onlyPhaseTwo,
        )
        self.resourceAmount = resourceAmount
        self.resourcesType = name
