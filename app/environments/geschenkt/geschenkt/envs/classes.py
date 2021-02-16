import random

class Player():
    def __init__(self, id):
        self.id = id
        self.position = Position()
        self.counters = Counters()

    
    @property
    def score(self):
        score = 0
        current_value = 0
        
        for card in sorted(self.position.cards, key=lambda x: x.id):
            if card.value > current_value + 1:
                score += card.value

            current_value = card.value

        score -= self.counters.size()

        return score


class Card():
    def __init__(self, id, order, value):
        self.id = id
        self.order = order
        self.value = value
        self.symbol = str(value)
               
class Deck():
    def __init__(self, contents):
        self.contents = contents
        self.create()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n):
        drawn = []
        for x in range(n):
            drawn.append(self.cards.pop())
        return drawn
    
    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def create(self):
        self.cards = []

        card_id = 0
        for order, x in enumerate(self.contents):
            x['info']['order'] = order
            for i in range(x['count']):
                x['info']['id'] = card_id
                self.add([x['card'](**x['info'])])
                card_id += 1
                
        self.shuffle()

    def pick(self, symbol):
        for i, c in enumerate(self.cards):
            if c.symbol == symbol:
                self.cards.pop(i)
                return [c]



    def size(self):
        return len(self.cards)


class Counters():
    def __init__(self):
        self.counters = 0
    
    def add(self, n):
        self.counters += n

    def remove(self, n):
        self.counters -= n
    
    def size(self):
        return self.counters
    
    def reset(self):
        self.counters = 0
        
                
class Discard():
    def __init__(self):
        self.cards = []  
    
    def add(self, cards):
        for card in cards:
            self.cards.append(card)
    
    def size(self):
        return len(self.cards)
    
class Position():
    def __init__(self):
        self.cards = []  
    
    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def reset(self):
        self.cards = []
    
    def size(self):
        return len(self.cards)

    def pick(self, name):
        for i, c in enumerate(self.cards):
            if c.name == name:
                self.cards.pop(i)
                return c
