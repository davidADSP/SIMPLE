from classes.player import Player
from python.id import id

from .enums import RoadType


class Road:
    def __init__(self, owner: Player, type: RoadType):
        self.id = id()
        self.type = type
        self.owner = owner

    def __repr__(self) -> str:
        return f"Owner: {self.owner}, {self.type}"
