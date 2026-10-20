"""Catalogue of units.

Base units are the coherent SI base units, each fixed by one of the defining constants
in :mod:`units_t._defining`. Every other unit is built from them with an exact scale
factor, so conversions between any two units here are exact rationals.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _defining
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
    return unit.scaled(factor, f"{symbol}{unit.symbol}")


# -- SI base units ------------------------------------------------------------

_ONE = Fraction(1)

s = Unit("s", _ONE, TIME)  # fixed by Δν_Cs
m = Unit("m", _ONE, LENGTH)  # fixed by c (and the second)
kg = Unit("kg", _ONE, MASS)  # fixed by h (and the metre and second)
A = Unit("A", _ONE, CURRENT)  # fixed by e (and the second)
K = Unit("K", _ONE, TEMPERATURE)  # fixed by k_B (and kg, m, s)
mol = Unit("mol", _ONE, AMOUNT)  # fixed by N_A
cd = Unit("cd", _ONE, LUMINOUS_INTENSITY)  # fixed by K_cd (and kg, m, s)

one = Unit("1", _ONE, DIMENSIONLESS)
rad = Unit("rad", _ONE, DIMENSIONLESS)
sr = Unit("sr", _ONE, DIMENSIONLESS)

# -- SI derived units with special names -------------------------------------

Hz = (s**-1).named("Hz")
N = (kg * m / s**2).named("N")
Pa = (N / m**2).named("Pa")
J = (N * m).named("J")
W = (J / s).named("W")
C = (A * s).named("C")
V = (W / A).named("V")
F = (C / V).named("F")
ohm = (V / A).named("Ω")
S = (A / V).named("S")
Wb = (V * s).named("Wb")
T = (Wb / m**2).named("T")
H = (Wb / A).named("H")
lm = (cd * sr).named("lm")
lx = (lm / m**2).named("lx")
Bq = (s**-1).named("Bq")
Gy = (J / kg).named("Gy")
Sv = (J / kg).named("Sv")
kat = (mol / s).named("kat")

# -- Common prefixed units ----------------------------------------------------

g = kg.scaled(Fraction(1, 1000), "g")
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

minute = s.scaled(60, "min")
h = minute.scaled(60, "h")
day = h.scaled(24, "d")
L = (prefixed("deci", m) ** 3).named("L")
mL = prefixed("milli", L)
tonne = kg.scaled(1000, "t")
au = m.scaled(149_597_870_700, "au")  # IAU 2012, exact
eV = J.scaled(_defining.E, "eV")  # exact since e is a defining constant
keV = prefixed("kilo", eV)
MeV = prefixed("mega", eV)
GeV = prefixed("giga", eV)

# -- Imperial / US customary (exact by the 1959 international agreement) ------

inch = m.scaled("0.0254", "in")
ft = inch.scaled(12, "ft")
yd = ft.scaled(3, "yd")
mi = ft.scaled(5280, "mi")
lb = kg.scaled("0.45359237", "lb")
oz = lb.scaled(Fraction(1, 16), "oz")
