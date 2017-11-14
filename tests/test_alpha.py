import pytest
from visitor.alpha import A, B, Visitor


class Visitor1(Visitor):
    def __init__(self, word):
        self.count = 0
        self.word = word

    def visit(self, node):
        self.count += 1
        print(self.word, node.value)


class Visitor2(Visitor):
    def __init__(self):
        self.count = 0

    def visit(self, node):
        node_type = type(node)
        if node_type == B:
            self.count += 1
            print(node.value)


class Visitor3(Visitor):
    def __init__(self):
        self.count = 0
        self.prefix = []

    def visit(self, node):
        node_type = type(node)
        self.prefix.append(node.value)
        if node_type == B:
            self.count += 1
            print('.'.join(map(str, self.prefix)))
            self.prefix.pop()


@pytest.mark.parametrize('visitor', [
    Visitor1('hoohah'),
    Visitor2(),
    Visitor3(),
])
def test_1(example_alpha_1, visitor):
    print()
    example_alpha_1.accept(visitor)
    print('Total', visitor.count, 'nodes')

