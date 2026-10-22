"""units-t: unit conversion and dimensional analysis down to fundamental constants."""

from importlib.metadata import PackageNotFoundError, version

from units_t import catalog, constants, sources, units
from units_t.dimensions import Dimension
from units_t.exceptions import DimensionError, UnitsError
from units_t.provenance import Certainty, Conversion, Source, UncertaintyTerm
from units_t.quantity import Quantity
from units_t.unit import Unit

try:
    __version__ = version("units-t")
except PackageNotFoundError:  # pragma: no cover - running from a source tree
    __version__ = "0.0.0"

__all__ = [
    "Certainty",
    "Conversion",
    "Dimension",
    "DimensionError",
    "Quantity",
    "Source",
    "UncertaintyTerm",
    "Unit",
    "UnitsError",
    "__version__",
    "catalog",
    "constants",
    "sources",
    "units",
]
