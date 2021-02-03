import random

class Player():
    def __init__(self, id):
        self.id = id
        self.position = Position()

class Tile():
    def __init__(self, id, order, name):
        self.id = id
        self.order = order
        self.name = name
        
class Butterfly(Tile):
    def __init__(self, id, order, name, colour, value):
        super(Butterfly, self).__init__(id, order, name)
        self.colour = colour
        self.value = value
        self.type = f'{colour}butterfly'
        if colour == 'G':
            colour_icon = '🟢'
        elif colour == 'B':
            colour_icon = '🔵'
        elif colour == 'Y':
            colour_icon = '🟡'
        elif colour == 'R':
            colour_icon = '🔴'
            
        self.symbol = f'{colour_icon}{value}' if value > 0 else f'{colour_icon}X'

class Flower(Tile):
    def __init__(self, id, order, name):
        super(Flower, self).__init__(id, order, name)
        self.type = 'flower'
        self.symbol = '🌼'
        
class Dragonfly(Tile):
    def __init__(self, id, order, name, value):
        super(Dragonfly, self).__init__(id, order, name)
        self.value = value
        self.type = 'dragonfly'
        self.symbol = f'🐲{value}'

class LightningBug(Tile):
    def __init__(self, id, order, name, value):
        super(LightningBug, self).__init__(id, order, name)
        self.value = value
        self.type = 'lightningbug'
        self.symbol = f'⚡️{value}'
        
class Cricket(Tile):
    def __init__(self, id, order, name, value):
        super(Cricket, self).__init__(id, order, name)
        self.value = value
        self.type = 'cricket'
        self.symbol = f'🏏{value}'


class Bee(Tile):
    def __init__(self, id, order, name):
        super(Bee, self).__init__(id, order, name)
        self.type = 'bee'
        self.value = -3
        self.symbol = 'BEE'


class Honeycomb(Tile):
    def __init__(self, id, order, name, value):
        super(Honeycomb, self).__init__(id, order, name)
        self.value = value
        self.type = 'honeycomb'
        self.symbol = f'🍯{value}'
    
class Wasp(Tile):
    def __init__(self, id, order, name, value):
        super(Wasp, self).__init__(id, order, name)
        self.value = value
        self.type = 'wasp'
        self.symbol = f'🐝{value}'



        
       
class DrawBag():
    def __init__(self, contents):
        self.contents = contents
        self.create()
    
    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self, n):
        drawn = []
        for x in range(n):
            drawn.append(self.tiles.pop())
        return drawn
    
    def add(self, tiles):
        for tile in tiles:
            self.tiles.append(tile)

    def create(self):
        self.tiles = []

        tile_id = 0
        for order, x in enumerate(self.contents):
            x['info']['order'] = order
            for i in range(x['count']):
                x['info']['id'] = tile_id
                self.add([x['tile'](**x['info'])])
                tile_id += 1
                
        self.shuffle()
                
    def size(self):
        return len(self.tiles)

  


class Position():
    def __init__(self):
        self.tiles = []  
    
    def add(self, tiles):
        for tile in tiles:
            self.tiles.append(tile)
    
    def size(self):
        return len(self.tiles)

    @property
    def score(self):
        score = 0
        #BUTTERFLIES
        for colour in ['R','B','G','Y']:
            tile_values = [t.value for t in self.tiles if t.type == f'{colour}butterfly']
            s = sum(tile_values)
            if 0 in tile_values:
                s *= 2
            
            score += s
        
        #FLOWERS
        count = len([t for t in self.tiles if t.type == f'flower'])
        score += pow(count, 2)

        #DRAGONFLY
        drag = [t.value for t in self.tiles if t.type == f'dragonfly']
        if len(drag) > 0:
            score += max(drag)

        #LIGHTNINGBUG
        lb = [t.value for t in self.tiles if t.type == f'lightningbug']
        if len(lb) > 0:
            score += min(lb)

        #CRICKET
        cricket = [t.value for t in self.tiles if t.type == f'cricket']
        if len(cricket) > 0:
            score += cricket[-1]

        #BEE / HONEYCOMB
        bees = [t.value for t in self.tiles if t.type == f'bee']
        honeycomb = sorted([t.value for t in self.tiles if t.type == f'honeycomb'], reverse = True)

        score += sum(honeycomb[:len(bees)])
        score += sum(bees[len(honeycomb):])

        #WASP
        score += sum([t.value for t in self.tiles if t.type == f'wasp'])


        return score
        


class Board():
    def __init__(self, size):
        self.size = size
        self.squares = size * size
        self.tiles = [None] * self.squares 
        self.nets = [False] * self.squares 
        self.hudson = 0
        self.hudson_facing = 'R'
    
    def add_net(self, position):
        self.nets[position] = True
    
    def remove(self, position):
        tile = self.tiles[position]
        self.tiles[position] = None
        return tile

    def fill(self, tiles):
        self.tiles = tiles


