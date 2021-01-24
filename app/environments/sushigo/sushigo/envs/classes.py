import random

class Player():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.hand = Hand()
        self.position = Position()

class Card():
    def __init__(self, id, order, name):
        self.id = id
        self.order = order
        self.name = name
        
class Tempura(Card):
    def __init__(self, id, order, name):
        super(Tempura, self).__init__(id, order, name)
        self.colour = 'purple'
        self.type = 'tempura'
        self.symbol = 'TEM'

class Sashimi(Card):
    def __init__(self, id, order, name):
        super(Sashimi, self).__init__(id, order, name)
        self.colour = 'green'
        self.type = 'sashimi'
        self.symbol = 'SAS'
        
class Dumpling(Card):
    def __init__(self, id, order, name):
        super(Dumpling, self).__init__(id, order, name)
        self.colour = 'blue'
        self.type = 'dumpling'
        self.symbol = 'DUM'

class Maki(Card):
    def __init__(self, id, order, name, value):
        super(Maki, self).__init__(id, order, name)
        self.colour = 'red'
        self.type = 'maki'
        self.value = value
        self.symbol = f'MA{value}'
        
class Nigiri(Card):
    def __init__(self, id, order, name, value):
        super(Nigiri, self).__init__(id, order, name)
        self.colour = 'yellow'
        self.type = 'nigiri'
        self.value = value
        self.played_on_wasabi = False

    @property
    def symbol(self):
        return f"N{self.value}{'W' if self.played_on_wasabi else '-'}"

class Pudding(Card):
    def __init__(self, id, order, name):
        super(Pudding, self).__init__(id, order, name)
        self.colour = 'pink'
        self.type = 'pudding'
        self.symbol = f'PUD'

class Wasabi(Card):
    def __init__(self, id, order, name):
        super(Wasabi, self).__init__(id, order, name)
        self.colour = 'yellow'
        self.type = 'wasabi'
        self.played_upon = False
    
    @property
    def symbol(self):
        return f"WA{'X' if self.played_upon else '-'}"

class Chopsticks(Card):
    def __init__(self, id, order, name):
        super(Chopsticks, self).__init__(id, order, name)
        self.colour = 'lightblue'
        self.type = 'chopsticks'
        self.symbol = f'CHO'
        
       
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
    
    def pick(self, name):
        for i, c in enumerate(self.cards):
            if c.name == name:
                self.cards.pop(i)
                return c
        
                
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
    
    def size(self):
        return len(self.cards)

    def pick(self, name):
        for i, c in enumerate(self.cards):
            if c.name == name:
                self.cards.pop(i)
                return c
