from ..python.id import id
from ..python.print_colors import (
    prCyan,
    prGreen,
    prLightGray,
    prPurple,
    prRed,
    prYellow,
)


class Town:
    """
    Town

    :param color: any of ['blue', 'green', 'red', 'yellow', 'purple']
    :param name: name
    :param buildLocation: array of BuildLocation objects"""

    def __init__(self, color, name, buildLocations):
        self.id = id()
        self.color = color
        self.name = name
        self.buildLocations = buildLocations
        for buildLocation in self.buildLocations:
            buildLocation.addTown(self)
        self.networks = (
            []
        )  # networks to other towns ex: Town('Leek') would have [Town('Stoke-On-Trent'), Town('Belper')]

    """
    addBoard
    game init use only

    :param board: board
    """

    def addBoard(self, board):
        self.board = board

    """
    addNetwork
    game init use only

    :param network: network
    """

    def addNetwork(self, network):
        network.addTown(self)
        self.networks.append(network)

    def __str__(self):
        returnStr = ""
        if self.color == "blue":
            returnStr = prCyan(self.name)
        elif self.color == "green":
            returnStr = prGreen(self.name)
        elif self.color == "red":
            returnStr = prRed(self.name)
        elif self.color == "yellow":
            returnStr = prYellow(self.name)
        elif self.color == "purple":
            returnStr = prPurple(self.name)
        elif self.color == "beer1" or self.color == "beer2":
            returnStr = prLightGray(self.color)
        return str(returnStr)

    def __repr__(self):
        return str(self)
