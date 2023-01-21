from python.print_colors import prGreen

from .card import Card
from .enums import CardName, CardType


class IndustryCard(Card):
    def __init__(self, name: CardName):
        super(IndustryCard, self).__init__(CardType.industry, name=name)
        self.isWild = name == CardName.wild_industry

    def __str__(self) -> str:
        if self.isWild:
            return self.name
        return prGreen(self.name)

    def __repr__(self) -> str:
        return str(self)
