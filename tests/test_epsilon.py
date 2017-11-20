import pytest
from visitor.epsilon import G, H, dispatch_on


class StackVisitor:
    def __init__(self):
        self.count = 0
        self.stack = []

    def pre(self, node):
        self.count += 1
        self.stack.append(node.value)
        indent = '  ' * (len(self.stack) - 1)
        print("{}{}".format(indent, '.'.join(map(str, self.stack))))

    def post(self):
        self.stack.pop()

    @dispatch_on('node')
    def visit(self, node):
        """Generic dispatch function"""

    @visit.when(G)
    def visitG(self, node):
        self.pre(node)
        for child in node.children:
            self.visit(child)
        self.post()

    @visit.when(H)
    def visitH(self, node):
        self.pre(node)
        self.post()


@pytest.mark.parametrize('visitor', [
    StackVisitor(),
])
def test_1(example_epsilon_1, visitor):
    print()
    visitor.visit(example_epsilon_1)
    print('Total', visitor.count, 'nodes')
