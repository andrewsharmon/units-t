"""Units fixed by measured physical constants: Planck, atomic and particle-physics units.

Since 2019, h, c, e and k_B are exact, but G and every particle mass are still measured.
Each measured constant contributes one shared uncertainty term (see :mod:`._measured`).
So Planck units carry G's 2.2 × 10⁻⁵ uncertainty (to the power ±½), but ratios such as
``planck_length / planck_time`` (exactly ``c``) do not.

ħ = h/2π, so everything built on ħ also carries the π rounding term, and Planck units
carry a √ rounding term too. Both are far below the measurement uncertainties.

Values: CODATA 2022.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _defining, _irrational
from units_t import sources as src
from units_t import units as u
from units_t.catalog._measured import G_TERM, G, codata_term
from units_t.unit import Unit

_CODATA = (src.CODATA_2022,)
_H, _C, _KB = _defining.H, _defining.C, _defining.K_B
_PI = _irrational.PI
_HALF = Fraction(1, 2)


def _codata(
    name: str,
    value: str,
    uncertainty: str,
    base: Unit,
    symbol: str,
    display: str = "",
    note: str = "",
) -> Unit:
    """A unit equal to a CODATA 2022 value, carrying that constant's uncertainty term."""
    return base.scaled(
        value,
        symbol,
        display or name,
        sources=_CODATA,
        note=note,
        uncertainty=codata_term(name, value, uncertainty),
    )


# -- Planck units --------------------------------------------------------------

planck_length = u.m.scaled(
    _irrational.sqrt(_H * G / (2 * _PI * _C**3)),
    "l_P",
    "Planck length",
    sources=_CODATA,
    uncertainty=(
        (G_TERM, _HALF),
        (_irrational.PI_TERM, -_HALF),
        (_irrational.rounding_term("√ l_P", "√(ħG/c³)"), 1),
    ),
    note="√(ħG/c³) ≈ 1.616 255 × 10⁻³⁵ m.",
)
planck_time = (planck_length / (u.m / u.s).scaled(_C, "c")).named(
    "t_P", "Planck time", note="Defined as l_P / c, so l_P / t_P is exactly c."
)
planck_mass = u.kg.scaled(
    _irrational.sqrt(_H * _C / (2 * _PI * G)),
    "m_P",
    "Planck mass",
    sources=_CODATA,
    uncertainty=(
        (G_TERM, -_HALF),
        (_irrational.PI_TERM, -_HALF),
        (_irrational.rounding_term("√ m_P", "√(ħc/G)"), 1),
    ),
    note="√(ħc/G) ≈ 21.76 µg, roughly a flea egg.",
)
_C_UNIT = (u.m / u.s).scaled(_C, "c")
planck_energy = (planck_mass * _C_UNIT**2).named("E_P", "Planck energy")
planck_temperature = (planck_energy / (u.J / u.K).scaled(_KB, "k_B")).named(
    "T_P", "Planck temperature"
)

# -- natural units (ħ = c = 1) in GeV ------------------------------------------

_HBAR = (u.J * u.s).scaled(
    _H / (2 * _PI),
    "ħ",
    "reduced Planck constant",
    sources=(src.SI_BROCHURE,),
    uncertainty=_irrational.PI_TERM,
)
natural_length_gev = (_HBAR * _C_UNIT / u.GeV).named(
    "ħc/GeV", "natural unit of length (ħc/GeV)", note="≈ 0.1973 fm; exact up to π rounding."
)
natural_time_gev = (_HBAR / u.GeV).named("ħ/GeV", "natural unit of time (ħ/GeV)")

# -- atomic units (Hartree) ----------------------------------------------------

hartree = _codata("Hartree energy", "4.3597447222060e-18", "0.0000000000048e-18", u.J, "E_h")
rydberg = hartree.scaled(_HALF, "Ry", "rydberg (energy)")
bohr_radius = _codata("Bohr radius", "5.29177210544e-11", "0.00000000082e-11", u.m, "a₀")
electron_mass = _codata("electron mass", "9.1093837139e-31", "0.0000000028e-31", u.kg, "mₑ")
atomic_unit_of_time = (_HBAR / hartree).named("ħ/E_h", "atomic unit of time")
atomic_unit_of_velocity = (bohr_radius * hartree / _HBAR).named(
    "a₀E_h/ħ", "atomic unit of velocity"
)
atomic_unit_of_force = (hartree / bohr_radius).named("E_h/a₀", "atomic unit of force")
classical_electron_radius = _codata(
    "classical electron radius", "2.8179403205e-15", "0.0000000013e-15", u.m, "rₑ"
)
compton_wavelength = _codata(
    "Compton wavelength", "2.42631023538e-12", "0.00000000076e-12", u.m, "λ_C"
)

# -- particle masses -----------------------------------------------------------

dalton = _codata(
    "atomic mass constant",
    "1.66053906892e-27",
    "0.00000000052e-27",
    u.kg,
    "Da",
    "dalton (unified atomic mass unit)",
    note="1/12 of the mass of a carbon-12 atom.",
)
unified_atomic_mass_unit = dalton
proton_mass = _codata("proton mass", "1.67262192595e-27", "0.00000000052e-27", u.kg, "m_p")
neutron_mass = _codata("neutron mass", "1.67492750056e-27", "0.00000000085e-27", u.kg, "m_n")
muon_mass = _codata("muon mass", "1.883531627e-28", "0.000000042e-28", u.kg, "m_μ")
electronvolt_mass = (u.eV / _C_UNIT**2).named(
    "eV/c²", "electronvolt per c²", note="Exact: e and c are both defining constants."
)

# -- X-ray wavelength standards ------------------------------------------------

copper_x_unit = _codata("Copper x unit", "1.00207697e-13", "0.00000028e-13", u.m, "xu(Cu Kα₁)")
molybdenum_x_unit = _codata(
    "Molybdenum x unit", "1.00209952e-13", "0.00000053e-13", u.m, "xu(Mo Kα₁)"
)
angstrom_star = _codata("Angstrom star", "1.00001495e-10", "0.00000090e-10", u.m, "Å*")
