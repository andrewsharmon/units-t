"""Exact numerical values of the seven SI defining constants (SI Brochure, 9th ed., 2019).

These are the bedrock of the library: every SI base unit, and therefore every unit
defined in terms of them, is fixed by these numbers. They are stored as exact
``Fraction`` values so that derived conversion factors stay exact.
"""

from fractions import Fraction

#: Hyperfine transition frequency of caesium-133, in Hz. Defines the second.
DELTA_NU_CS = Fraction(9_192_631_770)

#: Speed of light in vacuum, in m/s. Defines the metre.
C = Fraction(299_792_458)

#: Planck constant, in J·s. Defines the kilogram.
H = Fraction("6.62607015e-34")

#: Elementary charge, in C. Defines the ampere.
E = Fraction("1.602176634e-19")

#: Boltzmann constant, in J/K. Defines the kelvin.
K_B = Fraction("1.380649e-23")

#: Avogadro constant, in 1/mol. Defines the mole.
N_A = Fraction("6.02214076e23")

#: Luminous efficacy of 540 THz monochromatic radiation, in lm/W. Defines the candela.
K_CD = Fraction(683)
