"""Simple classes for forming examples with."""

class Internal:
    def __init__(self, value, *children):
        self.value = value
        self.children = children


class Leaf:
    def __init__(self, value):
        self.value = value
