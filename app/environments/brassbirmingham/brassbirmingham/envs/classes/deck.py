import random
from typing import List

from python.id import id

from .cards.card import Card


class Deck:
    """
    Deck object

    :param cards: array of Card objects
    """

    def __init__(self, cards: List[Card]):
        self.id = id()
        self.cards = cards
        self.discardPile = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards > 0):
            return self.cards.pop()
        else:
            self.reset()

    def reset(self):
        self.cards = self.discardPile
        self.discardPile = []
        self.shuffle()

    def __str__(self) -> str:
        return str(self.cards)
