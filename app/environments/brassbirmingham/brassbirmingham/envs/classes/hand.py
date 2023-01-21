from typing import List

from python.id import id

from .cards.card import Card
from .deck import Deck


class Hand:
    """
    Hand object

    :param deck: Deck object"""

    def __init__(self, deck: Deck):
        self.id = id()
        self.cards: List[Card] = []
        self.deck = deck

    def draw(self):
        self.cards.append(self.deck.draw())

    def spendCard(self, card: Card):
        self.cards = list(
            filter(lambda x: x.id != card.self.cards, self.cards)
        )  # remove that card from hand
        self.deck.discardPile.append(card)

    def add(self, card: Card):
        self.cards.append(card)

    """
    getTotal
    
    :return: amount of cards in hand
    """

    def getTotal(self) -> int:
        return len(self.cards)

    def __repr__(self):
        return self.cards
