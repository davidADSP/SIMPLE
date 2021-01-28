import random

class Player():
    def __init__(self, id):
        self.id = id
        self.score = 0

class Tile():
    def __init__(self, id, order, name):
        self.id = id
        self.order = order
        self.name = name
        
class Butterfly(Tile):
    def __init__(self, id, order, name, colour):
        super(Butterfly, self).__init__(id, order, name)
        self.colour = colour
        self.type = 'butterfly'
        self.symbol = colour + 'BU'

class Flower(Tile):
    def __init__(self, id, order, name):
        super(Flower, self).__init__(id, order, name)
        self.type = 'flower'
        self.symbol = 'FLO'
        
class Dragonfly(Tile):
    def __init__(self, id, order, name):
        super(Dragonfly, self).__init__(id, order, name)
        self.type = 'dragonfly'
        self.symbol = 'DRA'

class LightningBug(Tile):
    def __init__(self, id, order, name):
        super(LightningBug, self).__init__(id, order, name)
        self.type = 'lightningbug'
        self.symbol = f'LIB'
        
class Cricket(Tile):
    def __init__(self, id, order, name):
        super(Cricket, self).__init__(id, order, name)
        self.type = 'cricket'
        self.symbol = f'CRI'


class Bee(Tile):
    def __init__(self, id, order, name):
        super(Bee, self).__init__(id, order, name)
        self.type = 'bee'
        self.symbol = f'BEE'

class Honeycomb(Tile):
    def __init__(self, id, order, name):
        super(Honeycomb, self).__init__(id, order, name)
        self.type = 'honeycomb'
        self.symbol = f'HON'
    
class Wasp(Tile):
    def __init__(self, id, order, name):
        super(Wasp, self).__init__(id, order, name)
        self.type = 'wasp'
        self.symbol = f'WAS'



        
       
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

