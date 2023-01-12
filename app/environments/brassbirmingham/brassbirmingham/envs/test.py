import unittest

from classes.board import Board
from classes.player import Player
from consts import *


def resetGame(numPlayers):
    global board, p1, p2, p3, p4
    board = Board(numPlayers)
    p1 = Player("Noah", board)
    p2 = Player("Tyler", board)
    p3, p4 = None, None
    if numPlayers > 2:
        p3 = Player("Sam", board)
    if numPlayers > 3:
        p4 = Player("Mr. Mcdonald", board)


resetGame(2)


class Test(unittest.TestCase):
    # test decks, hand, cards
    def testStartingValues(self):
        resetGame(2)
        self.assertEqual(
            len(board.deck.cards), 40, "Should be 40 cards in a 2 player game"
        )
        resetGame(3)
        self.assertEqual(
            len(board.deck.cards), 54, "Should be 54 cards in a 3 player game"
        )
        resetGame(4)
        self.assertEqual(
            len(board.deck.cards), 64, "Should be 64 cards in a 4 player game"
        )
        self.assertEqual(
            len(board.wildBuildingDeck.cards), 5, "Should be 5 wild building cards"
        )
        self.assertEqual(
            len(board.wildLocationDeck.cards), 5, "Should be 5 wild location cards"
        )
        self.assertEqual(
            board.coalMarketRemaining, 15, "Should be 15 coal on the market"
        )
        self.assertEqual(board.ironMarketRemaining, 8, "Should be 8 iron on the market")
        self.assertEqual(board.coalMarketPrice, 1, "Should be $1 coal price")
        self.assertEqual(board.ironMarketPrice, 1, "Should be $1 coal price")
        self.assertEqual(len(board.players), 4, "Should be 4 players")

        self.assertEqual(p1.buildings[0].name, GOODS, "Should be")
        self.assertEqual(
            len(p1.buildings), 44, "Should be 44 buildings tiles to start with"
        )

        self.assertEqual(board.towns[0].name, LEEK, "Should be")

    # test building canal between leek/stoke-on-trent
    def testBuildingCanal(self):
        town1 = board.towns[4]
        town2 = board.towns[12]

        self.assertEqual(
            board.areNetworked(town1, town2),
            False,
            f"{town1} and {town2} should NOT be networked",
        )
        leek = board.towns[0]
        stokeOnTrent = board.towns[1]
        self.assertFalse(
            board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        # print(leek.networks)
        self.assertTrue(
            p1.canBuildCanal(leek.networks[0]), "Should be able to build a canal"
        )
        self.assertFalse(
            board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        p1.buildCanal(leek.networks[0])
        self.assertFalse(
            p1.canBuildCanal(leek.networks[0]), "Should NOT be able to build a canal"
        )
        self.assertTrue(
            board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        self.assertTrue(leek.networks[0].isBuilt, "Should be built")
        self.assertEqual(p1.money, 14, "P1 should have $14")

    # test network search
    def testNetworkSearch(self):
        # print(board.towns)
        redditch = board.townMap["Redditch"]
        birmingham = board.townMap["Birmingham"]
        walsall = board.towns[11]
        cannock = board.towns[9]
        # build network from cannock to redditch, assert network
        self.assertFalse(
            board.areNetworked(redditch, cannock),
            f"{redditch} and {cannock} should NOT be networked",
        )
        # print(redditch.networks)
        # print(birmingham.networks)
        # print(walsall.networks)
        # print(cannock.networks)
        self.assertFalse(
            p1.canPlaceCanal(redditch.networks[0]),
            "Should NOT be able to build a canal on a rail (no water)",
        )  # can't build canal on railray only
        self.assertTrue(
            p1.canBuildCanal(redditch.networks[1]), "Should be able to build a canal"
        )
        self.assertTrue(
            p1.canBuildCanal(birmingham.networks[4]), "Should be able to build a canal"
        )
        p1.buildCanal(redditch.networks[1])
        p1.buildCanal(birmingham.networks[4])
        p1.buildCanal(birmingham.networks[0])
        p1.buildCanal(walsall.networks[1])
        self.assertEqual(p1.money, 2, "p1 money should be $2")
        self.assertTrue(
            board.areNetworked(redditch, cannock),
            f"{redditch} and {cannock} should be networked",
        )

        # test buildings
        # print(p2.buildings)
        self.assertTrue(
            p2.canBuildBuilding(p2.buildings[0], redditch.buildLocations[0]),
            "Should be",
        )
        p2.buildBuilding(p2.buildings[0], redditch.buildLocations[0])
        # should take coal from market (linked to oxford)
        self.assertTrue(p2.buildings[0].isActive, "Should be")
        # print(p2.money)
        self.assertEqual(p2.money, 8, "Should be")  # 17-8-1
        self.assertTrue(
            p2.canBuildBuilding(p2.buildings[26], redditch.buildLocations[1]),
            "Should be",
        )
        p2.buildBuilding(p2.buildings[26], redditch.buildLocations[1])
        self.assertEqual(p2.money, 2, "Should be")  # 8-5-1

        print(board.townMap)


if __name__ == "__main__":
    unittest.main()
