from classes.player import Player

from .enums import RoadType
from .road import Road


class Canal(Road):
    def __init__(self, owner: Player):
        super(Canal, self).__init__(owner, RoadType.canal)
        self.cost = 3
