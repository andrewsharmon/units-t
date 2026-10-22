"""Citations for the definitions and values used in the unit catalogue.

Each :class:`~units_t.provenance.Source` is attached to the units whose definitions it
supports. Statutes and standards bodies are preferred. Secondary references (Rowlett,
Cardarelli, Zupko) are used for historical, regional and informal units that no
standard defines.
"""

from units_t.provenance import Source

# -- metrology standards ------------------------------------------------------

SI_BROCHURE = Source(
    "BIPM-SI-2019",
    "BIPM, The International System of Units (SI Brochure), 9th ed., 2019 (v3.01, 2024)",
    "https://www.bipm.org/en/publications/si-brochure",
)
NIST_SP811 = Source(
    "NIST-SP811",
    "A. Thompson & B. N. Taylor, Guide for the Use of the International System of Units "
    "(SI), NIST Special Publication 811, 2008 ed., Appendix B",
    "https://www.nist.gov/pml/special-publication-811",
)
NIST_HB44 = Source(
    "NIST-HB44",
    "NIST Handbook 44, Specifications, Tolerances, and Other Technical Requirements for "
    "Weighing and Measuring Devices, Appendix C: General Tables of Units of Measurement",
    "https://www.nist.gov/pml/owm/nist-handbook-44-current-edition",
)
CODATA_2022 = Source(
    "CODATA-2022",
    "P. J. Mohr, E. Tiesinga, D. B. Newell & B. N. Taylor, CODATA Recommended Values of "
    "the Fundamental Physical Constants: 2022, Rev. Mod. Phys. 97, 025002 (2025)",
    "https://physics.nist.gov/cuu/Constants/",
)
ISO_80000 = Source(
    "ISO-80000",
    "ISO/IEC 80000, Quantities and units (parts 1-13), 2019-2022; binary prefixes in "
    "IEC 80000-13:2008",
)

# -- treaties and statutes ----------------------------------------------------

YARD_POUND_1959 = Source(
    "Yard-Pound-1959",
    "Refinement of Values for the Yard and the Pound, Federal Register 24 FR 5348 "
    "(1 July 1959): the international yard (0.9144 m) and pound (0.45359237 kg)",
)
US_SURVEY_FOOT_2020 = Source(
    "US-Survey-Foot-2020",
    "Deprecation of the United States (U.S.) Survey Foot, Federal Register 85 FR 62698 "
    "(5 October 2020), effective 1 January 2023",
)
UK_WMA_1985 = Source(
    "UK-WMA-1985",
    "Weights and Measures Act 1985 (UK), Schedule 1: Definitions of units of measurement",
    "https://www.legislation.gov.uk/ukpga/1985/72/schedule/1",
)
JAPAN_WMA_1891 = Source(
    "Japan-WMA-1891",
    "Weights and Measures Act of Japan (度量衡法, Meiji 24 / 1891): 1 shaku = 10/33 m, "
    "1 kan = 15/4 kg",
)
CHINA_1984 = Source(
    "China-1984",
    "State Council of the PRC, Order on the Unified Implementation of Legal Units of "
    "Measurement (1984): market units 市制 (shì jīn = 500 g, shì chǐ = 1/3 m, mǔ = 1/15 ha)",
)
RUSSIA_1835 = Source(
    "Russia-1835",
    "Ukase of Nicholas I on the system of Russian measures (1835), sazhen = 7 English feet; "
    "funt fixed at 409.51241 g by the Regulations on Weights and Measures (1899)",
)
FDA_21CFR101 = Source(
    "21-CFR-101.9",
    "US Code of Federal Regulations, 21 CFR 101.9(b)(5)(viii): for nutrition labelling, "
    "1 cup = 240 mL and 1 fl oz = 30 mL",
)
HONG_KONG_CAP68 = Source(
    "HK-Cap68",
    "Weights and Measures Ordinance (Hong Kong, Cap. 68), Schedule 1: 1 chek = 0.371475 m, "
    "1 catty = 0.60478982 kg",
)
FRANCE_1799 = Source(
    "France-1799",
    "Loi du 19 frimaire an VIII (10 December 1799): the definitive metre is 3 pieds "
    "11.296 lignes, and the kilogram 18 827.15 grains, of the old Paris standards",
)
EIA_310 = Source(
    "EIA-310",
    "EIA/ECA-310-E, Cabinets, Racks, Panels, and Associated Equipment (2005): 1 U = 1.75 in",
)

# -- astronomy ----------------------------------------------------------------

IAU_2012_B2 = Source(
    "IAU-2012-B2",
    "IAU 2012 Resolution B2: re-definition of the astronomical unit of length "
    "(149 597 870 700 m exactly)",
    "https://www.iau.org/static/resolutions/IAU2012_English.pdf",
)
IAU_2015_B2 = Source(
    "IAU-2015-B2",
    "IAU 2015 Resolution B2: the parsec is defined as exactly 648000/π au",
    "https://www.iau.org/static/resolutions/IAU2015_English.pdf",
)
IAU_2015_B3 = Source(
    "IAU-2015-B3",
    "IAU 2015 Resolution B3: recommended nominal conversion constants for selected solar "
    "and planetary properties",
    "https://www.iau.org/static/resolutions/IAU2015_English.pdf",
)
IERS_CONVENTIONS = Source(
    "IERS-2010",
    "G. Petit & B. Luzum (eds.), IERS Conventions (2010), IERS Technical Note 36",
)
ASTRONOMICAL_ALMANAC = Source(
    "Astronomical-Almanac",
    "U.S. Naval Observatory & HM Nautical Almanac Office, The Astronomical Almanac, "
    "Section K (mean lengths of years and months, epoch J2000.0)",
)

# -- agriculture and trade ----------------------------------------------------

USDA_AH697 = Source(
    "USDA-AH697",
    "USDA Economic Research Service, Weights, Measures, and Conversion Factors for "
    "Agricultural Commodities and Their Products, Agricultural Handbook No. 697 (1992)",
)
API_MPMS = Source(
    "API-MPMS",
    "American Petroleum Institute, Manual of Petroleum Measurement Standards, Ch. 1 "
    "(barrel = 42 US gallons)",
)

# -- typography ---------------------------------------------------------------

POSTSCRIPT_REF = Source(
    "Adobe-PostScript-3",
    "Adobe Systems, PostScript Language Reference, 3rd ed. (1999): 1 unit = 1/72 inch",
)
TEXBOOK = Source(
    "Knuth-TeXbook",
    "D. E. Knuth, The TeXbook (Addison-Wesley, 1984), ch. 10: 72.27 pt = 1 in",
)

# -- secondary references -----------------------------------------------------

ROWLETT = Source(
    "Rowlett",
    "R. Rowlett, How Many? A Dictionary of Units of Measurement, University of North "
    "Carolina at Chapel Hill (2001-2018)",
    "https://www.ibiblio.org/units/",
)
CARDARELLI = Source(
    "Cardarelli-2003",
    "F. Cardarelli, Encyclopaedia of Scientific Units, Weights and Measures: Their SI "
    "Equivalences and Origins (Springer, 2003)",
)
ZUPKO_1968 = Source(
    "Zupko-1968",
    "R. E. Zupko, A Dictionary of English Weights and Measures from Anglo-Saxon Times to "
    "the Nineteenth Century (University of Wisconsin Press, 1968)",
)
CLAGETT_1999 = Source(
    "Clagett-1999",
    "M. Clagett, Ancient Egyptian Science, Vol. III: Ancient Egyptian Mathematics "
    "(American Philosophical Society, 1999)",
)
POWELL_1992 = Source(
    "Powell-1992",
    "M. A. Powell, 'Weights and Measures', in The Anchor Bible Dictionary, vol. 6 "
    "(Doubleday, 1992)",
)
HULTSCH_1882 = Source(
    "Hultsch-1882",
    "F. Hultsch, Griechische und römische Metrologie, 2nd ed. (Weidmann, Berlin, 1882)",
)
ENGELS_1985 = Source(
    "Engels-1985",
    "D. Engels, 'The Length of Eratosthenes' Stade', American Journal of Philology "
    "106(3), 298-311 (1985)",
)
THOM_1967 = Source(
    "Thom-1967",
    "A. Thom, Megalithic Sites in Britain (Oxford University Press, 1967)",
)
MIT_SMOOT = Source(
    "MIT-Smoot",
    "MIT Museum / Lambda Chi Alpha, the Harvard Bridge smoot markings (1958)",
)
