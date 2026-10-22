"""Where a conversion factor comes from, and how far it can be trusted.

Every :class:`~units_t.unit.Unit` stores its scale as an exact ``Fraction``, but not
every unit *has* an exact value. A furlong is exactly 201.168 m by statute; a dalton
is known only to about 3 parts in 10¹⁰; an Egyptian royal cubit is an archaeological
estimate; a "pinch" of salt is whatever your grandmother said it was. This module
records that difference.

A unit carries zero or more :class:`UncertaintyTerm` objects, each raised to a power,
in the same way it carries a dimension. Each term is one *independent* reason the
scale might be off. Exponents add under multiplication and cancel under division, so
correlated uncertainty is handled correctly: a millidalton converts to a dalton
exactly, and a Planck length per Planck time is exactly ``c``, because the shared term
(the dalton's CODATA value, or G) cancels.

Units also carry the :class:`Source` citations their definitions come from. Sources
propagate through unit algebra, so a compound unit lists every source behind it.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from units_t.dimensions import Exponent


class Certainty(Enum):
    """How well defined a conversion factor is, from best to worst.

    The order matters: a compound unit takes the worst certainty of its terms.
    """

    #: Fixed exactly by a law, treaty or standard. The stored scale *is* the value.
    EXACT = 0
    #: Defined exactly, but the true value is irrational (it involves π, √, ln …). The
    #: stored scale is a rational approximation good to about 55 significant digits.
    EXACT_IRRATIONAL = 1
    #: Depends on a measured physical quantity (CODATA constants, Earth's rotation, …).
    #: ``relative`` is the 1σ relative standard uncertainty of the measurement.
    MEASURED = 2
    #: Several competing definitions exist (by era, region, trade or reference
    #: temperature). The stored value is one recognised convention and is exact *for that
    #: convention*. ``relative`` is the approximate spread among common variants, if known.
    CONVENTIONAL = 3
    #: A historical or archaeological reconstruction. ``relative`` is a rough spread of
    #: scholarly estimates, not a statistical uncertainty.
    ESTIMATED = 4
    #: Informal and inherently imprecise ("pinch", "jiffy", "horse length"). The stored
    #: value is a commonly quoted figure. ``relative`` is usually ``None``.
    NOMINAL = 5


@dataclass(frozen=True, slots=True)
class Source:
    """A citation for a unit definition or a value."""

    #: Short stable identifier, e.g. ``"NIST-SP811"``.
    key: str
    #: Human-readable citation.
    citation: str
    url: str = ""

    def __str__(self) -> str:
        return f"{self.citation} <{self.url}>" if self.url else self.citation


@dataclass(frozen=True, slots=True)
class UncertaintyTerm:
    """One independent source of uncertainty in a conversion factor.

    Two units that share the same term are correlated through it. ``key`` identifies
    the term, so it must be unique across the library.
    """

    key: str
    certainty: Certainty
    #: Relative standard uncertainty (or relative spread, see :class:`Certainty`) of
    #: the factor this term describes. ``None`` means it cannot be meaningfully
    #: quantified.
    relative: float | None
    description: str

    def __post_init__(self) -> None:
        if self.certainty is Certainty.EXACT:
            raise ValueError("an exact value needs no uncertainty term")


#: Terms raised to powers, sorted by key. ``()`` means the scale is exact.
Terms = tuple[tuple[UncertaintyTerm, Fraction], ...]


def as_terms(value: UncertaintyTerm | Iterable[tuple[UncertaintyTerm, Exponent]] | None) -> Terms:
    """Normalise a single term, an iterable of ``(term, exponent)`` pairs, or ``None``."""
    if value is None:
        return ()
    if isinstance(value, UncertaintyTerm):
        return ((value, Fraction(1)),)
    return combine_terms((), tuple((t, Fraction(e)) for t, e in value))


def combine_terms(a: Terms, b: Terms, factor: Exponent = 1) -> Terms:
    """Return the terms of ``a · b**factor``, dropping any whose exponent cancels to 0."""
    merged: dict[UncertaintyTerm, Fraction] = dict(a)
    for term, exponent in b:
        merged[term] = merged.get(term, Fraction(0)) + exponent * Fraction(factor)
    return tuple(
        sorted(((t, e) for t, e in merged.items() if e != 0), key=lambda pair: pair[0].key)
    )


def power_terms(terms: Terms, exponent: Exponent) -> Terms:
    """Return the terms of a unit raised to ``exponent``."""
    return combine_terms((), terms, exponent)


def worst_certainty(terms: Terms) -> Certainty:
    """The least certain category among ``terms`` (``EXACT`` if there are none)."""
    return max((t.certainty for t, _ in terms), key=lambda c: c.value, default=Certainty.EXACT)


def relative_uncertainty(terms: Terms) -> float | None:
    """Combined relative uncertainty, to first order: ``sqrt(Σ (exponent · relative)²)``.

    Terms are independent by construction, so they add in quadrature. Returns ``0.0``
    for an exact factor and ``None`` if any contributing term is unquantified.
    """
    total = 0.0
    for term, exponent in terms:
        if term.relative is None:
            return None
        total += (float(exponent) * term.relative) ** 2
    return math.sqrt(total)


def merge_sources(*groups: Iterable[Source]) -> tuple[Source, ...]:
    """Ordered union of several groups of sources."""
    seen: dict[Source, None] = {}
    for group in groups:
        for source in group:
            seen.setdefault(source, None)
    return tuple(seen)


@dataclass(frozen=True, slots=True)
class Conversion:
    """The full story of converting one unit to another.

    ``factor`` is exact *as stored*. ``certainty`` and ``relative_uncertainty`` say how
    far the stored factor may be from the true one.
    """

    source_unit: str
    target_unit: str
    factor: Fraction
    terms: Terms
    sources: tuple[Source, ...]

    @property
    def certainty(self) -> Certainty:
        return worst_certainty(self.terms)

    @property
    def relative_uncertainty(self) -> float | None:
        return relative_uncertainty(self.terms)

    @property
    def is_exact(self) -> bool:
        return not self.terms

    def explain(self) -> str:
        """A human-readable account of the factor, its uncertainty and its sources."""
        rel = self.relative_uncertainty
        if self.is_exact:
            how = "exact"
        elif rel is None:
            how = f"{self.certainty.name.lower()}, uncertainty not quantifiable"
        else:
            how = f"{self.certainty.name.lower()}, relative uncertainty ≈ {rel:.2g}"
        lines = [f"1 {self.source_unit} = {float(self.factor):.15g} {self.target_unit} ({how})"]
        for term, exponent in self.terms:
            power = "" if exponent == 1 else f" (power {exponent})"
            lines.append(f"  - {term.key}{power}: {term.description}")
        if self.sources:
            lines.append("  sources:")
            lines.extend(f"    * {source}" for source in self.sources)
        return "\n".join(lines)


# -- shorthand constructors for catalogue entries -----------------------------


def measured(key: str, relative: float, description: str) -> UncertaintyTerm:
    return UncertaintyTerm(key, Certainty.MEASURED, relative, description)


def conventional(key: str, relative: float | None, description: str) -> UncertaintyTerm:
    return UncertaintyTerm(key, Certainty.CONVENTIONAL, relative, description)


def estimated(key: str, relative: float | None, description: str) -> UncertaintyTerm:
    return UncertaintyTerm(key, Certainty.ESTIMATED, relative, description)


def nominal(key: str, description: str, relative: float | None = None) -> UncertaintyTerm:
    return UncertaintyTerm(key, Certainty.NOMINAL, relative, description)
