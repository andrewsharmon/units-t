"""Fundamental physical constants as :class:`~units_t.quantity.Quantity` objects.

Currently this holds the seven exact SI defining constants and constants that follow
exactly from them. Measured constants (G, m_e, alpha, ...) with CODATA uncertainties are
planned.
"""

from __future__ import annotations

from units_t import _defining
from units_t import units as u
from units_t.quantity import Quantity

# -- SI defining constants (exact) --------------------------------------------

#: Hyperfine transition frequency of caesium-133.
delta_nu_Cs = Quantity(_defining.DELTA_NU_CS, u.Hz)

#: Speed of light in vacuum.
c = Quantity(_defining.C, u.m / u.s)

#: Planck constant.
h = Quantity(_defining.H, u.J * u.s)

#: Elementary charge.
e = Quantity(_defining.E, u.C)

#: Boltzmann constant.
k_B = Quantity(_defining.K_B, u.J / u.K)

#: Avogadro constant.
N_A = Quantity(_defining.N_A, u.mol**-1)

#: Luminous efficacy of 540 THz monochromatic radiation.
K_cd = Quantity(_defining.K_CD, u.lm / u.W)

# -- Exact constants derived from the defining constants ----------------------

#: Molar gas constant, R = N_A · k_B.
R = (N_A * k_B).to(u.J / (u.mol * u.K))

#: Faraday constant, F = N_A · e.
F = (N_A * e).to(u.C / u.mol)
