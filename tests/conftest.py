import pytest
from visitor.simple_classes import Internal, Leaf


@pytest.fixture
def simple_example_1():
    return Internal(
        1,
        Internal(
            2,
            Leaf(3),
            Leaf(4)
        ),
        Internal(
            5,
            Leaf(6),
            Leaf(7),
            Leaf(8)
        )
    )


