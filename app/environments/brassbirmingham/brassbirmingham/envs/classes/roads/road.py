from ...python.id import id


class Road:
    def __init__(self, owner, type):
        self.id = id()
        self.type = type
        self.owner = owner

    def __repr__(self):
        return f"Owner: {self.owner}, {self.type}"
