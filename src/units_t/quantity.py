"""The :class:`Quantity` type: a numerical value attached to a unit."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import total_ordering

from units_t.dimensions import Dimension, Exponent
from units_t.exceptions import DimensionError
from units_t.unit import Unit

Number = int | float | Fraction


@total_ordering
@dataclass(frozen=True, slots=True, eq=False)
class Quantity:
    """A value with a unit, e.g. ``Quantity(3, km)`` or equivalently ``3 * km``.

    Integer and ``Fraction`` values stay exact through conversion; floats are
    converted with a single multiplication by the exact conversion factor.
    """

    value: Number
    unit: Unit

    @property
    def dimension(self) -> Dimension:
        return self.unit.dimension

    @property
    def si_value(self) -> Number:
        """The value expressed in the coherent SI unit of this dimension."""
        return self.value * self.unit.scale

    def to(self, unit: Unit) -> Quantity:
        """Convert to ``unit``, raising :class:`DimensionError` if incompatible."""
        return Quantity(self.value * self.unit.conversion_factor(unit), unit)

    # -- arithmetic -----------------------------------------------------------

    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        return Quantity(self.value + other.to(self.unit).value, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        return Quantity(self.value - other.to(self.unit).value, self.unit)

    def __mul__(self, other: Quantity | Unit | Number) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit * other)
        if isinstance(other, int | float | Fraction):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    def __rmul__(self, other: Unit | Number) -> Quantity:
        if isinstance(other, Unit):
            return Quantity(self.value, other * self.unit)
        return self * other

    def __truediv__(self, other: Quantity | Unit | Number) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(_div(self.value, other.value), self.unit / other.unit)
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit / other)
        if isinstance(other, int | float | Fraction):
            return Quantity(_div(self.value, other), self.unit)
        return NotImplemented

    def __rtruediv__(self, other: Unit | Number) -> Quantity:
        if isinstance(other, Unit):
            return Quantity(_div(1, self.value), other / self.unit)
        if isinstance(other, int | float | Fraction):
            return Quantity(_div(other, self.value), self.unit**-1)
        return NotImplemented

    def __pow__(self, exponent: Exponent) -> Quantity:
        return Quantity(self.value**exponent, self.unit**exponent)

    def __neg__(self) -> Quantity:
        return Quantity(-self.value, self.unit)

    def __abs__(self) -> Quantity:
        return -self if self.value < 0 else self

    # -- comparison -----------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.dimension == other.dimension and self.si_value == other.si_value

    def __lt__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.dimension != other.dimension:
            raise DimensionError(f"cannot compare {self.unit} with {other.unit}")
        return self.si_value < other.si_value

    def __hash__(self) -> int:
        return hash((self.si_value, self.dimension))

    def __str__(self) -> str:
        # Exact values are shown as decimals for readability; ``.value`` stays exact.
        value = float(self.value) if isinstance(self.value, Fraction) else self.value
        return f"{value} {self.unit}"


def _div(a: Number, b: Number) -> Number:
    """Divide, keeping the result exact when both operands are exact."""
    if isinstance(a, int) and isinstance(b, int):
        return Fraction(a, b)
    return a / b
