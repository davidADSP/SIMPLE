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

# test building canal between leek/stoke-on-trent
leek = board.towns[0]
stokeOnTrent = board.towns[1]
assert not board.areNetworked(leek, stokeOnTrent)
print(leek.networks)
assert p1.canBuildCanal(leek.networks[0])
assert not board.areNetworked(leek, stokeOnTrent)
p1.buildCanal(leek.networks[0])
assert not p1.canBuildCanal(leek.networks[0])
assert board.areNetworked(leek, stokeOnTrent)
assert leek.networks[0].isBuilt
assert p1.money == 14

# test network search
print("---test network search---")
redditch = board.towns[-1]
birmingham = board.towns[18]
walsall = board.towns[11]
cannock = board.towns[9]
# build network from cannock to redditch, assert network
assert not board.areNetworked(redditch, cannock)
print(redditch.networks)
print(birmingham.networks)
print(walsall.networks)
print(cannock.networks)
assert not p1.canPlaceCanal(redditch.networks[0])  # can't build canal on railray only
assert p1.canBuildCanal(redditch.networks[1])
assert p1.canBuildCanal(birmingham.networks[4])
p1.buildCanal(redditch.networks[1])
p1.buildCanal(birmingham.networks[4])
p1.buildCanal(birmingham.networks[0])
p1.buildCanal(walsall.networks[1])
assert p1.money == 2
assert board.areNetworked(redditch, cannock)

# test building buildings
print(p2.buildings)
assert p2.canBuildBuilding(p2.buildings[0], redditch.buildLocations[0])
p2.buildBuilding(p2.buildings[0], redditch.buildLocations[0])
# should take coal from market (linked to oxford)
assert p2.buildings[0].isActive
print(p2.money)
assert p2.money == 8  # 17-8-1
# assert p2.canBuildBuilding(p2.)
assert p2.canBuildBuilding(p2.buildings[26], redditch.buildLocations[1])
p2.buildBuilding(p2.buildings[26], redditch.buildLocations[1])
assert p2.money == 2  # 8-5-1
