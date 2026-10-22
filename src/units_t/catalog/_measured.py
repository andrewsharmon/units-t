"""Measured constants shared by several catalogue modules, with CODATA 2022 uncertainties.

Each constant gets exactly one :class:`~units_t.provenance.UncertaintyTerm`. Every unit
that depends on the constant reuses that term, so the units stay correlated: a Planck
length divided by a Planck time is exactly ``c``, and a solar mass divided by an Earth
mass does not depend on G at all.

CODATA also publishes correlation coefficients *between* adjusted constants (for
example between mₑ and m_u). Those are not modelled: distinct constants are treated
as independent, so a conversion between, say, electron masses and daltons may slightly
overstate its uncertainty.
"""

from __future__ import annotations

from fractions import Fraction

from units_t.provenance import UncertaintyTerm, measured


def codata_term(name: str, value: str, uncertainty: str) -> UncertaintyTerm:
    """Uncertainty term for a CODATA 2022 value given as ``value ± uncertainty`` (1σ)."""
    relative = float(Fraction(uncertainty) / Fraction(value))
    return measured(f"CODATA-2022 {name}", relative, f"CODATA 2022: {value} ± {uncertainty} (1σ)")


#: Newtonian constant of gravitation, m³ kg⁻¹ s⁻², CODATA 2022.
G = Fraction("6.67430e-11")
G_TERM = codata_term("G", "6.67430e-11", "0.00015e-11")
