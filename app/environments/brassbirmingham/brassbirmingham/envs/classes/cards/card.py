from python.id import id

from .enums import CardType


class Card:
    """
    Card object

    :param type: any of ['location', 'industry', 'wild']
    :param name: name of location or industry
    """

    def __init__(self, type: CardType):
        self.id = id()
        self.type = type
