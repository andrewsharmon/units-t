"""Units of information: bits, bytes, SI and IEC binary multiples, and logarithmic units.

Information is dimensionless in the SI, so these share a dimension with :data:`one`
and the radian. One bit is taken as the unit, so a byte has scale 8. The nat and the
hartley are defined by logarithms (1 nat = 1/ln 2 bit, 1 hartley = log₂ 10 bit), so
they carry ln rounding terms.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import _irrational
from units_t import sources as src
from units_t.dimensions import DIMENSIONLESS
from units_t.unit import Unit

_STD = (src.ISO_80000,)

bit = Unit("bit", Fraction(1), DIMENSIONLESS, "bit", _STD)
shannon = bit.named("Sh", "shannon")
nibble = bit.scaled(4, "nibble", "nibble")
byte = bit.scaled(8, "B", "byte")
octet = byte.named("o", "octet")
nat = bit.scaled(
    1 / _irrational.LN2, "nat", "nat (nit, nepit)", uncertainty=((_irrational.LN2_TERM, -1),)
)
hartley = bit.scaled(
    _irrational.LN10 / _irrational.LN2,
    "Hart",
    "hartley (ban, dit)",
    uncertainty=((_irrational.LN10_TERM, 1), (_irrational.LN2_TERM, -1)),
)
ban = hartley
deciban = hartley.scaled("0.1", "dban", "deciban")

kilobyte = byte.scaled(10**3, "kB", "kilobyte")
megabyte = byte.scaled(10**6, "MB", "megabyte")
gigabyte = byte.scaled(10**9, "GB", "gigabyte")
terabyte = byte.scaled(10**12, "TB", "terabyte")
petabyte = byte.scaled(10**15, "PB", "petabyte")
exabyte = byte.scaled(10**18, "EB", "exabyte")
zettabyte = byte.scaled(10**21, "ZB", "zettabyte")
yottabyte = byte.scaled(10**24, "YB", "yottabyte")
ronnabyte = byte.scaled(10**27, "RB", "ronnabyte")
quettabyte = byte.scaled(10**30, "QB", "quettabyte")

kibibyte = byte.scaled(2**10, "KiB", "kibibyte")
mebibyte = byte.scaled(2**20, "MiB", "mebibyte")
gibibyte = byte.scaled(2**30, "GiB", "gibibyte")
tebibyte = byte.scaled(2**40, "TiB", "tebibyte")
pebibyte = byte.scaled(2**50, "PiB", "pebibyte")
exbibyte = byte.scaled(2**60, "EiB", "exbibyte")
zebibyte = byte.scaled(2**70, "ZiB", "zebibyte")
yobibyte = byte.scaled(2**80, "YiB", "yobibyte")

kilobit = bit.scaled(10**3, "kbit", "kilobit")
megabit = bit.scaled(10**6, "Mbit", "megabit")
gigabit = bit.scaled(10**9, "Gbit", "gigabit")
kibibit = bit.scaled(2**10, "Kibit", "kibibit")
mebibit = bit.scaled(2**20, "Mibit", "mebibit")
gibibit = bit.scaled(2**30, "Gibit", "gibibit")
