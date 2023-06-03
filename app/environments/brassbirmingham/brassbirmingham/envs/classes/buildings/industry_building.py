from .building import Building
from .enums import BuildingName, BuildingType


class IndustryBuilding(Building):
    """
    Industry Building - industry baby!

    :param name: any of [iron, coal, beer]
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
        name: BuildingName,
        tier: int,
        resourceAmount: int,
        cost: int,
        coalCost: int,
        ironCost: int,
        victoryPointsGained: int,
        incomeGained: int,
        networkPoints: int,
        onlyPhaseOne=False,
        onlyPhaseTwo=False,
    ):
        super(IndustryBuilding, self).__init__(
            BuildingType.industry,
            name,
            tier,
            cost,
            coalCost,
            ironCost,
            victoryPointsGained,
            incomeGained,
            networkPoints,
            canBeDeveloped=True,
            onlyPhaseOne=onlyPhaseOne,
            onlyPhaseTwo=onlyPhaseTwo,
        )
        self.resourceAmount = resourceAmount
        self.resourcesType = name

    def decreaseResourceAmount(self, amount: int):
        assert amount <= self.resourceAmount
        self.resourceAmount -= amount

        self.isFlipped = self.resourceAmount == 0
