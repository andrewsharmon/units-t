"""Exceptions raised by units-t."""


class UnitsError(Exception):
    """Base class for all units-t errors."""


class DimensionError(UnitsError, ValueError):
    """Raised when an operation combines quantities of incompatible dimensions."""
