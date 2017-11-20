import pytest
from visitor.epsilon import G, H, Dispatcher


class ExplicitStackVisitor:
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

    @Dispatcher.on('node')
    def visit(self, node):
        """Generic dispatch function"""

    @visit.when(G)
    def visit(self, node):
        self.pre(node)
        for child in node.children:
            self.visit(child)
        self.post()

    @visit.when(H)
    def visit(self, node):
        self.pre(node)
        self.post()


class ImplicitStackVisitor:
    def output(self, prefix):
        indent = '  ' * (len(prefix) - 1)
        print("{}{}".format(indent, '.'.join(map(str, prefix))))


    @Dispatcher.on('node')
    def visit(self, node, prefix=[]):
        """Generic dispatch function"""

    @visit.when(G)
    def visit(self, node, prefix=[]):
        prefix = prefix + [node.value]
        self.output(prefix)
        for child in node.children:
            self.visit(child, prefix)

    @visit.when(H)
    def visit(self, node, prefix=[]):
        prefix = prefix + [node.value]
        self.output(prefix)


@pytest.mark.parametrize('visitor', [
    ExplicitStackVisitor(),
    ImplicitStackVisitor(),
])
def test_1(example_epsilon_1, visitor):
    print()
    visitor.visit(example_epsilon_1)
    print('Total', getattr(visitor, 'count', 'no answer'), 'nodes')
