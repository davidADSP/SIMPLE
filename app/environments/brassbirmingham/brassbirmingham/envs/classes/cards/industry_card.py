from .card import Card
from ...python.print_colors import prGreen


class IndustryCard(Card):
    def __init__(self, name, isWild=False):
        super(IndustryCard, self).__init__("building")
        self.name = name
        self.isWild = isWild

    def __str__(self):
        if self.isWild:
            return self.name
        return prGreen(self.name)

    def __repr__(self):
        return str(self)
