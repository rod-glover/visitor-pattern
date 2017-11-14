import pytest
from visitor.beta import C, D, Visitor


class Visitor1(Visitor):
    def __init__(self):
        self.count = 0
        self.prefix = []

    def visit(self, node, extra):
        node_type = type(node)
        if extra is None:
            extra = []
        extra = extra + [node.value]
        if node_type == D:
            self.count += 1
            print('.'.join(map(str, extra)))
        return extra


class Visitor2(Visitor):
    def __init__(self):
        self.count = 0
        self.prefix = []

    def visit(self, node, extra):
        node_type = type(node)
        if extra is None:
            extra = []
        extra = extra + [node.value]
        indent = '\t' * (len(extra) - 1)
        if node_type == D:
            self.count += 1
            print("{} Leaf {}".format(indent, '.'.join(map(str, extra))))
        else:
            print('{}Internal {}'.format(indent, node.value))
        return extra


@pytest.mark.parametrize('visitor', [
    Visitor1(),
    Visitor2(),
])
def test_2(example_beta_1, visitor):
    print()
    example_beta_1.accept(visitor)
    print('Total', visitor.count, 'nodes')

