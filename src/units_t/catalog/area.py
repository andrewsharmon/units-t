"""Units of area: metric, Anglo-American land measure, nuclear cross-sections, feudal.

Feudal English land units (hide, virgate, oxgang, carucate) measured how much land
could support a household or a plough team, not a fixed area. Their acre values are
rough central estimates and are flagged ESTIMATED.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _irrational
from units_t import sources as src
from units_t import units as u
from units_t.catalog import length as L
from units_t.provenance import conventional, estimated

_STD = (src.NIST_HB44, src.NIST_SP811)

# -- metric --------------------------------------------------------------------

are = (u.m**2).scaled(100, "a", "are", sources=_STD)
decare = are.scaled(10, "daa", "decare")
hectare = are.scaled(100, "ha", "hectare", sources=(src.SI_BROCHURE,))
dunam = decare.named(
    "dunam",
    "dunam (metric)",
    sources=(src.ROWLETT,),
    note="The Ottoman dunam was about 919 m²; the modern (metric) dunam is exactly 1000 m².",
)

# -- nuclear and particle cross-sections ---------------------------------------

barn = (u.m**2).scaled(Fraction(1, 10**28), "b", "barn", sources=_STD)
megabarn = barn.scaled(10**6, "Mb", "megabarn")
shed = barn.scaled(Fraction(1, 10**24), "shed", "shed", sources=(src.ROWLETT,))
outhouse = barn.scaled(Fraction(1, 10**6), "outhouse", "outhouse", sources=(src.ROWLETT,))

# -- Anglo-American ------------------------------------------------------------

square_inch = (u.inch**2).named("in²", "square inch")
square_foot = (u.ft**2).named("ft²", "square foot")
square_yard = (u.yd**2).named("yd²", "square yard")
square_mile = (u.mi**2).named("mi²", "square mile")
square_rod = (L.rod**2).named("rd²", "square rod (perch)")
square_chain = (L.chain**2).named("ch²", "square chain")
acre = (L.furlong * L.chain).named(
    "ac",
    "acre (international)",
    sources=_STD,
    note="1 furlong × 1 chain = 43 560 ft². A day's ploughing with an ox team.",
)
rood = acre.scaled(Fraction(1, 4), "ro", "rood", sources=(src.ZUPKO_1968,))
survey_acre = (L.survey_furlong * L.survey_chain).named("ac (US)", "US survey acre", sources=_STD)
section = (L.survey_mile**2).named("section", "section (US PLSS)", sources=_STD)
township = section.scaled(36, "twp", "township (US PLSS)")
circular_mil = (L.thou**2).scaled(
    _irrational.PI / 4,
    "cmil",
    "circular mil",
    sources=_STD,
    uncertainty=_irrational.PI_TERM,
    note="Area of a circle 1 mil in diameter; used for wire gauges.",
)
circular_inch = circular_mil.scaled(10**6, "cin", "circular inch")

# -- feudal England ------------------------------------------------------------

_FEUDAL = (src.ZUPKO_1968, src.ROWLETT)

hide = acre.scaled(
    120,
    "hide",
    "hide",
    sources=_FEUDAL,
    uncertainty=estimated(
        "hide", 0.5, "land to support one household; 60-180 acres by region and soil"
    ),
)
carucate = acre.scaled(
    120,
    "carucate",
    "carucate (ploughland)",
    sources=_FEUDAL,
    uncertainty=estimated("carucate", 0.5, "land one 8-ox team could plough in a year"),
)
virgate = hide.scaled(Fraction(1, 4), "virgate", "virgate (yardland)", sources=_FEUDAL)
oxgang = carucate.scaled(Fraction(1, 8), "oxgang", "oxgang (bovate)", sources=_FEUDAL)

# -- continental ---------------------------------------------------------------

morgen = (u.m**2).scaled(
    "2553.22",
    "morgen",
    "morgen (Prussian)",
    sources=(src.CARDARELLI,),
    uncertainty=conventional(
        "morgen", 0.5, "a morning's ploughing; 0.2-1.0 ha across German and Dutch states"
    ),
)
arpent = (u.m**2).scaled(
    "3418.89",
    "arpent",
    "arpent (de Paris)",
    sources=(src.CARDARELLI, src.ROWLETT),
    uncertainty=conventional(
        "arpent", 0.5, "arpent de Paris; the arpent d'ordonnance was ~5107 m², Louisiana ~3419 m²"
    ),
)
