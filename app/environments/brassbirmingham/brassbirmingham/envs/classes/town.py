from __future__ import annotations

from typing import TYPE_CHECKING, List

import consts
from python.id import id
from python.print_colors import (prCyan, prGreen, prLightGray, prPurple, prRed,
                                 prYellow)

if TYPE_CHECKING:
    from .board import Board

from .build_location import BuildLocation
from .road_location import RoadLocation


class Town:
    """
    Town

    :param color: any of ['blue', 'green', 'red', 'yellow', 'purple']
    :param name: name
    :param buildLocation: array of BuildLocation objects"""

    def __init__(self, color: str, name: str, buildLocations: List[BuildLocation]):
        self.id = id()
        self.type = "Town"
        self.color = color
        self.name = name
        self.buildLocations = buildLocations
        for buildLocation in self.buildLocations:
            buildLocation.addTown(self)
        # networks to other towns ex: Town('Leek') would have [Town('Stoke-On-Trent'), Town('Belper')]
        self.networks: List[RoadLocation] = []

    """
    addBoard
    game init use only

    :param board: board
    """

    def addBoard(self, board: Board):
        self.board = board

    """
    addRoadLocation
    game init use only

    :param roadLocation: roadLocation
    """

    def addRoadLocation(self, roadLocation: RoadLocation):
        roadLocation.addTown(self)
        self.networks.append(roadLocation)

    def getNetworkVictoryPoints(self):
        networkVP = 0
        for buildLocation in self.buildLocations:
            if buildLocation.building:
                networkVP += buildLocation.building.networkPoints
        return networkVP

    def __str__(self) -> str:
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
        elif self.color == consts.BEER1 or self.color == consts.BEER2:
            returnStr = prLightGray(self.color)
        return f"Town({returnStr})"

    def __repr__(self) -> str:
        return str(self)
