from fractions import Fraction

from units_t import constants as const
from units_t import units as u
from units_t.dimensions import LENGTH, TIME


def test_defining_constants_are_exact() -> None:
    assert const.c.value == 299_792_458
    assert const.h.value == Fraction("6.62607015e-34")
    assert const.e.value == Fraction("1.602176634e-19")
    assert const.k_B.value == Fraction("1.380649e-23")
    assert const.N_A.value == Fraction("6.02214076e23")


def test_dimensions() -> None:
    assert const.c.dimension == LENGTH / TIME
    assert const.h.unit == u.J * u.s


def test_derived_constants_are_exact() -> None:
    assert const.R.value == Fraction("8.31446261815324")
    assert const.F.value == Fraction("96485.3321233100184")
