import random


class Player():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.hand = Hand()


class Card():
    def __init__(self, id, suit, name):
        self.id = id
        self.suit = suit
        self.name = name


class Deck():
    def __init__(self):
        self.create()

    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self, howmany=1):
        return [self.cards.pop(0) for idx in range(howmany)]

    def draw(self, n):
        drawn = []
        for x in range(n):
            drawn.append(self.cards.pop())
        return drawn

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def create(self):
        self.cards = [
            Card(1, "Gula", "VII"),
            Card(2, "Gula", "VIII"),
            Card(3, "Gula", "IX"),
            Card(4, "Gula", "X"),
            Card(5, "Gula", "Niznik"),
            Card(6, "Gula", "Vysnik"),
            Card(7, "Gula", "Kral"),
            Card(8, "Gula", "Eso"),

            Card(9, "Zalud", "VII"),
            Card(10, "Zalud", "VIII"),
            Card(11, "Zalud", "IX"),
            Card(12, "Zalud", "X"),
            Card(13, "Zalud", "Niznik"),
            Card(14, "Zalud", "Vysnik"),
            Card(15, "Zalud", "Kral"),
            Card(16, "Zalud", "Eso"),

            Card(17, "Zelen", "VII"),
            Card(18, "Zelen", "VIII"),
            Card(19, "Zelen", "IX"),
            Card(20, "Zelen", "X"),
            Card(21, "Zelen", "Niznik"),
            Card(22, "Zelen", "Vysnik"),
            Card(23, "Zelen", "Kral"),
            Card(24, "Zelen", "Eso"),

            Card(25, "Cerven", "VII"),
            Card(26, "Cerven", "VIII"),
            Card(27, "Cerven", "IX"),
            Card(28, "Cerven", "X"),
            Card(29, "Cerven", "Niznik"),
            Card(30, "Cerven", "Vysnik"),
            Card(31, "Cerven", "Kral"),
            Card(32, "Cerven", "Eso"),
        ]
        self.shuffle()

    def size(self):
        return len(self.cards)


class Hand():
    def __init__(self):
        self.cards = []

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def size(self):
        return len(self.cards)

    def pick(self, id):
        for i, c in enumerate(self.cards):
            if c.id == id:
                self.cards.pop(i)
                return c

    def playable(self, tableCard):
        playable = []
        for i, c in enumerate(self.cards):
            if c.suit == tableCard.suit:
                playable.append(self.cards[i])
            if c.name == tableCard.name:
                playable.append(self.cards[i])
        return playable


class Game():
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.tableCard = None
        self.playedCards = []

# Development test


""" deck = Deck()
hand = Hand()

tableCard = deck.cards.pop()
hand.add(deck.pop(5))

print("Otocena:", tableCard.name, tableCard.suit)
print("V decku:", len(deck.cards))
print("V ruke", len(hand.cards))

mozedat = hand.playable(tableCard)

for card in mozedat:
    print("Mozem dat: ", card.name, card.suit) """
