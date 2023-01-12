from .road import Road


class Canal(Road):
    def __init__(self, owner):
        super(Canal, self).__init__(owner, "canal")
        self.cost = 3
