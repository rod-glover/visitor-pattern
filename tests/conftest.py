import pytest
from visitor.alpha import A, B
from visitor.beta import C, D
from visitor.gamma import E, F
from visitor.epsilon import G, H


@pytest.fixture
def example_alpha_1():
    return A(
        1,
        A(
            2,
            B(3),
            B(4)
        ),
        A(
            5,
            B(6),
            B(7),
            B(8)
        )
    )


@pytest.fixture
def example_beta_1():
    return C(
        1,
        C(
            2,
            D(3),
            D(4)
        ),
        C(
            5,
            D(6),
            D(7),
            D(8)
        )
    )


@pytest.fixture
def example_gamma_1():
    return E(
        1,
        E(
            2,
            F(3),
            F(4)
        ),
        E(
            5,
            F(6),
            F(7),
            F(8)
        )
    )


@pytest.fixture
def example_epsilon_1():
    return G(
        1,
        G(
            2,
            H(3),
            H(4)
        ),
        G(
            5,
            H(6),
            H(7),
            H(8)
        )
    )


