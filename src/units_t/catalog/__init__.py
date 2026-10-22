"""The full unit catalogue: every unit in :mod:`units_t.units` plus the esoteric ones.

Units are grouped into submodules by quantity or origin. Every unit is also available
by name directly from this package and in the :data:`ALL` registry::

    >>> from units_t import catalog as uc
    >>> from units_t import units as u
    >>> print((1 * uc.furlong).to(u.m))
    201.168 m
    >>> uc.bushel.conversion(u.L).is_exact
    True
    >>> uc.royal_cubit.certainty
    <Certainty.ESTIMATED: 4>

Each unit records its sources (``unit.sources``) and how well its conversion factor is
known (``unit.certainty``, ``unit.relative_uncertainty``). ``unit.conversion(other)``
returns the factor with its combined uncertainty and every source behind it. See
:mod:`units_t.provenance`.
"""

from __future__ import annotations

from types import ModuleType

from units_t import units as _core
from units_t.catalog import (
    ancient,
    angle,
    area,
    astronomical,
    electromagnetic,
    energy,
    information,
    length,
    mass,
    mechanics,
    natural,
    photometry,
    radiation,
    regional,
    temperature,
    time,
    typography,
    volume,
)
from units_t.provenance import Certainty
from units_t.unit import Unit

#: The catalogue submodules, in the order their units are registered.
MODULES: tuple[ModuleType, ...] = (
    length,
    area,
    volume,
    mass,
    time,
    mechanics,
    energy,
    electromagnetic,
    radiation,
    photometry,
    angle,
    information,
    temperature,
    typography,
    astronomical,
    natural,
    regional,
    ancient,
)


def _collect() -> dict[str, Unit]:
    """Gather every public module-level ``Unit``, refusing two units with one name."""
    registry: dict[str, Unit] = {}
    for module in (_core, *MODULES):
        for name, value in vars(module).items():
            if name.startswith("_") or not isinstance(value, Unit):
                continue
            existing = registry.get(name)
            if existing is not None and existing is not value:
                raise RuntimeError(f"unit name {name!r} is defined in two catalogue modules")
            registry[name] = value
    return registry


#: Every catalogued unit by its Python name. Aliases (``pole``, ``perch`` for ``rod``)
#: map to the same object.
ALL: dict[str, Unit] = _collect()


def get(name: str) -> Unit:
    """Look up a unit by its Python name, e.g. ``get("furlong")``."""
    try:
        return ALL[name]
    except KeyError:
        raise KeyError(f"no unit named {name!r}; try catalog.search()") from None


def search(text: str) -> dict[str, Unit]:
    """Units whose Python name, long name or symbol contains ``text`` (case-insensitive)."""
    needle = text.casefold()
    return {
        key: unit
        for key, unit in ALL.items()
        if needle in key.casefold()
        or needle in unit.name.casefold()
        or needle in unit.symbol.casefold()
    }


def with_certainty(*certainties: Certainty) -> dict[str, Unit]:
    """Units whose scale has one of the given certainties."""
    return {key: unit for key, unit in ALL.items() if unit.certainty in certainties}


def inexact() -> dict[str, Unit]:
    """Units whose stored scale is not exactly their defined value."""
    return {key: unit for key, unit in ALL.items() if not unit.is_exact}


def __getattr__(name: str) -> Unit:
    try:
        return ALL[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no unit {name!r}") from None


def __dir__() -> list[str]:
    return sorted({*globals(), *ALL})
