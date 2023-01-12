class Hand:
    """
    Hand object

    :param deck: Deck object"""

    def __init__(self, deck):
        self.id = id()
        self.cards = []
        self.deck = deck

    def draw(self):
        self.cards.append(self.deck.draw())

    def spendCard(self, card):
        self.cards = list(
            filter(lambda x: x.id != card.self.cards, self.cards)
        )  # remove that card from hand
        self.deck.discardPile.append(card)

    """
    getTotal
    
    :return: amount of cards in hand
    """

    def getTotal(self):
        return len(self.cards)

    def __repr__(self):
        return self.cards
