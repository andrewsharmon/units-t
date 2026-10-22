"""Units of velocity, acceleration, force, pressure and viscosity, and the slug.

Gravitational ("force-based") units such as the kilogram-force and the pound-force are
exact through the conventional standard gravity g₀ = 9.806 65 m/s² (3rd CGPM, 1901). They
do *not* use local gravity.

Manometric units (mmHg, inH₂O …) are pressures of a liquid column. The plain versions
use the conventional densities (13 595.1 kg/m³ for mercury, 1000 kg/m³ for water) and g₀,
so they are exact. The versions at a named temperature use the measured density at that
temperature and are flagged MEASURED.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.catalog import length as L
from units_t.provenance import conventional, measured

_STD = (src.NIST_SP811, src.NIST_HB44)

# -- velocity ------------------------------------------------------------------

knot = (L.nautical_mile / u.h).named("kn", "knot", sources=_STD)
mile_per_hour = (u.mi / u.h).named("mph", "mile per hour")
kilometre_per_hour = (u.km / u.h).named("km/h", "kilometre per hour")
foot_per_second = (u.ft / u.s).named("fps", "foot per second")
speed_of_light = (u.m / u.s).scaled(299_792_458, "c", "speed of light", sources=(src.SI_BROCHURE,))
mach = (u.m / u.s).scaled(
    "340.294",
    "Ma",
    "Mach (ISA sea level)",
    sources=(src.ROWLETT,),
    uncertainty=conventional(
        "Mach",
        0.1,
        "speed of sound in the ISA standard atmosphere at sea level, 15 °C; it is 331 m/s at "
        "0 °C and 295 m/s at 11 km. Mach number is really a ratio, not a unit",
    ),
)
furlong_per_fortnight = (L.furlong / u.day.scaled(14, "fortnight")).named(
    "fur/ftn",
    "furlong per fortnight",
    sources=(src.ROWLETT,),
    note="≈ 0.166 mm/s, about 1 cm per minute. The FFF system's unit of speed.",
)

# -- acceleration --------------------------------------------------------------

standard_gravity = (u.m / u.s**2).scaled(
    "9.80665", "g₀", "standard gravity", sources=(src.SI_BROCHURE, src.NIST_SP811)
)
gal = (u.cm / u.s**2).named("Gal", "gal (galileo)", sources=_STD)
milligal = gal.scaled(Fraction(1, 1000), "mGal", "milligal")

# -- force ---------------------------------------------------------------------

dyne = u.N.scaled(Fraction(1, 10**5), "dyn", "dyne", sources=_STD)
kilogram_force = (u.kg * standard_gravity).named("kgf", "kilogram-force (kilopond)", sources=_STD)
gram_force = kilogram_force.scaled(Fraction(1, 1000), "gf", "gram-force")
tonne_force = kilogram_force.scaled(1000, "tf", "tonne-force")
pound_force = (u.lb * standard_gravity).named("lbf", "pound-force", sources=_STD)
ounce_force = pound_force.scaled(Fraction(1, 16), "ozf", "ounce-force")
kip = pound_force.scaled(1000, "kip", "kip (kilopound-force)")
short_ton_force = pound_force.scaled(2000, "tonf (US)", "short ton-force")
long_ton_force = pound_force.scaled(2240, "tonf (UK)", "long ton-force")
poundal = (u.lb * u.ft / u.s**2).named("pdl", "poundal", sources=_STD)
sthene = u.N.scaled(1000, "sn", "sthène", sources=(src.CARDARELLI,))

# -- gravitational-system masses -----------------------------------------------

slug = (pound_force * u.s**2 / u.ft).named("slug", "slug", sources=_STD)
slinch = (pound_force * u.s**2 / u.inch).named("slinch", "slinch (blob)", sources=(src.ROWLETT,))
hyl = (kilogram_force * u.s**2 / u.m).named(
    "hyl", "hyl (metric slug, TME)", sources=(src.CARDARELLI,)
)

# -- pressure ------------------------------------------------------------------

bar = u.Pa.scaled(10**5, "bar", "bar", sources=_STD)
millibar = bar.scaled(Fraction(1, 1000), "mbar", "millibar")
barye = u.Pa.scaled(Fraction(1, 10), "Ba", "barye", sources=_STD)
pieze = u.kPa.named("pz (pressure)", "pièze", sources=(src.CARDARELLI,))
atmosphere = u.Pa.scaled(101_325, "atm", "standard atmosphere", sources=_STD)
technical_atmosphere = (kilogram_force / u.cm**2).named("at", "technical atmosphere", sources=_STD)
torr = atmosphere.scaled(Fraction(1, 760), "Torr", "torr", sources=_STD)
millitorr = torr.scaled(Fraction(1, 1000), "mTorr", "millitorr")
psi = (pound_force / u.inch**2).named("psi", "pound-force per square inch", sources=_STD)
ksi = psi.scaled(1000, "ksi", "kilopound-force per square inch")
psf = (pound_force / u.ft**2).named("psf", "pound-force per square foot")

_MERCURY = u.kg.scaled("13595.1", "kg") / u.m**3
_WATER = u.kg.scaled(1000, "kg") / u.m**3
millimetre_of_mercury = (_MERCURY * standard_gravity * u.mm).named(
    "mmHg",
    "millimetre of mercury (conventional)",
    sources=_STD,
    note="Exactly 133.322 387 415 Pa, about 1.4 parts in 10⁷ more than a torr.",
)
inch_of_mercury = (_MERCURY * standard_gravity * u.inch).named(
    "inHg", "inch of mercury (conventional)", sources=_STD
)
inch_of_mercury_60F = u.Pa.scaled(
    "3376.85",
    "inHg (60 °F)",
    "inch of mercury at 60 °F",
    sources=(src.NIST_SP811,),
    uncertainty=measured(
        "mercury at 60 °F",
        3e-6,
        "uses the measured density of mercury at 60 °F; 6 figures in SP 811",
    ),
)
millimetre_of_water = (_WATER * standard_gravity * u.mm).named(
    "mmH₂O", "millimetre of water (conventional)", sources=_STD
)
centimetre_of_water = (_WATER * standard_gravity * u.cm).named(
    "cmH₂O", "centimetre of water (conventional)", sources=_STD
)
metre_of_water = (_WATER * standard_gravity * u.m).named(
    "mH₂O", "metre of water (conventional)", sources=_STD
)
inch_of_water = (_WATER * standard_gravity * u.inch).named(
    "inH₂O", "inch of water (conventional)", sources=_STD
)
foot_of_water = (_WATER * standard_gravity * u.ft).named(
    "ftH₂O", "foot of water (conventional)", sources=_STD
)
inch_of_water_39F = u.Pa.scaled(
    "249.082",
    "inH₂O (39.2 °F)",
    "inch of water at 39.2 °F",
    sources=(src.NIST_SP811,),
    uncertainty=measured(
        "water at 39.2 °F", 4e-6, "uses the measured density of water at 39.2 °F (4 °C)"
    ),
)
inch_of_water_60F = u.Pa.scaled(
    "248.84",
    "inH₂O (60 °F)",
    "inch of water at 60 °F",
    sources=(src.NIST_SP811,),
    uncertainty=measured("water at 60 °F", 2e-5, "uses the measured density of water at 60 °F"),
)

# -- viscosity -----------------------------------------------------------------

poise = (u.Pa * u.s).scaled(Fraction(1, 10), "P", "poise", sources=_STD)
centipoise = poise.scaled(Fraction(1, 100), "cP", "centipoise")
reyn = (pound_force * u.s / u.inch**2).named("reyn", "reyn", sources=(src.ROWLETT,))
stokes = (u.m**2 / u.s).scaled(Fraction(1, 10**4), "St", "stokes", sources=_STD)
centistokes = stokes.scaled(Fraction(1, 100), "cSt", "centistokes")
