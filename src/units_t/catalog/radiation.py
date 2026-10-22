"""Units of radioactivity and ionising radiation dose, including pre-SI units."""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional, nominal

_STD = (src.NIST_SP811,)

curie = u.Bq.scaled(37 * 10**9, "Ci", "curie", sources=_STD, note="Originally 1 g of radium-226.")
rutherford = u.Bq.scaled(10**6, "Rd", "rutherford", sources=(src.ROWLETT,))
roentgen = (u.C / u.kg).scaled("2.58e-4", "R", "röntgen", sources=_STD)
rad_dose = u.Gy.scaled(Fraction(1, 100), "rad", "rad (absorbed dose)", sources=_STD)
rem = u.Sv.scaled(Fraction(1, 100), "rem", "rem", sources=_STD)
eman = (u.Bq / u.L).scaled(
    Fraction(37, 10), "eman", "eman", sources=(src.ROWLETT,), note="10⁻¹⁰ Ci/L; radon in water."
)
mache = (u.Bq / u.L).scaled(
    "13.468",
    "ME",
    "mache",
    sources=(src.ROWLETT, src.CARDARELLI),
    uncertainty=conventional("mache", 1e-3, "3.64 × 10⁻¹⁰ Ci/L; older sources give 3.6 or 3.7"),
)
banana_equivalent_dose = u.Sv.scaled(
    Fraction(1, 10**7),
    "BED",
    "banana equivalent dose",
    sources=(src.ROWLETT,),
    uncertainty=nominal(
        "banana equivalent dose",
        "≈ 0.1 µSv for eating one banana (from potassium-40); estimates run 0.01-0.1 µSv",
    ),
)
