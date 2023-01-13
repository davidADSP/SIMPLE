from consts import *
from python.print_colors import prCyan, prGreen, prLightGray, prPurple, prRed, prYellow

from .card import Card
from .enums import CardName, CardType


class LocationCard(Card):
    def __init__(self, name: CardName, isWild=False):
        super(LocationCard, self).__init__(CardType.location)
        self.name = name
        self.isWild = isWild

    def __str__(self) -> str:
        if self.isWild:
            return self.name

        if self.name in [STOKE_ON_TRENT, LEEK, STONE, UTTOXETER]:
            return prCyan(self.name)
        elif self.name in [BELPER, DERBY]:
            return prGreen(self.name)
        elif self.name in [
            STAFFORD,
            CANNOCK,
            WALSALL,
            BURTON_UPON_TRENT,
            TAMWORTH,
        ]:
            return prRed(self.name)
        elif self.name in [
            WOLVERHAMPTON,
            COALBROOKDALE,
            DUDLEY,
            KIDDERMINSTER,
            WORCESTER,
        ]:
            return prYellow(self.name)
        elif self.name in [NUNEATON, BIRMINGHAM, COVENTRY, REDDITCH]:
            return prPurple(self.name)
        elif self.name == BEER1 or self.name == BEER2:
            return prLightGray(self.name)
        return self.name

    def __repr__(self) -> str:
        return str(self)
