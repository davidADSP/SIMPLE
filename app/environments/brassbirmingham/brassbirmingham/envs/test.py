import unittest
from unittest.mock import MagicMock, Mock

from classes.board import Board
from classes.deck import Deck
from classes.enums import Era
from classes.player import Player
from consts import *


class Test(unittest.TestCase):
    def resetGame(self, numPlayers):
        self.board = Board(numPlayers)

        self.p1 = Player("Noah", self.board)
        self.p2 = Player("Tyler", self.board)

        if numPlayers > 2:
            self.p3 = Player("Sam", self.board)
        if numPlayers > 3:
            self.p4 = Player("Mr. Mcdonald", self.board)

    def setUp(self):
        self.resetGame(2)

    # test decks, hand, cards
    def testStartingValues(self):
        self.assertEqual(
            len(self.board.deck.cards),
            40 - 2 * STARTING_HAND_SIZE,
            "Should be 24 cards in a 2 player game",
        )
        self.resetGame(3)
        self.assertEqual(
            len(self.board.deck.cards),
            54 - 3 * STARTING_HAND_SIZE,
            "Should be 30 cards in a 3 player game",
        )
        self.resetGame(4)
        self.assertEqual(
            len(self.board.deck.cards),
            64 - 4 * STARTING_HAND_SIZE,
            "Should be 32 cards in a 4 player game",
        )
        self.assertEqual(
            self.board.coalMarketRemaining, 13, "Should be 13 coal on the market"
        )
        self.assertEqual(
            self.board.ironMarketRemaining, 8, "Should be 8 iron on the market"
        )
        self.assertEqual(self.board.priceForCoal(1), 1, "Should be $1 coal price")
        self.assertEqual(self.board.priceForIron(1), 2, "Should be $2 iron price")
        self.assertEqual(len(self.board.players), 4, "Should be 4 players")

        self.assertEqual(self.p1.buildings[0].name, BuildingName.goods, "Should be")
        self.assertEqual(
            len(self.p1.buildings), 44, "Should be 44 buildings tiles to start with"
        )

        self.assertEqual(self.board.towns[0].name, LEEK, "Should be")

    # test building canal between leek/stoke-on-trent
    def testBuildingCanal(self):
        town1 = self.board.towns[4]
        town2 = self.board.towns[12]

        self.assertEqual(
            self.board.areNetworked(town1, town2),
            False,
            f"{town1} and {town2} should NOT be networked",
        )
        leek = self.board.towns[0]
        stokeOnTrent = self.board.towns[1]
        self.assertFalse(
            self.board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        # print(leek.networks)
        self.assertTrue(
            self.p1.canBuildCanal(leek.networks[0]), "Should be able to build a canal"
        )
        self.assertFalse(
            self.board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        self.p1.buildCanal(leek.networks[0])
        self.assertFalse(
            self.p1.canBuildCanal(leek.networks[0]),
            "Should NOT be able to build a canal",
        )
        self.assertTrue(
            self.board.areNetworked(leek, stokeOnTrent),
            f"{town1} and {town2} should NOT be networked",
        )
        self.assertTrue(leek.networks[0].isBuilt, "Should be built")
        self.assertEqual(self.p1.money, 14, "self.P1 should have $14")

    # test network search
    def testNetworkSearch(self):
        redditch = self.board.townDict["Redditch"]
        birmingham = self.board.townDict["Birmingham"]
        walsall = self.board.towns[11]
        cannock = self.board.towns[9]
        # build network from cannock to redditch, assert network
        self.assertFalse(
            self.board.areNetworked(redditch, cannock),
            f"{redditch} and {cannock} should NOT be networked",
        )
        # print(redditch.networks)
        # print(birmingham.networks)
        # print(walsall.networks)
        # print(cannock.networks)
        self.assertFalse(
            self.p1.canPlaceCanal(redditch.networks[0]),
            "Should NOT be able to build a canal on a rail (no water)",
        )  # can't build canal on railroad only
        self.assertTrue(
            self.p1.canBuildCanal(redditch.networks[1]),
            "Should be able to build a canal",
        )
        self.assertTrue(
            self.p1.canBuildCanal(birmingham.networks[4]),
            "Should be able to build a canal",
        )
        self.p1.buildCanal(redditch.networks[1])
        self.p1.buildCanal(birmingham.networks[4])
        self.p1.buildCanal(birmingham.networks[0])
        self.p1.buildCanal(walsall.networks[1])
        self.assertEqual(self.p1.money, 5, "self.p1 money should be $5")
        self.assertTrue(
            self.board.areNetworked(redditch, cannock),
            f"{redditch} and {cannock} should be networked",
        )

        # test buildings
        self.assertTrue(
            self.p2.canBuildBuilding(self.p2.buildings[0], redditch.buildLocations[0]),
            "Should be",
        )
        self.p2.buildBuilding(self.p2.buildings[0], redditch.buildLocations[0])
        # should take coal from market (linked to oxford)
        self.assertTrue(self.p2.buildings[0].isActive, "Should be")
        self.assertEqual(self.p2.money, 8, "Should be")  # 17-8-1
        self.assertTrue(
            self.p2.canBuildBuilding(self.p2.buildings[26], redditch.buildLocations[1]),
            "Should be",
        )
        self.p2.buildBuilding(self.p2.buildings[26], redditch.buildLocations[1])
        self.assertEqual(self.p2.money, 1, "Should be")  # 8-5-2 (coal market missing 1)

    def testResourceMarketPrice(self):
        # Empty markets
        self.board.coalMarketRemaining = 0
        self.assertEqual(self.board.priceForCoal(4), 32)
        self.board.ironMarketRemaining = 0
        self.assertEqual(self.board.priceForIron(5), 30)

        # Single needed
        self.board.coalMarketRemaining = 8
        self.assertEqual(self.board.priceForCoal(1), 4)
        self.board.ironMarketRemaining = 8
        self.assertEqual(self.board.priceForIron(1), 2)

        # Single price jump
        self.board.coalMarketRemaining = 8
        self.assertEqual(self.board.priceForCoal(3), 13)
        self.board.ironMarketRemaining = 8
        self.assertEqual(self.board.priceForIron(3), 7)

        # Big price jump
        self.board.coalMarketRemaining = 13
        self.assertEqual(self.board.priceForCoal(10), 35)
        self.board.ironMarketRemaining = 8
        self.assertEqual(self.board.priceForIron(10), 40)

    def testVictoryPoints(self):
        # Zero points
        playerVPs = self.board.getVictoryPoints()

        self.assertTrue(self.p1 in playerVPs)
        self.assertTrue(self.p2 in playerVPs)

        self.assertEqual(playerVPs[self.p1], 0)
        self.assertEqual(playerVPs[self.p2], 0)

        # # Buildings Only
        redditch = self.board.townDict["Redditch"]
        birmingham = self.board.townDict["Birmingham"]
        walsall = self.board.towns[11]
        cannock = self.board.towns[9]

        self.board.removeXCoal = Mock()
        self.board.removeXBeer = Mock()

        self.p1.canBuildBuilding = Mock(return_value=True)
        self.p1.canSell = Mock(return_value=True)

        self.p1CottonBuilding = self.p1.buildings[10]
        self.p1.buildBuilding(self.p1CottonBuilding, birmingham.buildLocations[0])
        self.p1CottonBuilding.sell()  # 5

        self.p2.canBuildBuilding = Mock(return_value=True)

        self.p2.buildBuilding(self.p2.buildings[0], redditch.buildLocations[0])

        self.p2Goods2Building = self.p2.buildings[1]
        self.p2.buildBuilding(self.p2Goods2Building, walsall.buildLocations[0])
        self.p2Goods2Building.sell()  # 5

        p2CoalBuilding: IndustryBuilding = self.p2.buildings[37]
        self.p2.buildBuilding(p2CoalBuilding, cannock.buildLocations[1])

        p2CoalBuilding.decreaseResourceAmount(p2CoalBuilding.resourceAmount)

        playerVPs = self.board.getVictoryPoints()

        self.assertEqual(playerVPs[self.p1], 5)
        self.assertEqual(playerVPs[self.p2], 6)

        # # With networks
        self.p1.canBuildCanal = Mock(return_value=True)
        self.p1.buildCanal(
            redditch.networks[1]
        )  # 4 = 2 (tradepost oxford) + 2 (goods @ redditch)
        print(redditch.networks[1])

        print(birmingham.networks[0])
        self.p1.buildCanal(
            birmingham.networks[4]
        )  # 3 = 2 (tradepost oxford) + 1 (cotton @ birmingham)

        self.p2.canBuildCanal = Mock(return_value=True)
        self.p2.buildCanal(birmingham.networks[1])  # 1 (cotton @ birmingham)

        playerVPs = self.board.getVictoryPoints()

        self.assertEqual(playerVPs[self.p1], 12)
        self.assertEqual(playerVPs[self.p2], 7)

        # With initial VPs

        self.p1.victoryPoints = 2
        self.p2.victoryPoints = 7

        playerVPs = self.board.getVictoryPoints()

        self.assertEqual(playerVPs[self.p1], 14)
        self.assertEqual(playerVPs[self.p2], 14)

    def testIncomeLevel(self):
        self.p1.income = 10
        self.assertEqual(self.p1.incomeLevel(), 0)

        self.p1.income = 19
        self.assertEqual(self.p1.incomeLevel(), 5)

        self.p1.income = 35
        self.assertEqual(self.p1.incomeLevel(), 12)

        self.p1.income = 68
        self.assertEqual(self.p1.incomeLevel(), 22)

        self.p1.income = 99
        self.assertEqual(self.p1.incomeLevel(), 30)

        self.p1.income = 7
        self.p1.decreaseIncomeLevel(2)
        self.assertEqual(self.p1.income, 5)

        self.p1.income = 12
        self.p1.decreaseIncomeLevel(1)
        self.assertEqual(self.p1.income, 10)

        self.p1.income = 17
        self.p1.decreaseIncomeLevel(2)
        self.assertEqual(self.p1.income, 13)

        self.p1.income = 33
        self.p1.decreaseIncomeLevel(3)
        self.assertEqual(self.p1.income, 25)

        self.p1.income = 87
        self.p1.decreaseIncomeLevel(2)
        self.assertEqual(self.p1.income, 77)

        self.p1.income = 98
        self.p1.decreaseIncomeLevel(3)
        self.assertEqual(self.p1.income, 85)

    def testEndCanalEra(self):
        self.board.deck = Deck([])
        for player in self.board.players:
            player.hand.cards = []

        self.board.endCanalEra()
        for player in self.board.players:
            self.assertEqual(player.roadCount, 14)
            self.assertEqual(len(player.hand.cards), 8)

        for town in self.board.towns:
            for network in town.networks:
                self.assertEqual(network.isBuilt, False)
            for buildLocation in town.buildLocations:
                if buildLocation.building and buildLocation.building.tier <= 1:
                    self.assertEqual(buildLocation.building.isRetired, True)

        for tradepost in self.board.tradePosts:
            self.assertEqual(tradepost.beerAmount, tradepost.startingBeerAmount)

        self.assertEqual(self.board.era, Era.railroad)


if __name__ == "__main__":
    unittest.main()
