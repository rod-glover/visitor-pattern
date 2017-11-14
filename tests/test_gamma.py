import pytest
from visitor.gamma import E, F, Visitor


class Visitor1(Visitor):
    def __init__(self):
        self.count = 0
        self.stack = []

    def pre(self, node):
        node_type = type(node)
        self.count += 1
        self.stack.append(node.value)
        indent = '\t' * (len(self.stack) - 1)
        if node_type == E:
            print('{}Internal {}'.format(indent, node.value))
        else:
            print("{} Leaf {}".format(indent, '.'.join(map(str, self.stack))))

    def post(self, node):
        self.stack.pop()


@pytest.mark.parametrize('visitor', [
    Visitor1(),
])
def test_1(example_gamma_1, visitor):
    print()
    example_gamma_1.accept(visitor)
    print('Total', visitor.count, 'nodes')

