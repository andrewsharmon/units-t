"""Catalogue of units.

Base units are the coherent SI base units, each fixed by one of the defining constants
in :mod:`units_t._defining`. Every other unit is built from them with an exact scale
factor, so conversions between any two units here are exact rationals.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _defining
from units_t import sources as src
from units_t.dimensions import (
    AMOUNT,
    CURRENT,
    DIMENSIONLESS,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TEMPERATURE,
    TIME,
)
from units_t.unit import Unit

# -- SI prefixes (including ronna/quetta/ronto/quecto, adopted 2022) ------------

SI_PREFIXES: dict[str, tuple[str, Fraction]] = {
    "quetta": ("Q", Fraction(10) ** 30),
    "ronna": ("R", Fraction(10) ** 27),
    "yotta": ("Y", Fraction(10) ** 24),
    "zetta": ("Z", Fraction(10) ** 21),
    "exa": ("E", Fraction(10) ** 18),
    "peta": ("P", Fraction(10) ** 15),
    "tera": ("T", Fraction(10) ** 12),
    "giga": ("G", Fraction(10) ** 9),
    "mega": ("M", Fraction(10) ** 6),
    "kilo": ("k", Fraction(10) ** 3),
    "hecto": ("h", Fraction(10) ** 2),
    "deca": ("da", Fraction(10) ** 1),
    "deci": ("d", Fraction(10) ** -1),
    "centi": ("c", Fraction(10) ** -2),
    "milli": ("m", Fraction(10) ** -3),
    "micro": ("µ", Fraction(10) ** -6),
    "nano": ("n", Fraction(10) ** -9),
    "pico": ("p", Fraction(10) ** -12),
    "femto": ("f", Fraction(10) ** -15),
    "atto": ("a", Fraction(10) ** -18),
    "zepto": ("z", Fraction(10) ** -21),
    "yocto": ("y", Fraction(10) ** -24),
    "ronto": ("r", Fraction(10) ** -27),
    "quecto": ("q", Fraction(10) ** -30),
}


def prefixed(prefix: str, unit: Unit) -> Unit:
    """Apply an SI prefix by name, e.g. ``prefixed("kilo", m)`` -> ``km``."""
    symbol, factor = SI_PREFIXES[prefix]
    name = f"{prefix}{unit.name}" if unit.name else ""
    return unit.scaled(factor, f"{symbol}{unit.symbol}", name)


# -- SI base units ------------------------------------------------------------

_ONE = Fraction(1)

_SI = (src.SI_BROCHURE,)

s = Unit("s", _ONE, TIME, "second", _SI)  # fixed by Δν_Cs
m = Unit("m", _ONE, LENGTH, "metre", _SI)  # fixed by c (and the second)
kg = Unit("kg", _ONE, MASS, "kilogram", _SI)  # fixed by h (and the metre and second)
A = Unit("A", _ONE, CURRENT, "ampere", _SI)  # fixed by e (and the second)
K = Unit("K", _ONE, TEMPERATURE, "kelvin", _SI)  # fixed by k_B (and kg, m, s)
mol = Unit("mol", _ONE, AMOUNT, "mole", _SI)  # fixed by N_A
cd = Unit("cd", _ONE, LUMINOUS_INTENSITY, "candela", _SI)  # fixed by K_cd (and kg, m, s)

one = Unit("1", _ONE, DIMENSIONLESS, "one", _SI)
rad = Unit("rad", _ONE, DIMENSIONLESS, "radian", _SI)
sr = Unit("sr", _ONE, DIMENSIONLESS, "steradian", _SI)

# -- SI derived units with special names -------------------------------------

Hz = (s**-1).named("Hz", "hertz", sources=_SI)
N = (kg * m / s**2).named("N", "newton", sources=_SI)
Pa = (N / m**2).named("Pa", "pascal", sources=_SI)
J = (N * m).named("J", "joule", sources=_SI)
W = (J / s).named("W", "watt", sources=_SI)
C = (A * s).named("C", "coulomb", sources=_SI)
V = (W / A).named("V", "volt", sources=_SI)
F = (C / V).named("F", "farad", sources=_SI)
ohm = (V / A).named("Ω", "ohm", sources=_SI)
S = (A / V).named("S", "siemens", sources=_SI)
Wb = (V * s).named("Wb", "weber", sources=_SI)
T = (Wb / m**2).named("T", "tesla", sources=_SI)
H = (Wb / A).named("H", "henry", sources=_SI)
lm = (cd * sr).named("lm", "lumen", sources=_SI)
lx = (lm / m**2).named("lx", "lux", sources=_SI)
Bq = (s**-1).named("Bq", "becquerel", sources=_SI)
Gy = (J / kg).named("Gy", "gray", sources=_SI)
Sv = (J / kg).named("Sv", "sievert", sources=_SI)
kat = (mol / s).named("kat", "katal", sources=_SI)

# -- Common prefixed units ----------------------------------------------------

g = kg.scaled(Fraction(1, 1000), "g", "gram")
mg = prefixed("milli", g)

km = prefixed("kilo", m)
cm = prefixed("centi", m)
mm = prefixed("milli", m)
um = prefixed("micro", m)
nm = prefixed("nano", m)

ms = prefixed("milli", s)
us = prefixed("micro", s)
ns = prefixed("nano", s)

kHz = prefixed("kilo", Hz)
MHz = prefixed("mega", Hz)
GHz = prefixed("giga", Hz)

kJ = prefixed("kilo", J)
kW = prefixed("kilo", W)
kPa = prefixed("kilo", Pa)
mA = prefixed("milli", A)
mV = prefixed("milli", V)
kV = prefixed("kilo", V)

# -- Non-SI units accepted for use with the SI --------------------------------

minute = s.scaled(60, "min", "minute", sources=_SI)
h = minute.scaled(60, "h", "hour")
day = h.scaled(24, "d", "day")
L = (prefixed("deci", m) ** 3).named("L", "litre", sources=_SI)
mL = prefixed("milli", L)
tonne = kg.scaled(1000, "t", "tonne", sources=_SI)
au = m.scaled(149_597_870_700, "au", "astronomical unit", sources=(src.IAU_2012_B2,))
eV = J.scaled(_defining.E, "eV", "electronvolt", sources=_SI)  # exact: e is defining
keV = prefixed("kilo", eV)
MeV = prefixed("mega", eV)
GeV = prefixed("giga", eV)

# -- Imperial / US customary (exact by the 1959 international agreement) ------

inch = m.scaled("0.0254", "in", "inch", sources=(src.YARD_POUND_1959,))
ft = inch.scaled(12, "ft", "foot")
yd = ft.scaled(3, "yd", "yard")
mi = ft.scaled(5280, "mi", "mile")
lb = kg.scaled("0.45359237", "lb", "pound (avoirdupois)", sources=(src.YARD_POUND_1959,))
oz = lb.scaled(Fraction(1, 16), "oz", "ounce (avoirdupois)")
