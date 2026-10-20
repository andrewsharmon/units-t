"""The :class:`Unit` type: an exact scale factor attached to a dimension."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import TYPE_CHECKING

from units_t.dimensions import Dimension, Exponent
from units_t.exceptions import DimensionError

if TYPE_CHECKING:
    from units_t.quantity import Number, Quantity


def _group(symbol: str) -> str:
    """Parenthesise a compound symbol so it can be safely combined."""
    return f"({symbol})" if any(c in symbol for c in "·/^") else symbol


@dataclass(frozen=True, slots=True)
class Unit:
    """A unit of measurement.

    ``scale`` is the exact factor that converts a value in this unit into the coherent
    SI unit of the same dimension: ``value_in_si = value * scale``. Two units compare
    equal when their scale and dimension match, regardless of symbol, so
    ``N * m == J``.
    """

    symbol: str = field(compare=False)
    scale: Fraction
    dimension: Dimension

    def __post_init__(self) -> None:
        object.__setattr__(self, "scale", Fraction(self.scale))

    # -- construction helpers -------------------------------------------------

    def named(self, symbol: str) -> Unit:
        """Return the same unit under a new symbol (e.g. ``(N * m).named("J")``)."""
        return Unit(symbol, self.scale, self.dimension)

    def scaled(self, factor: int | str | Fraction, symbol: str) -> Unit:
        """Return a new unit equal to ``factor`` of this one.

        ``factor`` may be an int, a ``Fraction`` or a decimal string; floats are
        deliberately not accepted so that definitions stay exact.
        """
        return Unit(symbol, self.scale * Fraction(factor), self.dimension)

    # -- analysis -------------------------------------------------------------

    def is_compatible(self, other: Unit) -> bool:
        """Whether a quantity in this unit can be converted to ``other``."""
        return self.dimension == other.dimension

    def conversion_factor(self, other: Unit) -> Fraction:
        """Exact factor ``f`` such that ``x [self] == x * f [other]``."""
        if not self.is_compatible(other):
            raise DimensionError(
                f"cannot convert {self} [{self.dimension}] to {other} [{other.dimension}]"
            )
        return self.scale / other.scale

    # -- algebra --------------------------------------------------------------

    def __mul__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            return NotImplemented
        return Unit(
            f"{self.symbol}·{other.symbol}",
            self.scale * other.scale,
            self.dimension * other.dimension,
        )

    def __truediv__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            return NotImplemented
        return Unit(
            f"{self.symbol}/{_group(other.symbol)}",
            self.scale / other.scale,
            self.dimension / other.dimension,
        )

    def __pow__(self, exponent: Exponent) -> Unit:
        exponent = Fraction(exponent)
        if exponent.denominator == 1:
            scale = self.scale**exponent.numerator
        else:
            # TODO: keep exact when the root is rational (e.g. sqrt(4/9)).
            scale = Fraction(float(self.scale) ** float(exponent))
        exp_str = str(exponent) if exponent.denominator == 1 else f"({exponent})"
        return Unit(f"{_group(self.symbol)}^{exp_str}", scale, self.dimension**exponent)

    def __rmul__(self, value: Number) -> Quantity:
        from units_t.quantity import Quantity

        return Quantity(value, self)

    def __rtruediv__(self, value: Number) -> Quantity:
        from units_t.quantity import Quantity

        return Quantity(value, self**-1)

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"Unit({self.symbol!r}, scale={self.scale}, dimension={self.dimension})"
