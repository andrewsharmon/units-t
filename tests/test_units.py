from fractions import Fraction

import pytest

from units_t import DimensionError
from units_t import units as u


def test_derived_units_match_definitions() -> None:
    assert u.N == u.kg * u.m / u.s**2
    assert u.J == u.N * u.m
    assert u.W == u.V * u.A
    assert u.ohm == u.V / u.A
    assert u.T == u.kg / (u.A * u.s**2)


def test_prefixes() -> None:
    assert u.km.conversion_factor(u.m) == 1000
    assert u.um.conversion_factor(u.m) == Fraction(1, 10**6)
    assert u.prefixed("quecto", u.g).scale == Fraction(1, 10**33)


def test_imperial_is_exact() -> None:
    assert u.mi.conversion_factor(u.m) == Fraction("1609.344")
    assert u.lb.conversion_factor(u.g) == Fraction("453.59237")


def test_electronvolt_traces_to_elementary_charge() -> None:
    assert u.eV.conversion_factor(u.J) == Fraction("1.602176634e-19")


def test_litre() -> None:
    assert u.L.conversion_factor(u.m**3) == Fraction(1, 1000)


def test_incompatible_conversion_raises() -> None:
    with pytest.raises(DimensionError):
        u.m.conversion_factor(u.s)
