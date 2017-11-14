from abc import ABC, abstractmethod


class Visitable(ABC):
    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError()


class Visitor(ABC):
    @abstractmethod
    def visit(self, node):
        raise NotImplementedError()


class A(Visitable):

    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def accept(self, visitor):
        visitor.visit(self)
        for child in self.children:
            child.accept(visitor)


class B(Visitable):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit(self)


