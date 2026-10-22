"""Typographic units.

There have been many "points". Today's desktop-publishing point (PostScript "big point")
is exactly 1/72 in. TeX keeps the older American printer's point of 1/72.27 in. The
continental Didot point was standardised by Berthold in 1878 as 1/2660 m.

Font-relative units (em, en, ex) depend on the font size and are not units in this sense.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional

point = u.inch.scaled(
    Fraction(1, 72), "pt", "point (desktop publishing, PostScript)", sources=(src.POSTSCRIPT_REF,)
)
big_point = point.named("bp", "big point (TeX)", sources=(src.TEXBOOK,))
pica = point.scaled(12, "pc", "pica (DTP)")
twip = point.scaled(Fraction(1, 20), "twip", "twip", sources=(src.ROWLETT,))
tex_point = u.inch.scaled(Fraction(100, 7227), "pt (TeX)", "TeX point", sources=(src.TEXBOOK,))
scaled_point = tex_point.scaled(Fraction(1, 65536), "sp", "scaled point (TeX)")
american_printers_point = u.inch.scaled(
    "0.013837",
    "pt (ATF)",
    "printer's point (American Type Founders, 1886)",
    sources=(src.ROWLETT, src.CARDARELLI),
    note="Agrees with the TeX point to about 1 part in 10⁸, but is defined separately.",
)
didot_point = u.m.scaled(
    Fraction(1, 2660),
    "dd",
    "Didot point (Berthold)",
    sources=(src.CARDARELLI,),
    uncertainty=conventional(
        "Didot point",
        2e-4,
        "Berthold's 1/2660 m; Didot's own point, 1/864 pied du roi, is 0.37597 mm",
    ),
)
cicero = didot_point.scaled(12, "cc", "cicero")
q_unit_typesetting = u.mm.scaled(
    Fraction(1, 4), "Q", "Q (kyū, Japanese typesetting)", sources=(src.ROWLETT,)
)
