"""Temperature *interval* units.

These convert temperature differences only: 1 °F of change is 5/9 K of change. Scales
with an offset (°C, °F, °Ré …) need affine conversion, which the library does not support
yet (see the roadmap). So ``fahrenheit_degree`` here means "a span of one Fahrenheit
degree", and converting 32 of them gives 17.8 K, not 273.15 K.

The Rankine scale has no offset (0 °R is absolute zero), so ``rankine`` is right for both.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u

_STD = (src.NIST_SP811,)
_OLD = (src.CARDARELLI, src.ROWLETT)

rankine = u.K.scaled(Fraction(5, 9), "°R", "rankine", sources=_STD)
fahrenheit_degree = u.K.scaled(
    Fraction(5, 9), "°F (Δ)", "degree Fahrenheit (interval)", sources=_STD
)
celsius_degree = u.K.named("°C (Δ)", "degree Celsius (interval)", sources=(src.SI_BROCHURE,))
reaumur_degree = u.K.scaled(Fraction(5, 4), "°Ré (Δ)", "degree Réaumur (interval)", sources=_OLD)
romer_degree = u.K.scaled(Fraction(40, 21), "°Rø (Δ)", "degree Rømer (interval)", sources=_OLD)
delisle_degree = u.K.scaled(Fraction(2, 3), "°De (Δ)", "degree Delisle (interval)", sources=_OLD)
newton_degree = u.K.scaled(Fraction(100, 33), "°N (Δ)", "degree Newton (interval)", sources=_OLD)
