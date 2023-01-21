from python.id import id

from .enums import CardName, CardType


class Card:
    """
    Card object

    :param type: any of ['location', 'industry']
    :param name: name of location or industry
    """

    def __init__(self, type: CardType, name: CardName):
        self.id = id()
        self.name = name
        self.type = type
