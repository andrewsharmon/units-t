"""Physical dimensions as exponent vectors over the seven SI base dimensions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

#: Symbols of the SI base dimensions, in canonical order.
BASE_SYMBOLS: tuple[str, ...] = ("L", "M", "T", "I", "Θ", "N", "J")

#: Names of the SI base dimensions, in the same order as :data:`BASE_SYMBOLS`.
BASE_NAMES: tuple[str, ...] = (
    "length",
    "mass",
    "time",
    "electric_current",
    "thermodynamic_temperature",
    "amount_of_substance",
    "luminous_intensity",
)

Exponent = int | Fraction


@dataclass(frozen=True, slots=True)
class Dimension:
    """A product of SI base dimensions raised to rational powers.

    ``Dimension((1, 0, -1, 0, 0, 0, 0))`` is velocity, L·T^-1. Rational exponents
    are allowed so that quantities such as noise spectral density (V/√Hz) can be
    represented.
    """

    exponents: tuple[Exponent, ...] = (Fraction(0),) * len(BASE_SYMBOLS)

    def __post_init__(self) -> None:
        if len(self.exponents) != len(BASE_SYMBOLS):
            raise ValueError(f"expected {len(BASE_SYMBOLS)} exponents, got {len(self.exponents)}")
        object.__setattr__(self, "exponents", tuple(Fraction(e) for e in self.exponents))

    @classmethod
    def base(cls, symbol: str) -> Dimension:
        """Return the base dimension with the given symbol (e.g. ``"L"``)."""
        index = BASE_SYMBOLS.index(symbol)
        return cls(tuple(Fraction(int(i == index)) for i in range(len(BASE_SYMBOLS))))

    @property
    def is_dimensionless(self) -> bool:
        return all(e == 0 for e in self.exponents)

    def __mul__(self, other: Dimension) -> Dimension:
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(tuple(a + b for a, b in zip(self.exponents, other.exponents, strict=True)))

    def __truediv__(self, other: Dimension) -> Dimension:
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(tuple(a - b for a, b in zip(self.exponents, other.exponents, strict=True)))

    def __pow__(self, exponent: Exponent) -> Dimension:
        return Dimension(tuple(e * exponent for e in self.exponents))

    def __str__(self) -> str:
        if self.is_dimensionless:
            return "1"
        parts = []
        for symbol, exponent in zip(BASE_SYMBOLS, self.exponents, strict=True):
            if exponent == 0:
                continue
            if exponent == 1:
                parts.append(symbol)
            elif exponent.denominator == 1:
                parts.append(f"{symbol}^{exponent.numerator}")
            else:
                parts.append(f"{symbol}^({exponent})")
        return "·".join(parts)

    def __repr__(self) -> str:
        return f"Dimension({self})"


DIMENSIONLESS = Dimension()
LENGTH = Dimension.base("L")
MASS = Dimension.base("M")
TIME = Dimension.base("T")
CURRENT = Dimension.base("I")
TEMPERATURE = Dimension.base("Θ")
AMOUNT = Dimension.base("N")
LUMINOUS_INTENSITY = Dimension.base("J")
