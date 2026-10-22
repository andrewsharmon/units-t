"""Ancient and prehistoric units, reconstructed from archaeology and texts.

None of these has an exact modern value. Each system hangs from one *base estimate*
(the Roman foot, the Egyptian royal cubit, the biblical bath …) with its own
:attr:`~units_t.provenance.Certainty.ESTIMATED` term. Everything else in the system is
an exact multiple of that base, as the ancient sources define it. So the uncertainty is
correlated correctly. Twelve Roman unciae are *exactly* one Roman foot, while a Roman
amphora (one cubic foot) carries three times the Roman foot's relative uncertainty.

The relative figures are rough spreads of scholarly estimates or of surviving
artefacts, not statistical standard uncertainties.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import estimated

# -- Rome ----------------------------------------------------------------------

_ROMAN = (src.HULTSCH_1882, src.CARDARELLI)

pes = u.m.scaled(
    "0.296",
    "pes",
    "Roman foot (pes)",
    sources=_ROMAN,
    uncertainty=estimated(
        "Roman foot", 0.004, "from surviving rulers and buildings: 0.294-0.297 m"
    ),
)
digitus = pes.scaled(Fraction(1, 16), "digitus", "Roman digit (digitus)")
roman_uncia = pes.scaled(Fraction(1, 12), "uncia (len)", "Roman inch (uncia)")
palmus = pes.scaled(Fraction(1, 4), "palmus", "Roman palm (palmus)")
cubitus = pes.scaled(Fraction(3, 2), "cubitus", "Roman cubit (cubitus)")
gradus = pes.scaled(Fraction(5, 2), "gradus", "Roman step (gradus)")
passus = pes.scaled(5, "passus", "Roman pace (passus)", note="A double step.")
actus = pes.scaled(120, "actus", "actus")
roman_stadium = pes.scaled(625, "stadium", "Roman stadium", note="1/8 Roman mile; cf. the furlong.")
roman_mile = passus.scaled(1000, "m.p.", "Roman mile (mille passus)", note="≈ 1.48 km.")
leuga = pes.scaled(7500, "leuga", "Gallic league (leuga)")
jugerum = (actus**2).scaled(2, "jugerum", "jugerum", note="Two square actus, ≈ 0.25 ha.")
amphora = (pes**3).named(
    "amphora", "Roman amphora (quadrantal)", note="One cubic Roman foot, ≈ 25.9 L."
)
modius = amphora.scaled(Fraction(1, 3), "modius", "modius")
congius = amphora.scaled(Fraction(1, 8), "congius", "congius")
sextarius = amphora.scaled(Fraction(1, 48), "sextarius", "sextarius")
hemina = sextarius.scaled(Fraction(1, 2), "hemina", "hemina")
libra = u.g.scaled(
    "327.45",
    "libra",
    "Roman pound (libra)",
    sources=_ROMAN,
    uncertainty=estimated("Roman pound", 0.01, "from coin and weight hoards: 322-329 g"),
)
roman_uncia_mass = libra.scaled(Fraction(1, 12), "uncia", "Roman ounce (uncia)")
scrupulum = roman_uncia_mass.scaled(Fraction(1, 24), "scrupulum", "scrupulum")
siliqua = scrupulum.scaled(Fraction(1, 6), "siliqua", "siliqua", note="A carob seed.")

# -- Greece --------------------------------------------------------------------

_GREEK = (src.HULTSCH_1882, src.ENGELS_1985, src.CARDARELLI)

attic_foot = u.m.scaled(
    "0.308",
    "pous",
    "Attic foot (pous)",
    sources=_GREEK,
    uncertainty=estimated("Attic foot", 0.02, "0.296-0.315 m depending on the building measured"),
)
plethron = attic_foot.scaled(100, "plethron", "plethron")
attic_stadion = attic_foot.scaled(600, "stadion", "stadion (Attic)", note="600 Attic feet.")
stadion = u.m.scaled(
    "184.8",
    "stade",
    "stade (as used by Eratosthenes, per Engels)",
    sources=_GREEK,
    uncertainty=estimated(
        "stade",
        0.15,
        "the stade varied by city and era from ~157 m to ~209 m; Engels (1985) argues 184.8 m",
    ),
    note="The reason estimates of Eratosthenes' Earth circumference are so contested.",
)
olympic_stadion = u.m.scaled(
    "192.27",
    "stadion (Ol)",
    "Olympic stadion (track at Olympia)",
    sources=(src.CARDARELLI,),
    uncertainty=estimated("Olympic stadion", 0.001, "length of the excavated track at Olympia"),
)
attic_talent = u.kg.scaled(
    "26.0",
    "talent (Att)",
    "Attic talent",
    sources=_GREEK,
    uncertainty=estimated(
        "Attic talent", 0.05, "≈ 25.8-26.2 kg from surviving weights and coinage"
    ),
)
attic_mina = attic_talent.scaled(Fraction(1, 60), "mina (Att)", "Attic mina")
drachma = attic_mina.scaled(Fraction(1, 100), "drachma", "Attic drachma (weight)")
obol = drachma.scaled(Fraction(1, 6), "obol", "obol")

# -- Egypt ---------------------------------------------------------------------

_EGYPT = (src.CLAGETT_1999, src.CARDARELLI)

royal_cubit = u.m.scaled(
    "0.5236",
    "meh nsw",
    "Egyptian royal cubit",
    sources=_EGYPT,
    uncertainty=estimated("royal cubit", 0.005, "surviving cubit rods measure 523-529 mm"),
)
egyptian_palm = royal_cubit.scaled(Fraction(1, 7), "shesep", "Egyptian palm (shesep)")
egyptian_digit = egyptian_palm.scaled(Fraction(1, 4), "djeba", "Egyptian digit (djeba)")
khet = royal_cubit.scaled(100, "khet", "khet (rod)")
iteru = royal_cubit.scaled(20_000, "iteru", "iteru (river measure)", note="≈ 10.5 km.")
setat = (khet**2).named("setat", "setat (aroura)", note="One square khet, ≈ 0.27 ha.")
hekat = (royal_cubit**3).scaled(
    Fraction(1, 30), "hekat", "hekat", note="1/30 cubic royal cubit, ≈ 4.8 L."
)
ro = hekat.scaled(Fraction(1, 320), "ro", "ro")
khar = hekat.scaled(20, "khar", "khar (sack)")
deben = u.g.scaled(
    91,
    "deben",
    "deben (New Kingdom)",
    sources=_EGYPT,
    uncertainty=estimated(
        "deben", 0.05, "New Kingdom value; Old Kingdom debens of 13.6 g (gold) also existed"
    ),
)
kite = deben.scaled(Fraction(1, 10), "kite", "kite (qedet)")

# -- Mesopotamia ---------------------------------------------------------------

_MESO = (src.POWELL_1992, src.CARDARELLI)

kush = u.m.scaled(
    "0.497",
    "kùš",
    "Babylonian cubit (kùš)",
    sources=_MESO,
    uncertainty=estimated("Babylonian cubit", 0.02, "≈ 0.49-0.51 m"),
)
mana = u.g.scaled(
    500,
    "ma-na",
    "Babylonian mina (ma-na)",
    sources=_MESO,
    uncertainty=estimated("Babylonian mina", 0.05, "≈ 480-505 g from duck and lion weights"),
)
gin = mana.scaled(Fraction(1, 60), "gín", "Babylonian shekel (gín)")
she = gin.scaled(Fraction(1, 180), "še", "še (barleycorn grain)")
gu = mana.scaled(60, "gú", "Babylonian talent (gú)")

# -- Ancient Israel (biblical) -------------------------------------------------

_BIBLE = (src.POWELL_1992,)

biblical_cubit = u.m.scaled(
    "0.445",
    "ammah",
    "biblical (common) cubit",
    sources=_BIBLE,
    uncertainty=estimated(
        "biblical cubit", 0.05, "common cubit ≈ 44.5 cm; the 'long' cubit ≈ 52 cm"
    ),
)
biblical_span = biblical_cubit.scaled(Fraction(1, 2), "zeret", "span (zeret)")
handbreadth = biblical_cubit.scaled(Fraction(1, 6), "tefah", "handbreadth (tefah)")
fingerbreadth = biblical_cubit.scaled(Fraction(1, 24), "etzba", "fingerbreadth (etzba)")
sabbath_days_journey = biblical_cubit.scaled(2000, "techum", "Sabbath day's journey")
shekel = u.g.scaled(
    "11.4",
    "shekel",
    "shekel (weight)",
    sources=_BIBLE,
    uncertainty=estimated(
        "shekel", 0.1, "Judean inscribed weights give 11.3-11.5 g; others 8-13 g"
    ),
)
gerah = shekel.scaled(Fraction(1, 20), "gerah", "gerah")
biblical_mina = shekel.scaled(50, "maneh", "biblical mina (maneh)")
biblical_talent = shekel.scaled(3000, "kikkar", "biblical talent (kikkar)")
bath = u.L.scaled(
    22,
    "bath",
    "bath",
    sources=_BIBLE,
    uncertainty=estimated(
        "bath", 0.3, "estimates range ~21-45 L; inscribed jars from Lachish suggest ~22 L"
    ),
)
ephah = bath.named("ephah", "ephah", note="The dry measure equal to the bath.")
homer = bath.scaled(10, "homer", "homer (kor)")
seah = ephah.scaled(Fraction(1, 3), "seah", "seah")
omer = ephah.scaled(Fraction(1, 10), "omer", "omer")
hin = bath.scaled(Fraction(1, 6), "hin", "hin")
cab = ephah.scaled(Fraction(1, 18), "cab", "cab (kab)")
log = bath.scaled(Fraction(1, 72), "log", "log")

# -- Neolithic Britain ---------------------------------------------------------

megalithic_yard = u.ft.scaled(
    "2.72",
    "MY",
    "megalithic yard",
    sources=(src.THOM_1967,),
    uncertainty=estimated(
        "megalithic yard",
        None,
        "Thom claimed 2.72 ± 0.003 ft from stone-circle surveys; later statistical work "
        "doubts that any such unit existed",
    ),
    note="Hypothetical. Included because it is the textbook example of a disputed unit.",
)
megalithic_rod = megalithic_yard.scaled(Fraction(5, 2), "MR", "megalithic rod")
