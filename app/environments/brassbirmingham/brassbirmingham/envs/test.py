from classes import *

NUM_PLAYERS = 2
board = Board(NUM_PLAYERS)
p1 = Player("Noah", board)
p2 = Player("Tyler", board)

# print(p1)
# print(p1.buildings)
print(board.towns)
# print(p1.roads)
# print(board.deck)
assert p1.buildings[0].name == "goods"
assert len(p1.buildings) == 44

assert board.towns[0].name == "Leek"

town1 = board.towns[4]
town2 = board.towns[12]

assert board.areNetworked(town1, town2) == False
