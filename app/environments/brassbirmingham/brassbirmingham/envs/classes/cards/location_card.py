from .card import Card
from ...python.print_colors import (
    prCyan,
    prGreen,
    prLightGray,
    prPurple,
    prRed,
    prYellow,
)


class LocationCard(Card):
    def __init__(self, name, isWild=False):
        super(LocationCard, self).__init__("location")
        self.name = name
        self.isWild = isWild

    def __str__(self):
        if self.isWild:
            return self.name

        if self.name in ["Stoke-On-Trent", "Leek", "Stone", "Uttoxeter"]:
            return prCyan(self.name)
        elif self.name in ["Belper", "Derby"]:
            return prGreen(self.name)
        elif self.name in [
            "Stafford",
            "Cannock",
            "Walsall",
            "Burton-Upon-Trent",
            "Tamworth",
        ]:
            return prRed(self.name)
        elif self.name in [
            "Wolverhampton",
            "Coalbrookdale",
            "Dudley",
            "Kidderminster",
            "Worcester",
        ]:
            return prYellow(self.name)
        elif self.name in ["Nuneaton", "Birmingham", "Coventry", "Redditch"]:
            return prPurple(self.name)
        elif self.name == "beer1" or self.name == "beer2":
            return prLightGray(self.name)
        return self.name

    def __repr__(self):
        return str(self)
