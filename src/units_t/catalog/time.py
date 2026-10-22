"""Units of time: calendar, astronomical, physics, decimal, historical and informal.

The SI second is exact. A "day" here is 86 400 SI seconds, *not* one rotation of the
Earth: the mean solar day is currently ~1-2 ms longer and varies unpredictably, which is
why UTC has leap seconds. Astronomical periods (sidereal day, tropical year, synodic
month) are mean values at epoch J2000.0 and drift slowly. They are flagged MEASURED.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional, estimated, measured, nominal

_STD = (src.NIST_SP811,)
_ALMANAC = (src.ASTRONOMICAL_ALMANAC, src.IERS_CONVENTIONS)

week = u.day.scaled(7, "wk", "week")
fortnight = u.day.scaled(14, "fortnight", "fortnight", sources=(src.ROWLETT,))

# -- years ---------------------------------------------------------------------

julian_year = u.day.scaled(
    "365.25",
    "a",
    "Julian year",
    sources=(src.SI_BROCHURE, src.IAU_2012_B2),
    note="The year of the light-year. Exact by IAU convention.",
)
gregorian_year = u.day.scaled(
    "365.2425", "yr (Greg)", "Gregorian year (mean)", note="Mean over the 400-year cycle."
)
common_year = u.day.scaled(365, "yr (common)", "common year")
leap_year = u.day.scaled(366, "yr (leap)", "leap year")
julian_month = julian_year.scaled(Fraction(1, 12), "mo", "month (mean Julian)")
tropical_year = u.day.scaled(
    "365.24219",
    "yr (trop)",
    "tropical year (mean, J2000)",
    sources=_ALMANAC,
    uncertainty=measured(
        "tropical year", 2e-8, "equinox-to-equinox mean; shortens by ~0.5 s per century"
    ),
)
sidereal_year = u.day.scaled(
    "365.256363004",
    "yr (sid)",
    "sidereal year (J2000)",
    sources=_ALMANAC,
    uncertainty=measured("sidereal year", 1e-9, "Earth's orbital period against the stars"),
)
anomalistic_year = u.day.scaled(
    "365.259636",
    "yr (anom)",
    "anomalistic year (J2000)",
    sources=_ALMANAC,
    uncertainty=measured("anomalistic year", 1e-8, "perihelion to perihelion"),
)
draconic_year = u.day.scaled(
    "346.620075883",
    "yr (drac)",
    "draconic (eclipse) year (J2000)",
    sources=_ALMANAC,
    uncertainty=measured(
        "draconic year", 1e-9, "successive passages of the Sun through a lunar node"
    ),
)
_DECADES = conventional(
    "Julian decades", 1e-4, "multiples of the Julian year; calendar decades have 3652 or 3653 days"
)
decade = julian_year.scaled(10, "dec", "decade", uncertainty=_DECADES)
century = julian_year.scaled(100, "c", "century", uncertainty=_DECADES)
millennium = julian_year.scaled(1000, "millennium", "millennium", uncertainty=_DECADES)

# -- months and days -----------------------------------------------------------

synodic_month = u.day.scaled(
    "29.530588853",
    "mo (syn)",
    "synodic month (mean, J2000)",
    sources=_ALMANAC,
    uncertainty=measured(
        "synodic month", 1e-9, "new moon to new moon; individual months vary by ±7 hours"
    ),
)
sidereal_month = u.day.scaled(
    "27.321661",
    "mo (sid)",
    "sidereal month (mean, J2000)",
    sources=_ALMANAC,
    uncertainty=measured("sidereal month", 4e-8, "Moon's orbital period against the stars"),
)
sidereal_day = u.s.scaled(
    "86164.0905",
    "d (sid)",
    "sidereal day",
    sources=_ALMANAC,
    uncertainty=measured(
        "sidereal day", 2e-8, "one rotation relative to the equinox; length of day varies ~ms"
    ),
)
sol = u.s.scaled(
    "88775.244",
    "sol",
    "sol (Martian mean solar day)",
    sources=(src.ROWLETT,),
    uncertainty=measured("sol", 1e-8, "mean solar day on Mars (Allison 1997)"),
)

# -- physics -------------------------------------------------------------------

shake = u.ns.scaled(10, "shake", "shake", sources=_STD, note="From the Manhattan Project.")
svedberg = u.s.scaled(Fraction(1, 10**13), "S (sed)", "svedberg", sources=(src.ROWLETT,))
light_fermi = u.s.scaled(
    Fraction(1, 10**15) / 299_792_458,
    "jiffy (phys)",
    "jiffy (physics: light-fermi)",
    sources=(src.ROWLETT,),
    note="Time for light to cross 1 fm; exact since c is defined.",
)

# -- decimal and invented clocks -----------------------------------------------

decimal_hour = u.day.scaled(
    Fraction(1, 10), "h (dec)", "decimal hour (French Revolutionary)", sources=(src.CARDARELLI,)
)
decimal_minute = decimal_hour.scaled(Fraction(1, 100), "min (dec)", "decimal minute")
decimal_second = decimal_minute.scaled(Fraction(1, 100), "s (dec)", "decimal second")
beat = u.day.scaled(
    Fraction(1, 1000),
    ".beat",
    "Swatch beat",
    sources=(src.ROWLETT,),
    note="Swatch Internet Time, 1998.",
)
microcentury = century.scaled(
    Fraction(1, 10**6),
    "µc",
    "microcentury",
    sources=(src.ROWLETT,),
    note="≈ 52.6 min, the classic length of a lecture (attributed to von Neumann).",
)
nanocentury = century.scaled(
    Fraction(1, 10**9),
    "nc",
    "nanocentury",
    note="≈ 3.156 s, famously 'about π seconds' (Tom Duff).",
)

# -- historical ----------------------------------------------------------------

moment = u.h.scaled(
    Fraction(1, 40),
    "moment",
    "moment (medieval)",
    sources=(src.ROWLETT, src.CARDARELLI),
    uncertainty=conventional(
        "moment", None, "1/40 of a (solar) hour per Bede; hours varied with season"
    ),
)
helek = u.h.scaled(
    Fraction(1, 1080),
    "helek",
    "helek (ḥelek)",
    sources=(src.ROWLETT,),
    note="Hebrew calendar; exactly 3⅓ s.",
)
ke = u.day.scaled(
    Fraction(1, 100),
    "kè",
    "kè (刻, Chinese)",
    sources=(src.CARDARELLI,),
    uncertainty=conventional(
        "ke", 0.04, "1/100 day for most of Chinese history; 1/96 day (15 min) after 1645"
    ),
)

# -- informal ------------------------------------------------------------------

jiffy = u.s.scaled(
    Fraction(1, 60),
    "jiffy",
    "jiffy (electronics)",
    sources=(src.ROWLETT,),
    uncertainty=nominal(
        "jiffy", "one AC mains cycle (1/60 s US, 1/50 s EU); 1/100 s in Linux kernels"
    ),
)
dog_year = julian_year.scaled(
    Fraction(1, 7),
    "dog yr",
    "dog year",
    sources=(src.ROWLETT,),
    uncertainty=nominal("dog year", "the 7:1 rule of thumb; real canine ageing is not linear"),
)
galactic_year = julian_year.scaled(
    230 * 10**6,
    "GY",
    "galactic year",
    sources=(src.CARDARELLI,),
    uncertainty=estimated(
        "galactic year", 0.1, "Sun's orbit about the Galactic centre; 225-250 Myr"
    ),
)
