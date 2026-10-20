from fractions import Fraction

import pytest

from units_t import DimensionError, Quantity
from units_t import units as u


def test_construction_via_multiplication() -> None:
    assert 3 * u.km == Quantity(3, u.km)


def test_exact_conversion() -> None:
    speed = (100 * u.km / u.h).to(u.m / u.s)
    assert speed.value == Fraction(250, 9)


def test_float_conversion() -> None:
    assert (2.5 * u.km).to(u.m).value == pytest.approx(2500.0)


def test_equality_across_units() -> None:
    assert 1 * u.km == 1000 * u.m
    assert hash(1 * u.km) == hash(1000 * u.m)
    assert 1 * u.m != 1 * u.s


def test_addition_converts_to_left_unit() -> None:
    total = 1 * u.km + 500 * u.m
    assert total.unit == u.km
    assert total.value == Fraction(3, 2)


def test_addition_of_incompatible_raises() -> None:
    with pytest.raises(DimensionError):
        _ = 1 * u.m + 1 * u.s


def test_multiplication_and_division() -> None:
    work = (2 * u.N) * (3 * u.m)
    assert work == 6 * u.J
    assert (work / (2 * u.s)) == 3 * u.W
    assert (1 / (2 * u.s)) == Fraction(1, 2) * u.Hz


def test_ordering() -> None:
    assert 1 * u.mi > 1 * u.km
    with pytest.raises(DimensionError):
        _ = 1 * u.m < 1 * u.s


def test_str_shows_exact_values_as_decimals() -> None:
    assert str((1 * u.eV).to(u.J)) == "1.602176634e-19 J"
