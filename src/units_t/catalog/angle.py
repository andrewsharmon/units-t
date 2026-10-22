"""Units of plane and solid angle.

The radian is the coherent unit, so every unit defined as a fraction of a full circle
involves π. Those carry the π rounding term with an exponent. Ratios between such units
(degree to arcminute, turn to NATO mil) cancel π and come out exact.

The radian and steradian are dimensionless in the SI, so these units also convert to
:data:`units_t.units.one`. That is an SI quirk, not a feature.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _irrational
from units_t import sources as src
from units_t import units as u

_STD = (src.NIST_SP811,)
_PI = _irrational.PI_TERM
_PI_RAD = u.rad.scaled(_irrational.PI, "π rad", "π radians", uncertainty=_PI)

turn = _PI_RAD.scaled(2, "tr", "turn (revolution)", sources=_STD)
revolution = turn
quadrant = turn.scaled(Fraction(1, 4), "quadrant", "quadrant (right angle)")
sextant = turn.scaled(Fraction(1, 6), "sextant", "sextant")
degree = turn.scaled(Fraction(1, 360), "°", "degree", sources=_STD)
arcminute = degree.scaled(Fraction(1, 60), "′", "arcminute")
arcsecond = arcminute.scaled(Fraction(1, 60), "″", "arcsecond")
milliarcsecond = arcsecond.scaled(Fraction(1, 1000), "mas", "milliarcsecond")
microarcsecond = arcsecond.scaled(Fraction(1, 10**6), "µas", "microarcsecond")
gradian = turn.scaled(Fraction(1, 400), "gon", "gradian (gon)", sources=_STD)
centesimal_minute = gradian.scaled(Fraction(1, 100), "c", "centesimal minute")
centesimal_second = centesimal_minute.scaled(Fraction(1, 100), "cc", "centesimal second")
zodiac_sign = degree.scaled(30, "sign", "sign (zodiacal)", sources=(src.ROWLETT,))
hour_angle = degree.scaled(15, "h (angle)", "hour angle", sources=(src.ROWLETT,))
minute_of_time = hour_angle.scaled(Fraction(1, 60), "m (angle)", "minute of right ascension")
second_of_time = minute_of_time.scaled(Fraction(1, 60), "s (angle)", "second of right ascension")
compass_point = turn.scaled(Fraction(1, 32), "point", "point (compass)", sources=(src.ROWLETT,))
binary_degree = turn.scaled(Fraction(1, 256), "brad", "binary degree", sources=(src.ROWLETT,))
milliradian = u.rad.scaled(Fraction(1, 1000), "mrad", "milliradian")
nato_mil = turn.scaled(Fraction(1, 6400), "mil (NATO)", "mil (NATO)", sources=(src.ROWLETT,))
warsaw_pact_mil = turn.scaled(
    Fraction(1, 6000), "mil (WP)", "mil (Warsaw Pact)", sources=(src.ROWLETT,)
)
swedish_streck = turn.scaled(
    Fraction(1, 6300), "streck", "streck (Swedish mil)", sources=(src.ROWLETT,)
)

# -- solid angle ---------------------------------------------------------------

square_degree = (degree**2).named("deg²", "square degree", sources=_STD)
square_arcminute = (arcminute**2).named("arcmin²", "square arcminute")
square_arcsecond = (arcsecond**2).named("arcsec²", "square arcsecond")
spat = u.sr.scaled(
    4 * _irrational.PI, "sp", "spat (full sphere)", sources=(src.ROWLETT,), uncertainty=_PI
)
hemisphere = spat.scaled(Fraction(1, 2), "hemisphere", "hemisphere")
