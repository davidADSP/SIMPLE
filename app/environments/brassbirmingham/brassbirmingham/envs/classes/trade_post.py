from ..python.id import id


class TradePost:
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

    def __init__(
        self,
        name,
        beerAmount,
        moneyGained,
        victoryPointsGained,
        incomeGained,
        networkPoints,
        canDevelop,
    ):
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
