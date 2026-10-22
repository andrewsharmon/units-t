"""High-precision rational approximations of irrational numbers used in unit definitions.

Some units are defined exactly in terms of π (degree, parsec, oersted, lambert …), a
logarithm (nat, hartley) or a square root (Planck units). Their true scale is irrational
and cannot be a ``Fraction``. We compute each number to :data:`DIGITS` significant
digits with :mod:`decimal` and record the rounding as an
:attr:`~units_t.provenance.Certainty.EXACT_IRRATIONAL` uncertainty term. The values are
computed here instead of typed in, so there are no transcription errors.
"""

from __future__ import annotations

from decimal import Context, Decimal, localcontext
from fractions import Fraction

from units_t.provenance import Certainty, UncertaintyTerm

#: Significant digits kept. The rounding error is below 10**-(DIGITS - 1) relative.
DIGITS = 60
_CTX = Context(prec=DIGITS + 10)
#: Bound on the relative rounding error of every value in this module.
ROUNDING = 10.0 ** -(DIGITS - 1)


def _round(x: Decimal) -> Fraction:
    return Fraction(Context(prec=DIGITS).plus(x))


def _arctan_inv(n: int) -> Decimal:
    """arctan(1/n) by its Taylor series."""
    with localcontext(_CTX):
        x = Decimal(1) / n
        x2 = x * x
        cutoff = Decimal(10) ** -(_CTX.prec + 2)
        total, term, k = Decimal(0), x, 0
        while term > cutoff:
            total += term / (2 * k + 1) * (-1) ** k
            term *= x2
            k += 1
        return total


def _pi() -> Decimal:
    """π by Machin's formula, π/4 = 4·arctan(1/5) − arctan(1/239)."""
    with localcontext(_CTX):
        return 4 * (4 * _arctan_inv(5) - _arctan_inv(239))


PI = _round(_pi())
LN2 = _round(Decimal(2).ln(_CTX))
LN10 = _round(Decimal(10).ln(_CTX))


def sqrt(x: Fraction) -> Fraction:
    """√x to :data:`DIGITS` significant digits."""
    with localcontext(_CTX):
        return _round((Decimal(x.numerator) / Decimal(x.denominator)).sqrt())


def rounding_term(key: str, what: str) -> UncertaintyTerm:
    """The uncertainty term for storing the irrational ``what`` as a rational."""
    return UncertaintyTerm(
        key,
        Certainty.EXACT_IRRATIONAL,
        ROUNDING,
        f"{what} is irrational; stored to {DIGITS} significant digits",
    )


PI_TERM = rounding_term("π", "π")
LN2_TERM = rounding_term("ln 2", "ln 2")
LN10_TERM = rounding_term("ln 10", "ln 10")
