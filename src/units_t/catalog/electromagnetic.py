"""CGS electromagnetic units (EMU, ESU and Gaussian), expressed as their SI counterparts.

**Caution.** CGS electromagnetic units do not have the same dimensions as SI units: in
the Gaussian system charge is M^(1/2)·L^(3/2)·T^-1. The entries here are the standard
*correspondences* in NIST SP 811 (1 G ↔ 10⁻⁴ T, 1 statC ↔ 1/(10c) C …), so they can be
converted to SI. They do not reproduce Gaussian-system dimensional analysis.

The factor 4π in the oersted and gilbert is the rationalisation factor between the
systems. It is exact in the conventional correspondence, but irrational, so those units
carry the π rounding term. Since 2019 the SI vacuum permeability μ₀ is *measured*
(μ₀/(4π·10⁻⁷ N/A²) = 1 + 5.5·10⁻¹⁰). The conventional factor ignores that tiny
difference, as NIST SP 811 does.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _defining, _irrational
from units_t import sources as src
from units_t import units as u

_STD = (src.NIST_SP811,)
_C = _defining.C  # m/s

# -- EMU (abunits) -------------------------------------------------------------

abampere = u.A.scaled(10, "abA", "abampere (biot)", sources=_STD)
biot = abampere
abcoulomb = u.C.scaled(10, "abC", "abcoulomb", sources=_STD)
abvolt = u.V.scaled(Fraction(1, 10**8), "abV", "abvolt", sources=_STD)
abohm = u.ohm.scaled(Fraction(1, 10**9), "abΩ", "abohm", sources=_STD)
abfarad = u.F.scaled(10**9, "abF", "abfarad", sources=_STD)
abhenry = u.H.scaled(Fraction(1, 10**9), "abH", "abhenry", sources=_STD)
absiemens = u.S.scaled(10**9, "abS", "absiemens (abmho)", sources=_STD)

# -- ESU (statunits); exact because c is exact ---------------------------------

statcoulomb = u.C.scaled(Fraction(1, 10) / _C, "statC", "statcoulomb (franklin)", sources=_STD)
franklin = statcoulomb
statampere = u.A.scaled(Fraction(1, 10) / _C, "statA", "statampere", sources=_STD)
statvolt = u.V.scaled(_C / 10**6, "statV", "statvolt", sources=_STD)
statohm = u.ohm.scaled(_C**2 / 10**5, "statΩ", "statohm", sources=_STD)
statfarad = u.F.scaled(10**5 / _C**2, "statF", "statfarad", sources=_STD)
debye = (u.C * u.m).scaled(
    Fraction(1, 10**21) / _C,
    "D",
    "debye",
    sources=_STD,
    note="10⁻¹⁸ statC·cm; molecular electric dipole moments.",
)

# -- magnetism -----------------------------------------------------------------

gauss = u.T.scaled(Fraction(1, 10**4), "G", "gauss", sources=_STD)
gamma_field = u.T.scaled(Fraction(1, 10**9), "γ", "gamma (nanotesla)", sources=_STD)
maxwell = u.Wb.scaled(Fraction(1, 10**8), "Mx", "maxwell", sources=_STD)
oersted = (u.A / u.m).scaled(
    1000 / (4 * _irrational.PI),
    "Oe",
    "oersted",
    sources=_STD,
    uncertainty=((_irrational.PI_TERM, -1),),
)
gilbert = u.A.scaled(
    10 / (4 * _irrational.PI),
    "Gb",
    "gilbert",
    sources=_STD,
    uncertainty=((_irrational.PI_TERM, -1),),
)
ampere_turn = u.A.named("At", "ampere-turn", sources=_STD)
