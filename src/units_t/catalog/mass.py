"""Units of mass: avoirdupois, troy, apothecaries', metric oddities, and the bushel by weight.

Three English weight systems share the grain (exactly 64.798 91 mg since 1959) and
nothing else. The avoirdupois pound is 7000 grains, the troy and apothecaries' pounds
5760. An ounce of gold (troy) is therefore heavier than an ounce of feathers
(avoirdupois), and a pound of gold is lighter than a pound of feathers.

Masses that depend on measured constants (dalton, electron mass, Planck mass) are in
:mod:`.natural`, and astronomical masses are in :mod:`.astronomical`. The slug and other
gravitational-system masses are in :mod:`.mechanics`.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional
from units_t.unit import Unit

_STD = (src.NIST_HB44, src.NIST_SP811)

# -- avoirdupois ---------------------------------------------------------------

grain = u.lb.scaled(Fraction(1, 7000), "gr", "grain", sources=_STD)
avoirdupois_dram = u.oz.scaled(Fraction(1, 16), "dr", "dram (avoirdupois)", sources=_STD)
stone = u.lb.scaled(14, "st", "stone", sources=(src.UK_WMA_1985,))
quarter_mass = u.lb.scaled(28, "qr", "quarter (avoirdupois, UK)", sources=_STD)
short_hundredweight = u.lb.scaled(100, "cwt (US)", "short hundredweight", sources=_STD)
long_hundredweight = u.lb.scaled(112, "cwt", "long hundredweight", sources=_STD)
short_ton = u.lb.scaled(2000, "ton (US)", "short ton", sources=_STD)
long_ton = u.lb.scaled(2240, "ton (UK)", "long ton", sources=_STD)
kip_mass = u.lb.scaled(1000, "kip (mass)", "kip (kilopound, mass)", sources=(src.ROWLETT,))

# -- troy (precious metals) ----------------------------------------------------

mite = grain.scaled(Fraction(1, 20), "mite", "mite", sources=(src.ROWLETT,))
pennyweight = grain.scaled(24, "dwt", "pennyweight", sources=_STD)
troy_ounce = grain.scaled(480, "oz t", "troy ounce", sources=_STD)
troy_pound = troy_ounce.scaled(12, "lb t", "troy pound", sources=_STD)

# -- apothecaries' -------------------------------------------------------------

scruple = grain.scaled(20, "℈", "scruple (apothecaries')", sources=_STD)
apothecaries_dram = scruple.scaled(3, "ʒ", "dram (apothecaries')", sources=_STD)
apothecaries_ounce = apothecaries_dram.scaled(8, "℥", "ounce (apothecaries')", sources=_STD)
apothecaries_pound = apothecaries_ounce.scaled(12, "lb ap", "pound (apothecaries')", sources=_STD)

# -- metric and trade ----------------------------------------------------------

carat = u.mg.scaled(200, "ct", "carat (metric)", sources=_STD)
carat_point = carat.scaled(Fraction(1, 100), "pt (ct)", "point (of a carat)")
metric_grain = u.mg.scaled(50, "gr (metric)", "metric grain", sources=(src.ROWLETT,))
gamma_mass = u.g.scaled(Fraction(1, 10**6), "γ", "gamma (microgram)", sources=(src.NIST_SP811,))
quintal = u.kg.scaled(100, "q", "quintal (metric)", sources=(src.CARDARELLI,))
myriagram = u.kg.scaled(10, "myg", "myriagram", sources=(src.CARDARELLI,))
grave = u.kg.named(
    "grave", "grave", sources=(src.CARDARELLI,), note="The 1793 French name for the kilogram."
)

# -- the bushel as a weight ----------------------------------------------------
#
# US grain is traded by the "bushel", but by weight: each crop has a legal standard
# bushel mass, regardless of how much volume the grain takes up. Each value is exact as
# a US convention, but other jurisdictions chose differently (a Canadian bushel of oats
# is 34 lb, not 32), so they are flagged CONVENTIONAL. Turning one into a *volume*
# bushel also depends on the grain's moisture and test weight. That is not a unit
# conversion and is not modelled. A bushel of feathers is not defined.

_BUSHEL = conventional(
    "bushel by weight",
    None,
    "US legal standard bushel weight per crop; other countries differ (Canadian oats: 34 lb)",
)


def _bushel_of(pounds: int, crop: str) -> Unit:
    return u.lb.scaled(
        pounds,
        f"bu ({crop})",
        f"bushel of {crop} (US)",
        sources=(src.USDA_AH697,),
        uncertainty=_BUSHEL,
    )


bushel_of_wheat = _bushel_of(60, "wheat")
bushel_of_soybeans = _bushel_of(60, "soybeans")
bushel_of_corn = _bushel_of(56, "shelled corn")
bushel_of_rye = _bushel_of(56, "rye")
bushel_of_sorghum = _bushel_of(56, "sorghum")
bushel_of_flaxseed = _bushel_of(56, "flaxseed")
bushel_of_barley = _bushel_of(48, "barley")
bushel_of_rough_rice = _bushel_of(45, "rough rice")
bushel_of_oats = _bushel_of(32, "oats")
