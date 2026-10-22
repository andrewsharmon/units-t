"""Traditional units of particular countries, as later fixed in metric or English terms.

Most traditional systems were eventually tied to the metre or the English inch by
statute: Japan by the 1891 Weights and Measures Act, Russia by the 1835 ukase,
Hong Kong by ordinance, and the PRC "market" units in 1984. Under those definitions
the units are exact, even though the older units they replaced varied. Where no
definition was ever fixed (Scotland, the Indian maund, the Castilian vara) the units
are flagged CONVENTIONAL.
"""

from __future__ import annotations

from fractions import Fraction

from units_t import sources as src
from units_t import units as u
from units_t.provenance import conventional

# -- Japan (shakkanhō, fixed 1891) ---------------------------------------------

_JP = (src.JAPAN_WMA_1891, src.CARDARELLI)

shaku = u.m.scaled(Fraction(10, 33), "shaku", "shaku (尺)", sources=_JP)
sun = shaku.scaled(Fraction(1, 10), "sun", "sun (寸)")
bu_jp = sun.scaled(Fraction(1, 10), "bu", "bu (分, length)")
ken = shaku.scaled(6, "ken", "ken (間)")
jo = shaku.scaled(10, "jō", "jō (丈)")
cho_length = ken.scaled(60, "chō", "chō (町, length)")
ri_jp = cho_length.scaled(36, "ri", "ri (里, Japanese)", note="≈ 3.927 km.")
tsubo = (ken**2).named("tsubo", "tsubo (坪)", note="The area of two tatami mats; ≈ 3.306 m².")
se = tsubo.scaled(30, "se", "se (畝)")
tan = se.scaled(10, "tan", "tan (反)")
cho_area = tan.scaled(10, "chō (area)", "chō (町, area)")
sho = u.L.scaled(Fraction(2401, 1331), "shō", "shō (升)", sources=_JP, note="64.827 cubic sun.")
go = sho.scaled(Fraction(1, 10), "gō", "gō (合)", note="The rice-cooker cup, ≈ 180 mL.")
to = sho.scaled(10, "to", "to (斗)")
koku = sho.scaled(100, "koku", "koku (石)", note="Rice to feed one person for a year.")
kan = u.kg.scaled(Fraction(15, 4), "kan", "kan (貫)", sources=_JP)
momme = kan.scaled(Fraction(1, 1000), "momme", "momme (匁)", note="Still used for pearls and silk.")
kin_jp = momme.scaled(160, "kin", "kin (斤, Japanese)")

# -- China (shìzhì market units, 1984) -----------------------------------------

_CN = (src.CHINA_1984, src.CARDARELLI)

chi = u.m.scaled(Fraction(1, 3), "chǐ", "chǐ (市尺)", sources=_CN)
cun = chi.scaled(Fraction(1, 10), "cùn", "cùn (市寸)")
fen = cun.scaled(Fraction(1, 10), "fēn", "fēn (市分, length)")
zhang = chi.scaled(10, "zhàng", "zhàng (市丈)")
li_cn = chi.scaled(1500, "lǐ", "lǐ (市里)", note="Exactly 500 m.")
mu = (u.m**2).scaled(Fraction(10_000, 15), "mǔ", "mǔ (市亩)", sources=_CN)
qing = mu.scaled(100, "qǐng", "qǐng (市顷)")
jin = u.g.scaled(500, "jīn", "jīn (市斤)", sources=_CN)
liang = jin.scaled(Fraction(1, 10), "liǎng", "liǎng (市两)", note="1/16 jīn before 1959.")
qian = liang.scaled(Fraction(1, 10), "qián", "qián (市钱)")
dan_mass = jin.scaled(100, "dàn", "dàn (市担)")
sheng = u.L.named("shēng", "shēng (市升)", sources=_CN)
dou = sheng.scaled(10, "dǒu", "dǒu (市斗)")

# -- Hong Kong -----------------------------------------------------------------

_HK = (src.HONG_KONG_CAP68,)

chek = u.m.scaled("0.371475", "chek", "chek (Hong Kong foot)", sources=_HK, note="14⅝ in exactly.")
tsun = chek.scaled(Fraction(1, 10), "tsun", "tsun (Hong Kong inch)")
catty = u.kg.scaled(
    "0.60478982",
    "catty",
    "catty (Hong Kong)",
    sources=_HK,
    note="≈ 1⅓ lb, but defined in kilograms (the two differ by 1 part in 10⁸).",
)
tael = catty.scaled(
    Fraction(1, 16), "tael", "tael (Hong Kong)", note="Gold is still traded in taels."
)
picul = catty.scaled(100, "picul", "picul (Hong Kong)")

# -- Russia (fixed to English feet, 1835) --------------------------------------

_RU = (src.RUSSIA_1835, src.CARDARELLI)

vershok = u.inch.scaled(Fraction(7, 4), "vershok", "vershok", sources=_RU)
arshin = u.inch.scaled(28, "arshin", "arshin", sources=_RU)
sazhen = u.ft.scaled(7, "sazhen", "sazhen", sources=_RU)
verst = sazhen.scaled(500, "verst", "verst", note="≈ 1.0668 km.")
russian_mile = verst.scaled(7, "milya", "Russian mile")
desyatina = (sazhen**2).scaled(2400, "desyatina", "desyatina", sources=_RU)
funt = u.kg.scaled("0.40951241", "funt", "funt (Russian pound)", sources=_RU)
pood = funt.scaled(40, "pood", "pood", note="Still used for kettlebells (16.38 kg).")
zolotnik = funt.scaled(Fraction(1, 96), "zolotnik", "zolotnik")
dolya = zolotnik.scaled(Fraction(1, 96), "dolya", "dolya")
vedro = u.L.scaled(
    "12.29941",
    "vedro",
    "vedro (bucket)",
    sources=(src.CARDARELLI,),
    uncertainty=conventional("vedro", 1e-4, "defined via 30 funt of water at 13⅓ °Ré"),
)

# -- France before the metre (Paris standards, fixed 1799) ---------------------

_FR = (src.FRANCE_1799, src.CARDARELLI)

ligne = u.m.scaled(Fraction(1) / Fraction("443.296"), "ligne", "ligne (Paris line)", sources=_FR)
pouce = ligne.scaled(12, "pouce", "pouce (Paris inch)")
pied_du_roi = pouce.scaled(12, "pied", "pied du roi (Paris foot)", note="≈ 324.84 mm.")
toise = pied_du_roi.scaled(6, "toise", "toise (de Paris)")
lieue = toise.scaled(
    2000,
    "lieue",
    "lieue de Paris (1674)",
    uncertainty=conventional(
        "lieue", 0.3, "2000 toises; the lieue de poste, lieue commune and others ran 3.9-5.6 km"
    ),
)
livre = u.kg.scaled(
    Fraction(9216) / Fraction("18827.15"),
    "livre",
    "livre (poids de marc)",
    sources=_FR,
    note="9216 grains of the 1799 standard; ≈ 489.506 g.",
)
pied_usuel = u.m.scaled(
    Fraction(1, 3), "pied (usuel)", "pied usuel (1812-1840)", sources=(src.CARDARELLI,)
)
toise_usuelle = pied_usuel.scaled(6, "toise (usuelle)", "toise usuelle (1812-1840)")
livre_usuelle = u.g.scaled(
    500, "livre (usuelle)", "livre usuelle (1812-1840)", sources=(src.CARDARELLI,)
)

# -- Prussia (from Paris lines, 1816) ------------------------------------------

rhineland_foot = ligne.scaled(
    "139.13",
    "Fuß (rh)",
    "Rhineland (Prussian) foot",
    sources=(src.CARDARELLI,),
    note="≈ 313.85 mm.",
)
prussian_rute = rhineland_foot.scaled(12, "Rute", "Rute (Prussian rod)")
prussian_mile = prussian_rute.scaled(2000, "Meile (pr)", "Prussian mile", note="≈ 7.5325 km.")

# -- Spain and the Americas ----------------------------------------------------

castilian_vara = u.m.scaled(
    "0.835905",
    "vara",
    "vara (Castilian, de Burgos)",
    sources=(src.CARDARELLI, src.ROWLETT),
    uncertainty=conventional("vara", 0.03, "vara de Burgos; local varas ran 0.768-0.912 m"),
)
texas_vara = u.inch.scaled(
    Fraction(100, 3),
    "vara (TX)",
    "Texas vara",
    sources=(src.ROWLETT,),
    note="33⅓ in exactly, by Texas statute (1919). Still found in Texas land titles.",
)

# -- Scotland (never fixed by statute in metric or English terms) --------------

_SCOTS = conventional(
    "Scots measure", 0.002, "Scots ell taken as 37 in; surviving standards give 37.0-37.2 in"
)
scots_ell = u.inch.scaled(
    37, "ell (Sc)", "Scots ell", sources=(src.ZUPKO_1968,), uncertainty=_SCOTS
)
scots_fall = scots_ell.scaled(6, "fall (Sc)", "Scots fall")
scots_mile = scots_fall.scaled(320, "mi (Sc)", "Scots mile", note="≈ 1.80 km.")
scots_pint = u.L.scaled(
    "1.696",
    "pt (Sc)",
    "Scots pint (joug)",
    sources=(src.ZUPKO_1968, src.CARDARELLI),
    uncertainty=conventional("Scots pint", 0.01, "Stirling jug standard; ~3 imperial pints"),
)

# -- Ireland (Irish measure, abolished 1826) -----------------------------------

irish_perch = u.yd.scaled(7, "perch (Ir)", "Irish perch", sources=(src.ROWLETT,))
irish_furlong = irish_perch.scaled(
    40, "fur (Ir)", "Irish furlong", note="280 yd, vs 220 yd English."
)
irish_mile = irish_furlong.scaled(8, "mi (Ir)", "Irish mile", note="2240 yd ≈ 2.048 km.")

# -- South Asia ----------------------------------------------------------------

_SA = (src.CARDARELLI, src.ROWLETT)

tola = u.lb.scaled(Fraction(180, 7000), "tola", "tola", sources=_SA, note="180 grains ≈ 11.66 g.")
seer = tola.scaled(
    80,
    "seer",
    "seer (Indian standard)",
    uncertainty=conventional("seer", 0.5, "80 tola in British India; local seers varied ~2x"),
)
maund = seer.scaled(40, "maund", "maund (Indian standard)", note="≈ 37.32 kg (82 2/7 lb).")

# -- Thailand (fixed to metric, 1923) ------------------------------------------

wa = u.m.scaled(2, "wa", "wa (วา)", sources=(src.CARDARELLI,))
sok = wa.scaled(Fraction(1, 4), "sok", "sok (ศอก)")
rai = (u.m**2).scaled(1600, "rai", "rai (ไร่)", sources=(src.CARDARELLI,))
baht_mass = u.g.scaled(
    15,
    "baht",
    "baht (บาท, mass)",
    sources=(src.CARDARELLI,),
    note="Gold is sold by a different baht: 15.244 g for jewellery, 15.16 g for bullion.",
)
