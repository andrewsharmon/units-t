"""The :class:`Unit` type: an exact scale factor attached to a dimension."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from typing import TYPE_CHECKING

from units_t.dimensions import Dimension, Exponent
from units_t.exceptions import DimensionError
from units_t.provenance import (
    Certainty,
    Conversion,
    Source,
    Terms,
    UncertaintyTerm,
    as_terms,
    combine_terms,
    merge_sources,
    power_terms,
    relative_uncertainty,
    worst_certainty,
)

if TYPE_CHECKING:
    from units_t.quantity import Number, Quantity

#: What ``scaled``/``named`` accept for a new unit's uncertainty.
UncertaintyLike = UncertaintyTerm | Iterable[tuple[UncertaintyTerm, Exponent]] | None


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

    The remaining fields are provenance and never affect equality. ``uncertainty_terms``
    records why ``scale`` might differ from the unit's true value (see
    :mod:`units_t.provenance`); it is empty for an exactly defined unit. ``sources``
    lists the citations behind the definition.
    """

    symbol: str = field(compare=False)
    scale: Fraction
    dimension: Dimension
    name: str = field(default="", compare=False)
    sources: tuple[Source, ...] = field(default=(), compare=False)
    note: str = field(default="", compare=False)
    uncertainty_terms: Terms = field(default=(), compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "scale", Fraction(self.scale))

    # -- construction helpers -------------------------------------------------

    def named(
        self,
        symbol: str,
        name: str = "",
        *,
        sources: Iterable[Source] = (),
        note: str = "",
        uncertainty: UncertaintyLike = None,
    ) -> Unit:
        """Return the same unit under a new symbol (e.g. ``(N * m).named("J")``)."""
        return self.scaled(1, symbol, name, sources=sources, note=note, uncertainty=uncertainty)

    def scaled(
        self,
        factor: int | str | Fraction,
        symbol: str,
        name: str = "",
        *,
        sources: Iterable[Source] = (),
        note: str = "",
        uncertainty: UncertaintyLike = None,
    ) -> Unit:
        """Return a new unit equal to ``factor`` of this one.

        ``factor`` may be an int, a ``Fraction`` or a decimal string; floats are
        deliberately not accepted so that definitions stay exact. The new unit inherits
        this unit's uncertainty terms and sources, plus any given here.
        """
        return Unit(
            symbol,
            self.scale * Fraction(factor),
            self.dimension,
            name=name,
            sources=merge_sources(self.sources, sources),
            note=note,
            uncertainty_terms=combine_terms(self.uncertainty_terms, as_terms(uncertainty)),
        )

    # -- analysis -------------------------------------------------------------

    @property
    def certainty(self) -> Certainty:
        """How well defined this unit's scale is (the worst of its uncertainty terms)."""
        return worst_certainty(self.uncertainty_terms)

    @property
    def relative_uncertainty(self) -> float | None:
        """Relative uncertainty of ``scale``: ``0.0`` if exact, ``None`` if unquantifiable."""
        return relative_uncertainty(self.uncertainty_terms)

    @property
    def is_exact(self) -> bool:
        """Whether ``scale`` is exactly the unit's defined value."""
        return not self.uncertainty_terms

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

    def conversion(self, other: Unit) -> Conversion:
        """The conversion factor to ``other`` together with its uncertainty and sources.

        Uncertainty terms shared by both units cancel, so e.g. converting between two
        units built on the same measured constant can still be exact.
        """
        return Conversion(
            source_unit=self.symbol,
            target_unit=other.symbol,
            factor=self.conversion_factor(other),
            terms=combine_terms(self.uncertainty_terms, other.uncertainty_terms, -1),
            sources=merge_sources(self.sources, other.sources),
        )

    # -- algebra --------------------------------------------------------------

    def __mul__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            return NotImplemented
        return Unit(
            f"{self.symbol}·{other.symbol}",
            self.scale * other.scale,
            self.dimension * other.dimension,
            sources=merge_sources(self.sources, other.sources),
            uncertainty_terms=combine_terms(self.uncertainty_terms, other.uncertainty_terms),
        )

    def __truediv__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            return NotImplemented
        return Unit(
            f"{self.symbol}/{_group(other.symbol)}",
            self.scale / other.scale,
            self.dimension / other.dimension,
            sources=merge_sources(self.sources, other.sources),
            uncertainty_terms=combine_terms(self.uncertainty_terms, other.uncertainty_terms, -1),
        )

    def __pow__(self, exponent: Exponent) -> Unit:
        exponent = Fraction(exponent)
        if exponent.denominator == 1:
            scale = self.scale**exponent.numerator
        else:
            # TODO: keep exact when the root is rational (e.g. sqrt(4/9)).
            scale = Fraction(float(self.scale) ** float(exponent))
        exp_str = str(exponent) if exponent.denominator == 1 else f"({exponent})"
        return Unit(
            f"{_group(self.symbol)}^{exp_str}",
            scale,
            self.dimension**exponent,
            sources=self.sources,
            uncertainty_terms=power_terms(self.uncertainty_terms, exponent),
        )

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
