import random


class Player():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.hand = Hand()
        self.position = Position()


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
            Card(5, "Gula", "D"),
            Card(6, "Gula", "H"),
            Card(7, "Gula", "K"),
            Card(8, "Gula", "E"),

            Card(9, "Zalud", "VII"),
            Card(10, "Zalud", "VIII"),
            Card(11, "Zalud", "IX"),
            Card(12, "Zalud", "X"),
            Card(13, "Zalud", "D"),
            Card(14, "Zalud", "H"),
            Card(15, "Zalud", "K"),
            Card(16, "Zalud", "E"),

            Card(17, "Zelen", "VII"),
            Card(18, "Zelen", "VIII"),
            Card(19, "Zelen", "IX"),
            Card(20, "Zelen", "X"),
            Card(21, "Zelen", "D"),
            Card(22, "Zelen", "H"),
            Card(23, "Zelen", "K"),
            Card(24, "Zelen", "E"),

            Card(25, "Cerven", "VII"),
            Card(26, "Cerven", "VIII"),
            Card(27, "Cerven", "IX"),
            Card(28, "Cerven", "X"),
            Card(29, "Cerven", "D"),
            Card(30, "Cerven", "H"),
            Card(31, "Cerven", "K"),
            Card(32, "Cerven", "E"),
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


deck = Deck()
hand = Hand()

tableCard = deck.cards.pop()

hand.add(deck.pop(5))

print("Otocena:", tableCard.name, tableCard.suit)
print("V decku:", len(deck.cards))
print("V ruke", len(hand.cards))
