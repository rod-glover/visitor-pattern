from abc import ABC, abstractmethod


class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor, extra):
        raise NotImplementedError()


class Visitor(ABC):
    @abstractmethod
    def visit(self, node, extra):
        raise NotImplementedError()


class C(Visitable):

    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def accept(self, visitor, extra=None):
        extra = visitor.visit(self, extra)
        for child in self.children:
            child.accept(visitor, extra)


class D(Visitable):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor, extra=None):
        visitor.visit(self, extra)


