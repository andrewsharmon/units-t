"""Astronomical units of length, mass, power and spectral flux density.

Light-travel units use the exact speed of light and the exact Julian year. The parsec
is defined as exactly 648 000/π au (IAU 2015 B2), so it carries the π rounding term.

The IAU 2015 *nominal* solar and planetary values (R☉, L☉, GM☉ …) are exact
conversion constants by resolution. They are not the current best measurements of the
Sun or planets. A nominal solar radius is exactly 695 700 km even though the Sun has
no sharp edge.

Masses are a special case. The IAU fixed the *mass parameters* GM, which are measured
far better than G. Converting a solar mass to kilograms therefore brings in G's
2.2 × 10⁻⁵ uncertainty. Converting solar masses to Earth masses does not, because G
cancels.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _defining, _irrational
from units_t import sources as src
from units_t import units as u
from units_t.catalog._measured import G_TERM, G
from units_t.catalog.time import julian_year
from units_t.provenance import measured
from units_t.unit import Unit

_IAU = (src.IAU_2015_B3,)
_C = _defining.C

# -- light-travel distances ----------------------------------------------------

light_second = u.m.scaled(_C, "ls", "light-second", sources=(src.SI_BROCHURE,))
light_nanosecond = light_second.scaled(
    Fraction(1, 10**9),
    "lns",
    "light-nanosecond",
    note="≈ 29.98 cm, Grace Hopper's 'nanosecond' wire.",
)
light_minute = light_second.scaled(60, "lmin", "light-minute")
light_hour = light_minute.scaled(60, "lh", "light-hour")
light_day = light_hour.scaled(24, "ld", "light-day")
light_year = u.m.scaled(
    _C * julian_year.scale,
    "ly",
    "light-year",
    sources=(src.IAU_2012_B2, src.SI_BROCHURE),
    note="Light travel in one Julian year (365.25 d); exactly 9 460 730 472 580 800 m.",
)

# -- the parsec ----------------------------------------------------------------

parsec = u.au.scaled(
    648_000 / _irrational.PI,
    "pc",
    "parsec",
    sources=(src.IAU_2015_B2,),
    uncertainty=((_irrational.PI_TERM, -1),),
    note="Distance at which 1 au subtends 1 arcsecond.",
)
kiloparsec = u.prefixed("kilo", parsec).named("kpc", "kiloparsec")
megaparsec = u.prefixed("mega", parsec).named("Mpc", "megaparsec")
gigaparsec = u.prefixed("giga", parsec).named("Gpc", "gigaparsec")
attoparsec = u.prefixed("atto", parsec).named(
    "apc", "attoparsec", note="≈ 3.086 cm, about an inch."
)
siriometer = u.au.scaled(10**6, "siriometer", "siriometer", sources=(src.CARDARELLI,))

# -- the Moon ------------------------------------------------------------------

lunar_distance = u.km.scaled(
    384_399,
    "LD",
    "lunar distance (mean)",
    sources=(src.ASTRONOMICAL_ALMANAC,),
    uncertainty=measured(
        "lunar distance",
        1e-6,
        "semi-major axis of the lunar orbit; the actual distance ranges 363 300-405 500 km "
        "and grows ~3.8 cm/yr",
    ),
)

# -- IAU 2015 nominal radii and luminosity (exact by resolution) ---------------

solar_radius = u.km.scaled(695_700, "R☉", "nominal solar radius", sources=_IAU)
earth_equatorial_radius = u.km.scaled(
    "6378.1", "R⊕e", "nominal Earth equatorial radius", sources=_IAU
)
earth_polar_radius = u.km.scaled("6356.8", "R⊕p", "nominal Earth polar radius", sources=_IAU)
jupiter_equatorial_radius = u.km.scaled(
    71_492, "RJe", "nominal Jupiter equatorial radius", sources=_IAU
)
jupiter_polar_radius = u.km.scaled(66_854, "RJp", "nominal Jupiter polar radius", sources=_IAU)
solar_luminosity = u.W.scaled("3.828e26", "L☉", "nominal solar luminosity", sources=_IAU)
solar_constant = (u.W / u.m**2).scaled(1361, "S☉", "nominal total solar irradiance", sources=_IAU)

# -- masses from IAU nominal mass parameters (GM exact, G measured) ------------

_GM = u.m**3 / u.s**2


def _mass_from_gm(gm: str, symbol: str, name: str) -> Unit:
    return u.kg.scaled(
        Fraction(gm) / G,
        symbol,
        name,
        sources=(src.IAU_2015_B3, src.CODATA_2022),
        uncertainty=((G_TERM, -1),),
        note=f"(GM)ᴺ = {gm} m³/s² exactly (IAU 2015 B3), divided by the measured G.",
    )


solar_mass = _mass_from_gm("1.3271244e20", "M☉", "solar mass")
earth_mass = _mass_from_gm("3.986004e14", "M⊕", "Earth mass")
jupiter_mass = _mass_from_gm("1.2668653e17", "MJ", "Jupiter mass")

# -- radio astronomy -----------------------------------------------------------

jansky = (u.W / (u.m**2 * u.Hz)).scaled(
    Fraction(1, 10**26), "Jy", "jansky", sources=(src.NIST_SP811,)
)
solar_flux_unit = jansky.scaled(10**4, "sfu", "solar flux unit", sources=(src.ROWLETT,))
