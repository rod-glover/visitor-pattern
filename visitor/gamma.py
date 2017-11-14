from abc import ABC, abstractmethod


class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError()


class Visitor(ABC):
    @abstractmethod
    def pre(self, node):
        raise NotImplementedError()

    @abstractmethod
    def post(self, node):
        raise NotImplementedError()


class E(Visitable):

    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def accept(self, visitor):
        visitor.pre(self)
        for child in self.children:
            child.accept(visitor)
        visitor.post(self)


class F(Visitable):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.pre(self)
        visitor.post(self)


