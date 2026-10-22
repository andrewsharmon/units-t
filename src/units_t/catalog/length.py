"""Units of length: international, survey, nautical, body-based English, physical, novelty.

The international inch, foot, yard and mile are exact by the 1959 yard-pound agreement
(see :mod:`units_t.units`). The US survey foot (1200/3937 m) is a *different* foot,
about 2 ppm longer. It was deprecated on 1 January 2023 but still underlies a century
of US land records, so survey units are kept separate with a ``survey_`` prefix.

Regional, ancient and typographic lengths are in :mod:`.regional`, :mod:`.ancient`
and :mod:`.typography`. Astronomical lengths are in :mod:`.astronomical`, and lengths
fixed by measured constants (Bohr radius, Planck length …) are in :mod:`.natural`.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional, nominal
from units_t.unit import Unit

_STD = (src.NIST_HB44, src.NIST_SP811)

# -- small international (1959) units ------------------------------------------

thou = u.inch.scaled(Fraction(1, 1000), "mil", "thou (mil)", sources=_STD)
barleycorn = u.inch.scaled(Fraction(1, 3), "barleycorn", "barleycorn", sources=(src.ZUPKO_1968,))
poppyseed = barleycorn.scaled(
    Fraction(1, 4), "poppyseed", "poppyseed", sources=(src.ZUPKO_1968, src.ROWLETT)
)
line = u.inch.scaled(
    Fraction(1, 12),
    "ln",
    "line (English)",
    sources=(src.ROWLETT,),
    uncertainty=conventional(
        "line", None, "1/12 in is the English line; the button line is 1/40 in"
    ),
    note="The button trade still uses a line of 1/40 in (ligne), so check context.",
)

# -- English body-based units --------------------------------------------------
#
# These were fixed in inches by late-medieval and Tudor custom, not by statute, and
# writers disagreed. Only the hand (horse heights) and the fathom have statutory
# values; the others are flagged CONVENTIONAL.

_BODY = (src.ZUPKO_1968, src.ROWLETT)


def _body(factor: int | str | Fraction, symbol: str, name: str, spread: str) -> Unit:
    return u.inch.scaled(
        factor,
        symbol,
        name,
        sources=_BODY,
        uncertainty=conventional(name, None, f"customary length in inches; {spread}"),
    )


digit = _body(Fraction(3, 4), "digit", "digit", "sometimes 13/16 in")
finger = _body(Fraction(7, 8), "finger", "finger (cloth)", "a finger's breadth is also ~3/4 in")
nail = _body(Fraction(9, 4), "nail", "nail (cloth)", "1/16 yard in the cloth trade")
palm = _body(3, "palm", "palm", "some writers use 4 in")
hand = u.inch.scaled(4, "hh", "hand", sources=_STD, note="Still used for horse heights.")
shaftment = _body(6, "shaftment", "shaftment", "Anglo-Saxon value ~6.5 in")
span = _body(9, "span", "span", "the distance across a spread hand")
cubit = _body(18, "cubit", "cubit (English)", "English cubit; ancient cubits are in .ancient")
ell = _body(45, "ell", "ell (English)", "the English cloth ell; the Flemish ell was 27 in")
flemish_ell = _body(27, "ell (Fl)", "Flemish ell", "regional cloth measure")
pace = _body(30, "pace", "pace (military)", "a 'pace' can also mean a double step of 5 ft")

# -- Gunter's chain, rods and furlongs (international foot) --------------------

fathom = u.ft.scaled(6, "fathom", "fathom", sources=_STD)
rope = u.ft.scaled(
    20,
    "rope",
    "rope",
    sources=(src.ZUPKO_1968,),
    uncertainty=conventional("rope", None, "obsolete; 20 ft is the usual value"),
)
link = u.ft.scaled(Fraction(66, 100), "li", "link (Gunter's)", sources=_STD)
rod = link.scaled(25, "rd", "rod (pole, perch)", sources=_STD)
pole = rod
perch = rod
chain = rod.scaled(4, "ch", "chain (Gunter's)", sources=_STD)
furlong = chain.scaled(
    10,
    "fur",
    "furlong",
    sources=_STD,
    note="10 chains = 40 rods = 220 yd = 1/8 mile, exactly 201.168 m. Originally the "
    "length of a furrow in a common field.",
)
league = u.mi.scaled(
    3,
    "lea",
    "league (land)",
    sources=(src.ROWLETT, src.CARDARELLI),
    uncertainty=conventional(
        "league", 0.5, "3 statute miles in English usage; continental leagues ran 3-7 km"
    ),
)
engineers_chain = u.ft.scaled(100, "ch (eng)", "engineer's (Ramsden's) chain", sources=_STD)
engineers_link = engineers_chain.scaled(Fraction(1, 100), "li (eng)", "engineer's link")

# -- US survey units (1200/3937 m foot, deprecated 2023) -----------------------

_SURVEY = (src.NIST_HB44, src.US_SURVEY_FOOT_2020)

survey_foot = u.m.scaled(
    Fraction(1200, 3937),
    "ft (US)",
    "US survey foot",
    sources=_SURVEY,
    note="Deprecated 1 Jan 2023; 1 survey ft = 1.000002 international ft.",
)
survey_link = survey_foot.scaled(Fraction(66, 100), "li (US)", "US survey link")
survey_rod = survey_link.scaled(25, "rd (US)", "US survey rod")
survey_chain = survey_rod.scaled(4, "ch (US)", "US survey chain")
survey_furlong = survey_chain.scaled(10, "fur (US)", "US survey furlong")
survey_mile = survey_furlong.scaled(8, "mi (US)", "US survey mile (statute mile)")
survey_league = survey_mile.scaled(3, "lea (US)", "US survey league")

# -- nautical ------------------------------------------------------------------

nautical_mile = u.m.scaled(
    1852,
    "nmi",
    "nautical mile (international)",
    sources=(src.SI_BROCHURE, src.NIST_SP811),
    note="Adopted 1929. Originally one minute of arc of latitude, which varies 1843-1862 m.",
)
nautical_league = nautical_mile.scaled(3, "nl", "nautical league")
cable = nautical_mile.scaled(Fraction(1, 10), "cbl", "cable length (international)")
us_cable = fathom.scaled(120, "cbl (US)", "cable length (US Navy)", sources=(src.ROWLETT,))
imperial_cable = u.ft.scaled(608, "cbl (UK)", "cable length (Royal Navy)", sources=(src.ROWLETT,))
admiralty_mile = u.ft.scaled(
    6080,
    "nmi (UK)",
    "Admiralty (UK nautical) mile",
    sources=(src.ROWLETT, src.NIST_SP811),
    note="Obsolete since 1970; 6080 ft = 1853.184 m.",
)

# -- metric and physics --------------------------------------------------------

angstrom = u.m.scaled(Fraction(1, 10**10), "Å", "ångström", sources=_STD)
micron = u.um.named("µ", "micron", sources=_STD, note="Old name for the micrometre.")
fermi = u.m.scaled(Fraction(1, 10**15), "fm", "fermi", sources=(src.NIST_SP811,))
myriametre = u.m.scaled(10**4, "mym", "myriametre", sources=(src.CARDARELLI,))
scandinavian_mile = u.m.scaled(
    10**4, "mil", "Scandinavian mile", sources=(src.ROWLETT,), note="Sweden and Norway, 10 km."
)

# -- standards and trade -------------------------------------------------------

rack_unit = u.inch.scaled(Fraction(7, 4), "U", "rack unit", sources=(src.EIA_310,))
football_field = u.yd.scaled(
    100,
    "football field",
    "American football field (goal line to goal line)",
    sources=(src.ROWLETT,),
    uncertainty=conventional("football field", 0.2, "100 yd of play; 120 yd including end zones"),
)

# -- informal and novelty ------------------------------------------------------

smoot = u.inch.scaled(
    67,
    "smoot",
    "smoot",
    sources=(src.MIT_SMOOT,),
    uncertainty=nominal(
        "smoot", "Oliver Smoot's height in 1958, recorded as 5 ft 7 in", relative=0.005
    ),
    note="364.4 smoots ± one ear = the Harvard Bridge.",
)
beard_second = u.nm.scaled(
    5,
    "beard-second",
    "beard-second",
    sources=(src.ROWLETT,),
    uncertainty=nominal("beard-second", "length a beard grows in one second; 5 nm or 10 nm"),
)
sheppey = u.mi.scaled(
    Fraction(7, 8),
    "sheppey",
    "sheppey",
    sources=(src.ROWLETT,),
    uncertainty=nominal(
        "sheppey",
        "the closest distance at which sheep remain picturesque (Douglas Adams & John Lloyd)",
    ),
)
mickey = u.inch.scaled(
    Fraction(1, 200),
    "mickey",
    "mickey",
    sources=(src.ROWLETT,),
    uncertainty=nominal("mickey", "smallest step a computer mouse detects; device dependent"),
)
potrzebie = u.mm.scaled(
    "2.263348517438173216473",
    "pz",
    "potrzebie",
    sources=(src.ROWLETT,),
    uncertainty=nominal(
        "potrzebie",
        "Donald Knuth's 1957 MAD Magazine system: the thickness of MAD issue 26; the "
        "22-digit 'precision' is a joke",
    ),
)
horse_length = u.ft.scaled(
    8,
    "horse length",
    "horse length",
    sources=(src.ROWLETT,),
    uncertainty=nominal("horse length", "racing margin, roughly 8 ft (2.4 m)", relative=0.1),
)
