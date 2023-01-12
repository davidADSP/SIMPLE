from .road import Road


class Railroad(Road):
    def __init__(self, owner):
        super(Railroad, self).__init__(owner, "railroad")
        # TODO cost
