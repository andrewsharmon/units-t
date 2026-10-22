"""Units of energy and power: CGS, calories and BTUs, fuels and explosives, horsepowers.

The calorie and the British thermal unit were originally "the heat that warms a gram
(or pound) of water by one degree". Water's heat capacity depends on temperature, which
gave a family of units:

* the *thermochemical* (4.184 J) and *International Table* (4.1868 J) calories are
  exact by definition, and so are the BTUs built from them;
* the 15 °C, 20 °C and "mean" calories and the 39 °F, 59 °F and 60 °F BTUs rest on
  measurements of water and are flagged MEASURED.

A BTU is a calorie scaled by (pound/gram) × (5/9), so ``btu_it`` and ``btu_th`` are
built from the calories exactly.

Fuel equivalents (tonne of oil equivalent, barrel of oil equivalent …) are accounting
conventions whose values differ between agencies. They are flagged CONVENTIONAL.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.catalog import mechanics as mech
from units_t.provenance import conventional, measured, nominal
from units_t.unit import Unit

_STD = (src.NIST_SP811,)
_PER_DEGREE_F = u.lb.scaled(Fraction(5, 9), "lb·°F") / u.g

# -- mechanical and CGS --------------------------------------------------------

erg = u.J.scaled(Fraction(1, 10**7), "erg", "erg", sources=_STD)
foot_pound = (mech.pound_force * u.ft).named("ft·lbf", "foot-pound (force)", sources=_STD)
inch_pound = (mech.pound_force * u.inch).named("in·lbf", "inch-pound (force)", sources=_STD)
foot_poundal = (mech.poundal * u.ft).named("ft·pdl", "foot-poundal", sources=_STD)
litre_atmosphere = (u.L * mech.atmosphere).named("L·atm", "litre-atmosphere", sources=_STD)
watt_hour = (u.W * u.h).named("W·h", "watt-hour")
kilowatt_hour = (u.kW * u.h).named("kW·h", "kilowatt-hour", sources=_STD)
foe = u.J.scaled(10**44, "foe", "foe (bethe)", sources=(src.ROWLETT,), note="10⁵¹ erg; supernovae.")

# -- calories ------------------------------------------------------------------

calorie_th = u.J.scaled("4.184", "cal_th", "calorie (thermochemical)", sources=_STD)
calorie_it = u.J.scaled("4.1868", "cal_IT", "calorie (International Table)", sources=_STD)
kilocalorie = calorie_th.scaled(
    1000,
    "kcal",
    "kilocalorie (food Calorie)",
    note="The nutritional 'Calorie'. US and EU labelling use the thermochemical value, 4.184 kJ.",
)


def _water_calorie(joules: str, symbol: str, name: str, key: str, relative: float) -> Unit:
    return u.J.scaled(
        joules,
        symbol,
        name,
        sources=_STD,
        uncertainty=measured(key, relative, "based on the measured specific heat of water"),
    )


calorie_15C = _water_calorie("4.18580", "cal₁₅", "calorie (15 °C)", "calorie (15 °C)", 1.2e-4)
calorie_20C = _water_calorie("4.18190", "cal₂₀", "calorie (20 °C)", "calorie (20 °C)", 1e-5)
calorie_mean = _water_calorie("4.19002", "cal_mean", "calorie (mean)", "calorie (mean)", 1e-5)

# -- British thermal units -----------------------------------------------------

btu_it = (calorie_it * _PER_DEGREE_F).named(
    "BTU", "British thermal unit (International Table)", sources=_STD, note="1055.055 852 62 J."
)
btu_th = (calorie_th * _PER_DEGREE_F).named(
    "BTU_th", "British thermal unit (thermochemical)", sources=_STD
)
btu_39F = _water_calorie("1059.67", "BTU₃₉", "British thermal unit (39 °F)", "BTU (39 °F)", 1e-5)
btu_59F = _water_calorie("1054.80", "BTU₅₉", "British thermal unit (59 °F)", "BTU (59 °F)", 1e-5)
btu_60F = _water_calorie("1054.68", "BTU₆₀", "British thermal unit (60 °F)", "BTU (60 °F)", 1e-5)
btu_mean = _water_calorie("1055.87", "BTU_mean", "British thermal unit (mean)", "BTU (mean)", 1e-5)
celsius_heat_unit = btu_it.scaled(
    Fraction(9, 5), "CHU", "Celsius heat unit", sources=(src.ROWLETT,)
)
therm = btu_it.scaled(10**5, "thm (EC)", "therm (EC)", sources=_STD)
us_therm = u.J.scaled(
    105_480_400,
    "thm (US)",
    "therm (US)",
    sources=_STD,
    note="Defined in US gas regulation as exactly 105 480 400 J (≈ 10⁵ BTU at 59 °F).",
)
quad = btu_it.scaled(10**15, "quad", "quad", sources=(src.ROWLETT,))
q_unit = btu_it.scaled(10**18, "Q", "Q unit", sources=(src.ROWLETT,))

# -- explosives and fuels ------------------------------------------------------

gram_of_tnt = calorie_th.scaled(
    1000,
    "g TNT",
    "gram of TNT",
    sources=_STD,
    note="Exact by convention. Real TNT releases 4.1-4.6 kJ/g depending on how it is measured.",
)
ton_of_tnt = gram_of_tnt.scaled(10**6, "t TNT", "ton of TNT")
kiloton_of_tnt = ton_of_tnt.scaled(1000, "kt TNT", "kiloton of TNT")
megaton_of_tnt = ton_of_tnt.scaled(10**6, "Mt TNT", "megaton of TNT")
tonne_of_oil_equivalent = calorie_it.scaled(
    10**10,
    "toe",
    "tonne of oil equivalent",
    sources=(src.ROWLETT,),
    uncertainty=conventional(
        "toe", 0.005, "IEA/OECD convention of 10⁷ kcal_IT = 41.868 GJ; some agencies use 42 GJ"
    ),
)
tonne_of_coal_equivalent = calorie_it.scaled(
    7 * 10**9,
    "tce",
    "tonne of coal equivalent",
    sources=(src.ROWLETT,),
    uncertainty=conventional("tce", 0.05, "7 Gcal_IT convention; real coals vary widely"),
)
barrel_of_oil_equivalent = btu_59F.scaled(
    "5.8e6",
    "BOE",
    "barrel of oil equivalent",
    sources=(src.ROWLETT,),
    uncertainty=conventional(
        "BOE", 0.05, "US IRS convention of 5.8 MMBtu; other agencies use 5.7-6.1 GJ"
    ),
)
cubic_foot_of_natural_gas = btu_it.scaled(
    1037,
    "cf (gas)",
    "cubic foot of natural gas",
    sources=(src.ROWLETT,),
    uncertainty=conventional(
        "natural gas heat content", 0.03, "US average heat content ≈ 1037 BTU/ft³; varies by field"
    ),
)

# -- radiant exposure ----------------------------------------------------------

langley = (calorie_th / u.cm**2).named("Ly", "langley", sources=_STD)

# -- power ---------------------------------------------------------------------

erg_per_second = (erg / u.s).named("erg/s", "erg per second")
btu_per_hour = (btu_it / u.h).named("BTU/h", "BTU per hour")
horsepower = (foot_pound / u.s).scaled(
    550,
    "hp",
    "horsepower (mechanical, imperial)",
    sources=_STD,
    note="550 ft·lbf/s ≈ 745.70 W. James Watt's estimate of a mill horse, rounded up.",
)
metric_horsepower = (mech.kilogram_force * u.m / u.s).scaled(
    75, "PS", "horsepower (metric, Pferdestärke)", sources=_STD
)
electrical_horsepower = u.W.scaled(746, "hp(E)", "horsepower (electrical)", sources=_STD)
boiler_horsepower = u.W.scaled(
    "9809.50",
    "hp(S)",
    "horsepower (boiler)",
    sources=_STD,
    uncertainty=conventional(
        "boiler horsepower", 1e-4, "33 475 BTU/h; the BTU used is not specified, so ~0.1% spread"
    ),
)
water_horsepower = u.W.scaled(
    "746.043",
    "hp (water)",
    "horsepower (water)",
    sources=_STD,
    uncertainty=conventional("water horsepower", 1e-5, "SP 811 value to 6 significant figures"),
)
poncelet = (mech.kilogram_force * u.m / u.s).scaled(100, "p", "poncelet", sources=(src.CARDARELLI,))
ton_of_refrigeration = btu_per_hour.scaled(
    12_000,
    "TR",
    "ton of refrigeration",
    sources=_STD,
    note="The rate of melting one short ton of ice per day.",
)
lusec = (u.L * mech.millimetre_of_mercury / u.s).scaled(
    Fraction(1, 1000),
    "lusec",
    "lusec",
    sources=(src.ROWLETT,),
    note="Vacuum-pump leak rate: 1 litre·micrometre of mercury per second.",
)
donkeypower = u.W.scaled(
    250,
    "donkeypower",
    "donkeypower",
    sources=(src.ROWLETT,),
    uncertainty=nominal("donkeypower", "about a third of a horsepower"),
)
