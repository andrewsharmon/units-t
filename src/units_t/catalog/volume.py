"""Units of volume: US liquid and dry, British imperial, casks, bottles, kitchens, timber.

The US and Britain split in 1824. The US kept two pre-1824 English gallons: the
231 in³ Queen Anne wine gallon for liquids and the Winchester bushel (2150.42 in³)
for dry goods. Britain replaced both with the imperial gallon, now exactly 4.54609 L.
So there are three "pints" and two "bushels" here, and every name says which it is.

Cask and bottle names (hogshead, firkin, jeroboam …) changed size with the commodity
and the century. The values here are the most common modern convention, flagged
CONVENTIONAL.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.catalog import length as L
from units_t.provenance import conventional, nominal
from units_t.unit import Unit

_STD = (src.NIST_HB44, src.NIST_SP811)
_CASK = (src.ROWLETT, src.CARDARELLI, src.ZUPKO_1968)

cubic_inch = (u.inch**3).named("in³", "cubic inch")
cubic_foot = (u.ft**3).named("ft³", "cubic foot")
cubic_yard = (u.yd**3).named("yd³", "cubic yard")
cubic_mile = (u.mi**3).named("mi³", "cubic mile")
lambda_ = u.L.scaled(Fraction(1, 10**6), "λ", "lambda (microlitre)", sources=(src.NIST_SP811,))
stere = (u.m**3).named("st", "stère", sources=(src.CARDARELLI,))

# -- US liquid (Queen Anne wine gallon, 1707) ----------------------------------

us_gallon = cubic_inch.scaled(231, "gal", "US liquid gallon", sources=_STD)
us_quart = us_gallon.scaled(Fraction(1, 4), "qt", "US liquid quart")
us_pint = us_quart.scaled(Fraction(1, 2), "pt", "US liquid pint")
us_cup = us_pint.scaled(Fraction(1, 2), "cup", "US customary cup")
us_gill = us_pint.scaled(Fraction(1, 4), "gi", "US gill")
us_fluid_ounce = us_gallon.scaled(Fraction(1, 128), "fl oz", "US fluid ounce")
us_tablespoon = us_fluid_ounce.scaled(Fraction(1, 2), "tbsp", "US tablespoon")
us_teaspoon = us_tablespoon.scaled(Fraction(1, 3), "tsp", "US teaspoon")
us_fluid_dram = us_fluid_ounce.scaled(Fraction(1, 8), "fl dr", "US fluid dram")
us_minim = us_fluid_dram.scaled(Fraction(1, 60), "min", "US minim")
us_legal_cup = u.mL.scaled(
    240,
    "cup (legal)",
    "US legal cup",
    sources=(src.FDA_21CFR101,),
    note="Used for US nutrition labelling; 1.4% larger than the customary cup.",
)
fifth = us_gallon.scaled(
    Fraction(1, 5), "fifth", "fifth", note="757 mL; replaced by the 750 mL bottle in 1979."
)
jigger = us_fluid_ounce.scaled(
    Fraction(3, 2),
    "jigger",
    "jigger (shot)",
    sources=(src.ROWLETT,),
    uncertainty=conventional("jigger", 0.2, "1.5 US fl oz in the US; a shot is 1-2 fl oz by bar"),
)
pony = us_fluid_ounce.scaled(
    1,
    "pony",
    "pony",
    sources=(src.ROWLETT,),
    uncertainty=conventional("pony", None, "a small bar measure, usually 1 fl oz"),
)

# -- US dry (Winchester bushel, 1696) ------------------------------------------

bushel = cubic_inch.scaled(
    "2150.42",
    "bu",
    "US bushel (Winchester, struck)",
    sources=_STD,
    note="A cylinder 18.5 in in diameter and 8 in deep, per a 1696 Act of Parliament; "
    "exactly 35.239 070 166 88 L. 'Struck' means levelled off at the rim. For "
    "bushels of a particular crop by weight, see the bushel_of_* masses in .mass.",
)
peck = bushel.scaled(Fraction(1, 4), "pk", "US peck")
us_dry_gallon = bushel.scaled(Fraction(1, 8), "gal (dry)", "US dry gallon")
us_dry_quart = us_dry_gallon.scaled(Fraction(1, 4), "qt (dry)", "US dry quart")
us_dry_pint = us_dry_quart.scaled(Fraction(1, 2), "pt (dry)", "US dry pint")
heaped_bushel = cubic_inch.scaled(
    "2747.715",
    "bu (heaped)",
    "US heaped bushel",
    sources=(src.NIST_HB44,),
    note="≈ 1.278 struck bushels: the bushel measure piled into a cone, for apples and "
    "other produce sold by heaped measure.",
)
dry_barrel = cubic_inch.scaled(
    7056, "bbl (dry)", "US barrel for fruits, vegetables and dry goods", sources=(src.NIST_HB44,)
)
cranberry_barrel = cubic_inch.scaled(
    5826, "bbl (cranberry)", "US cranberry barrel", sources=(src.NIST_HB44,)
)

# -- British imperial (1824; 4.54609 L since 1985) -----------------------------

imperial_gallon = u.L.scaled("4.54609", "gal (imp)", "imperial gallon", sources=(src.UK_WMA_1985,))
imperial_quart = imperial_gallon.scaled(Fraction(1, 4), "qt (imp)", "imperial quart")
imperial_pint = imperial_quart.scaled(Fraction(1, 2), "pt (imp)", "imperial pint")
imperial_gill = imperial_pint.scaled(Fraction(1, 4), "gi (imp)", "imperial gill (noggin)")
imperial_fluid_ounce = imperial_gallon.scaled(
    Fraction(1, 160), "fl oz (imp)", "imperial fluid ounce"
)
imperial_fluid_drachm = imperial_fluid_ounce.scaled(
    Fraction(1, 8), "fl dr (imp)", "imperial fluid drachm"
)
imperial_minim = imperial_fluid_drachm.scaled(Fraction(1, 60), "min (imp)", "imperial minim")
imperial_peck = imperial_gallon.scaled(2, "pk (imp)", "imperial peck")
imperial_bushel = imperial_gallon.scaled(
    8,
    "bu (imp)",
    "imperial bushel",
    sources=(src.ROWLETT, src.CARDARELLI),
    note="8 imperial gallons = 36.368 72 L exactly, about 3.2% larger than the US bushel. "
    "No longer a legal UK unit of trade.",
)
strike = imperial_bushel.scaled(
    2,
    "strike",
    "strike",
    uncertainty=conventional("strike", None, "2 bushels in most places; 4 in some counties"),
)
coomb = imperial_bushel.scaled(4, "coomb", "coomb", sources=_CASK)
imperial_quarter = imperial_bushel.scaled(
    8, "qr (vol)", "quarter (imperial, of grain)", sources=_CASK
)
chaldron = imperial_bushel.scaled(
    36,
    "chaldron",
    "chaldron (London, of coal)",
    sources=_CASK,
    uncertainty=conventional(
        "chaldron", 0.3, "London coal chaldron of 36 bushels; the Newcastle chaldron was a weight"
    ),
)

# -- wine casks (English wine gallon = US gallon) ------------------------------

_WINE = conventional(
    "wine casks", None, "English wine-cask sizes in US (wine) gallons; sizes drifted over centuries"
)


def _wine(gallons: int | str | Fraction, symbol: str, name: str) -> Unit:
    return us_gallon.scaled(gallons, symbol, name, sources=_CASK, uncertainty=_WINE)


wine_rundlet = _wine(18, "rundlet", "rundlet (wine)")
wine_barrel = _wine("31.5", "bbl (wine)", "barrel (wine)")
tierce = _wine(42, "tierce", "tierce")
wine_hogshead = _wine(63, "hhd (wine)", "hogshead (wine)")
puncheon = _wine(84, "puncheon", "puncheon (tertian)")
wine_pipe = _wine(126, "pipe", "pipe (butt), wine")
tun = _wine(252, "tun", "tun")
us_liquid_barrel = us_gallon.scaled(
    "31.5", "bbl (liq)", "US barrel (liquid)", sources=(src.NIST_HB44,)
)
us_beer_barrel = us_gallon.scaled(
    31, "bbl (beer)", "US beer barrel", sources=(src.ROWLETT,), note="Federal excise-tax barrel."
)
oil_barrel = us_gallon.scaled(
    42,
    "bbl",
    "barrel (petroleum)",
    sources=(src.API_MPMS, src.NIST_SP811),
    note="42 US gallons ≈ 158.987 L. The unit of the oil trade.",
)

# -- beer and ale casks (imperial gallons) -------------------------------------

_BEER = conventional(
    "beer casks", None, "UK beer-cask sizes since 1824; earlier ale and beer casks differed"
)


def _beer(gallons: int | str | Fraction, symbol: str, name: str) -> Unit:
    return imperial_gallon.scaled(gallons, symbol, name, sources=_CASK, uncertainty=_BEER)


pin = _beer("4.5", "pin", "pin (beer)")
firkin = _beer(9, "firkin", "firkin (beer)")
kilderkin = _beer(18, "kilderkin", "kilderkin")
beer_barrel = _beer(36, "bbl (UK beer)", "barrel (UK beer)")
beer_hogshead = _beer(54, "hhd (beer)", "hogshead (beer)")
beer_butt = _beer(108, "butt", "butt (beer)")

# -- wine bottles (Champagne naming) -------------------------------------------

_BOTTLE = conventional(
    "large bottles",
    0.3,
    "Champagne sizes; Bordeaux uses 4.5 L for a jeroboam and different names above 6 L",
)
standard_bottle = u.mL.scaled(750, "bottle", "wine bottle (standard)", sources=(src.ROWLETT,))
piccolo = standard_bottle.scaled(Fraction(1, 4), "piccolo", "piccolo (split)")
demi = standard_bottle.scaled(Fraction(1, 2), "demi", "demi (half bottle)")
magnum = standard_bottle.scaled(2, "magnum", "magnum")


def _bottle(bottles: int, name: str) -> Unit:
    return standard_bottle.scaled(bottles, name, name, uncertainty=_BOTTLE)


jeroboam = _bottle(4, "jeroboam")
rehoboam = _bottle(6, "rehoboam")
methuselah = _bottle(8, "methuselah")
salmanazar = _bottle(12, "salmanazar")
balthazar = _bottle(16, "balthazar")
nebuchadnezzar = _bottle(20, "nebuchadnezzar")
solomon = _bottle(24, "solomon")
primat = _bottle(36, "primat")
melchizedek = _bottle(40, "melchizedek")

# -- kitchen -------------------------------------------------------------------

metric_cup = u.mL.scaled(250, "cup (metric)", "metric cup", sources=(src.ROWLETT,))
metric_tablespoon = u.mL.scaled(15, "tbsp (metric)", "metric tablespoon", sources=(src.ROWLETT,))
metric_teaspoon = u.mL.scaled(5, "tsp (metric)", "metric teaspoon", sources=(src.ROWLETT,))
australian_tablespoon = u.mL.scaled(
    20, "tbsp (AU)", "Australian tablespoon", sources=(src.ROWLETT,)
)
dessertspoon = us_teaspoon.scaled(
    2,
    "dstspn",
    "dessertspoon",
    sources=(src.ROWLETT,),
    uncertainty=conventional("dessertspoon", 0.05, "2 teaspoons; 10 mL in UK and Australian use"),
)
coffeespoon = us_teaspoon.scaled(
    Fraction(1, 2),
    "coffeespoon",
    "coffeespoon",
    sources=(src.ROWLETT,),
    uncertainty=nominal("coffeespoon", "half a teaspoon by convention"),
)
dash = us_teaspoon.scaled(
    Fraction(1, 8),
    "dash",
    "dash",
    sources=(src.ROWLETT,),
    uncertainty=nominal("dash", "1/8 tsp per measuring-spoon sets; some sets mark it 1/16"),
)
pinch = us_teaspoon.scaled(
    Fraction(1, 16),
    "pinch",
    "pinch",
    sources=(src.ROWLETT,),
    uncertainty=nominal("pinch", "what fits between finger and thumb; spoon sets mark 1/16 tsp"),
)
smidgen = us_teaspoon.scaled(
    Fraction(1, 32),
    "smidgen",
    "smidgen",
    sources=(src.ROWLETT,),
    uncertainty=nominal("smidgen", "1/32 tsp per measuring-spoon sets"),
)
drop = u.mL.scaled(
    Fraction(1, 20),
    "gtt",
    "drop (medical)",
    sources=(src.ROWLETT,),
    uncertainty=nominal("drop", "depends on dropper and liquid; 0.05 mL is the metric convention"),
)

# -- timber, earthworks and shipping -------------------------------------------

board_foot = cubic_inch.scaled(144, "FBM", "board foot", sources=_STD)
cord = cubic_foot.scaled(128, "cd (wood)", "cord (of firewood)", sources=_STD)
face_cord = cord.scaled(
    Fraction(1, 3),
    "face cord",
    "face cord (rick)",
    sources=(src.ROWLETT,),
    uncertainty=nominal("face cord", "a 4 × 8 ft stack of logs of whatever length was cut"),
)
acre_foot = (L.furlong * L.chain * u.ft).named(
    "ac·ft", "acre-foot", sources=_STD, note="43 560 ft³ ≈ 1233.48 m³ (international foot)."
)
register_ton = cubic_foot.scaled(
    100,
    "RT",
    "register ton",
    sources=(src.ROWLETT,),
    note="Ship capacity, not mass. Replaced by the dimensionless GT index in 1982.",
)
freight_ton = cubic_foot.scaled(
    40,
    "FT",
    "freight (measurement) ton",
    sources=(src.ROWLETT,),
    uncertainty=conventional("freight ton", None, "40 ft³ in US practice; 1 m³ in metric shipping"),
)
olympic_pool = (u.m**3).scaled(
    2500,
    "Olympic pool",
    "Olympic swimming pool",
    sources=(src.ROWLETT,),
    uncertainty=nominal("Olympic pool", "50 × 25 m × 2 m minimum depth; deeper pools hold more"),
)

# -- volume flow ---------------------------------------------------------------

sverdrup = (u.m**3 / u.s).scaled(
    10**6, "Sv (flow)", "sverdrup", sources=(src.ROWLETT,), note="Ocean currents."
)
cusec = (cubic_foot / u.s).named("cusec", "cubic foot per second")
cumec = (u.m**3 / u.s).named("cumec", "cubic metre per second")
