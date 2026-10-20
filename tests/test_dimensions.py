from fractions import Fraction

import pytest

from units_t.dimensions import DIMENSIONLESS, LENGTH, MASS, TIME, Dimension


def test_algebra() -> None:
    velocity = LENGTH / TIME
    force = MASS * LENGTH / TIME**2
    assert velocity == Dimension((1, 0, -1, 0, 0, 0, 0))
    assert force / MASS == velocity / TIME
    assert (LENGTH / LENGTH).is_dimensionless


def test_rational_exponents() -> None:
    root_time = TIME ** Fraction(1, 2)
    assert root_time * root_time == TIME
    assert str(root_time) == "T^(1/2)"


def test_str() -> None:
    assert str(DIMENSIONLESS) == "1"
    assert str(MASS * LENGTH**2 / TIME**2) == "L^2·M·T^-2"


def test_wrong_length_rejected() -> None:
    with pytest.raises(ValueError):
        Dimension((1, 2, 3))
