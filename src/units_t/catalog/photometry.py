"""Photometric units: illuminance, luminance and luminous energy, including CGS and imperial.

Several luminance units (lambert, apostilb, foot-lambert, skot, bril) are defined with
a factor 1/π. That comes from the luminance of a perfect diffuser, so they carry the π
rounding term.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _irrational
from units_t import sources as src
from units_t import units as u
from units_t.provenance import estimated

_STD = (src.NIST_SP811,)
_INV_PI = ((_irrational.PI_TERM, -1),)
_CD_M2 = u.cd / u.m**2

# -- illuminance ---------------------------------------------------------------

phot = u.lx.scaled(10**4, "ph", "phot", sources=_STD)
foot_candle = (u.lm / u.ft**2).named("fc", "foot-candle", sources=_STD)
nox = u.lx.scaled(Fraction(1, 1000), "nx", "nox", sources=(src.CARDARELLI,))

# -- luminance -----------------------------------------------------------------

nit = _CD_M2.named("nt", "nit", sources=_STD)
stilb = _CD_M2.scaled(10**4, "sb", "stilb", sources=_STD)
lambert = _CD_M2.scaled(10**4 / _irrational.PI, "Lb", "lambert", sources=_STD, uncertainty=_INV_PI)
millilambert = lambert.scaled(Fraction(1, 1000), "mL (lum)", "millilambert")
apostilb = _CD_M2.scaled(
    1 / _irrational.PI, "asb", "apostilb (blondel)", sources=_STD, uncertainty=_INV_PI
)
blondel = apostilb
foot_lambert = (u.cd / u.ft**2).scaled(
    1 / _irrational.PI, "fL", "foot-lambert", sources=_STD, uncertainty=_INV_PI
)
skot = apostilb.scaled(Fraction(1, 1000), "sk", "skot", sources=(src.CARDARELLI,))
bril = apostilb.scaled(Fraction(1, 10**7), "bril", "bril", sources=(src.CARDARELLI,))

# -- luminous energy -----------------------------------------------------------

talbot = (u.lm * u.s).named("talbot", "talbot", sources=(src.ROWLETT,))
lumen_hour = (u.lm * u.h).named("lm·h", "lumen-hour")

# -- historical light standards ------------------------------------------------

hefner_candle = u.cd.scaled(
    "0.903",
    "HK",
    "Hefner candle (Hefnerkerze)",
    sources=(src.CARDARELLI, src.ROWLETT),
    uncertainty=estimated(
        "Hefner candle", 0.02, "flame of an amyl-acetate lamp; quoted as 0.90-0.92 cd"
    ),
)
international_candle = u.cd.scaled(
    "1.019",
    "ICP",
    "international candle",
    sources=(src.CARDARELLI, src.ROWLETT),
    uncertainty=estimated(
        "international candle", 0.005, "carbon-filament lamp standard of 1909; ≈ 1.02 cd"
    ),
)
