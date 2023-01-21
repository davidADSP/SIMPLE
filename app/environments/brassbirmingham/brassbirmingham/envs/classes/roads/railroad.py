from classes.player import Player

from .enums import RoadType
from .road import Road


class Railroad(Road):
    def __init__(self, owner: Player):
        super(Railroad, self).__init__(owner, RoadType.railroad)
        # TODO cost
