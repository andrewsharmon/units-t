from fractions import Fraction

import pytest

from units_t import Certainty, DimensionError, Unit
from units_t import catalog as uc
from units_t import units as u

# -- catalogue-wide invariants --------------------------------------------------


@pytest.mark.parametrize("key", sorted(uc.ALL))
def test_every_unit_has_name_and_source(key: str) -> None:
    unit = uc.ALL[key]
    assert unit.name, f"{key} has no long name"
    assert unit.sources, f"{key} cites no source"


@pytest.mark.parametrize("key", sorted(uc.inexact()))
def test_inexact_units_explain_themselves(key: str) -> None:
    for term, exponent in uc.ALL[key].uncertainty_terms:
        assert term.description
        assert exponent != 0
        assert term.relative is None or term.relative > 0


def test_catalogue_is_large_and_varied() -> None:
    assert len(uc.ALL) > 600
    for certainty in Certainty:
        assert uc.with_certainty(certainty), f"no {certainty.name} units"


def test_lookup_helpers() -> None:
    assert uc.get("furlong") is uc.furlong
    assert "heaped_bushel" in uc.search("bushel")
    with pytest.raises(KeyError):
        uc.get("not_a_unit")
    with pytest.raises(AttributeError):
        uc.__getattr__("not_a_unit")


def test_core_units_are_included() -> None:
    assert uc.m is u.m
    assert uc.mi is u.mi


# -- furlongs ----------------------------------------------------------------------


def test_furlong() -> None:
    assert uc.furlong.conversion_factor(u.m) == Fraction("201.168")
    assert uc.furlong.conversion_factor(u.yd) == 220
    assert uc.furlong.conversion_factor(uc.chain) == 10
    assert uc.furlong.conversion_factor(uc.rod) == 40
    assert u.mi.conversion_factor(uc.furlong) == 8
    assert uc.furlong.is_exact


def test_survey_furlong_differs_by_two_ppm() -> None:
    ratio = uc.survey_furlong.conversion_factor(uc.furlong)
    assert ratio == Fraction(1200, 3937) / Fraction("0.3048")
    assert float(ratio) == pytest.approx(1 + 2e-6, rel=1e-9)
    assert uc.survey_mile.conversion_factor(uc.survey_furlong) == 8


def test_irish_and_roman_furlongs() -> None:
    assert uc.irish_furlong.conversion_factor(u.yd) == 280
    assert uc.roman_mile.conversion_factor(uc.roman_stadium) == 8
    assert uc.roman_stadium.certainty is Certainty.ESTIMATED


def test_furlong_per_fortnight() -> None:
    speed = (1 * uc.furlong_per_fortnight).to(u.m / u.s)
    assert speed.value == Fraction("201.168") / (14 * 86400)


# -- bushels -------------------------------------------------------------------------


def test_us_bushel_is_winchester() -> None:
    assert uc.bushel.conversion_factor(uc.cubic_inch) == Fraction("2150.42")
    assert uc.bushel.conversion_factor(u.L) == Fraction("35.23907016688")
    assert uc.bushel.conversion_factor(uc.peck) == 4
    assert uc.bushel.conversion_factor(uc.us_dry_gallon) == 8
    assert uc.bushel.conversion_factor(uc.us_dry_pint) == 64


def test_imperial_bushel() -> None:
    assert uc.imperial_bushel.conversion_factor(u.L) == Fraction("36.36872")
    assert uc.imperial_quarter.conversion_factor(uc.imperial_bushel) == 8
    assert uc.chaldron.certainty is Certainty.CONVENTIONAL


def test_heaped_bushel() -> None:
    assert float(uc.heaped_bushel.conversion_factor(uc.bushel)) == pytest.approx(1.278, abs=5e-4)


def test_bushels_by_weight_are_masses_and_conventional() -> None:
    assert uc.bushel_of_wheat.conversion_factor(u.lb) == 60
    assert uc.bushel_of_wheat.conversion_factor(u.kg) == Fraction("27.2155422")
    assert uc.bushel_of_corn.conversion_factor(u.lb) == 56
    assert uc.bushel_of_oats.conversion_factor(u.lb) == 32
    assert uc.bushel_of_wheat.certainty is Certainty.CONVENTIONAL
    # Different crops share one convention, so their ratio is exact.
    assert uc.bushel_of_wheat.conversion(uc.bushel_of_oats).is_exact
    with pytest.raises(DimensionError):
        uc.bushel_of_wheat.conversion_factor(uc.bushel)


# -- other exact definitions ------------------------------------------------------------


@pytest.mark.parametrize(
    ("unit", "target", "factor"),
    [
        (uc.nautical_mile, u.m, Fraction(1852)),
        (uc.us_gallon, u.L, Fraction("3.785411784")),
        (uc.imperial_gallon, uc.imperial_fluid_ounce, Fraction(160)),
        (uc.oil_barrel, uc.us_gallon, Fraction(42)),
        (uc.grain, u.mg, Fraction("64.79891")),
        (uc.troy_ounce, u.g, Fraction("31.1034768")),
        (uc.stone, u.lb, Fraction(14)),
        (uc.carat, u.mg, Fraction(200)),
        (uc.pound_force, u.N, Fraction("4.4482216152605")),
        (uc.torr, u.Pa, Fraction(101325, 760)),
        (uc.millimetre_of_mercury, u.Pa, Fraction("133.322387415")),
        (uc.btu_it, u.J, Fraction("1055.05585262")),
        (uc.calorie_th, u.J, Fraction("4.184")),
        (uc.ton_of_tnt, u.J, Fraction("4.184e9")),
        (uc.light_year, u.m, Fraction(9_460_730_472_580_800)),
        (uc.shaku, u.m, Fraction(10, 33)),
        (uc.jin, u.g, Fraction(500)),
        (uc.statcoulomb, u.C, Fraction(1, 2_997_924_580)),
        (uc.curie, u.Bq, Fraction(37 * 10**9)),
        (uc.rankine, u.K, Fraction(5, 9)),
        (uc.byte, uc.bit, Fraction(8)),
        (uc.kibibyte, uc.byte, Fraction(1024)),
        (uc.tex_point, uc.scaled_point, Fraction(65536)),
        (uc.sverdrup, u.m**3 / u.s, Fraction(10**6)),
    ],
)
def test_exact_factor(unit: Unit, target: Unit, factor: Fraction) -> None:
    assert unit.conversion_factor(target) == factor
    assert unit.conversion(target).is_exact


# -- irrational definitions ----------------------------------------------------------------


def test_pi_cancels_between_angle_units() -> None:
    assert uc.degree.conversion(uc.arcminute).is_exact
    assert uc.turn.conversion_factor(uc.nato_mil) == 6400
    assert uc.degree.conversion(u.rad).certainty is Certainty.EXACT_IRRATIONAL
    assert float(uc.degree.conversion_factor(u.rad)) == pytest.approx(0.017453292519943295)


def test_parsec() -> None:
    conversion = uc.parsec.conversion(uc.light_year)
    assert conversion.certainty is Certainty.EXACT_IRRATIONAL
    assert float(conversion.factor) == pytest.approx(3.261563777167433)
    assert uc.megaparsec.conversion(uc.parsec).is_exact


def test_logarithmic_information_units() -> None:
    assert float(uc.nat.conversion_factor(uc.bit)) == pytest.approx(1.4426950408889634)
    assert float(uc.hartley.conversion_factor(uc.bit)) == pytest.approx(3.321928094887362)


# -- measured constants ----------------------------------------------------------------------


def test_planck_units_share_g() -> None:
    assert uc.planck_length.certainty is Certainty.MEASURED
    assert uc.planck_length.relative_uncertainty == pytest.approx(1.1e-5, rel=0.03)
    assert float(uc.planck_length.scale) == pytest.approx(1.616255e-35, rel=1e-6)
    assert float(uc.planck_mass.scale) == pytest.approx(2.176434e-8, rel=1e-6)
    # l_P / t_P is c exactly: G cancels.
    assert (uc.planck_length / uc.planck_time).conversion(uc.speed_of_light).is_exact
    # m_P · l_P = ħ/c, also independent of G (π remains, from ħ).
    product = (uc.planck_mass * uc.planck_length).conversion(u.kg * u.m)
    assert product.certainty is Certainty.EXACT_IRRATIONAL


def test_codata_values() -> None:
    assert uc.dalton.conversion_factor(u.kg) == Fraction("1.66053906892e-27")
    assert uc.dalton.relative_uncertainty == pytest.approx(3.1e-10, rel=0.02)
    assert uc.dalton.conversion(uc.dalton.scaled(Fraction(1, 1000), "mDa")).is_exact
    assert float(uc.atomic_unit_of_time.scale) == pytest.approx(2.4188843265864e-17, rel=1e-12)
    assert float(uc.atomic_unit_of_velocity.scale) == pytest.approx(2.18769126216e6, rel=1e-10)


def test_solar_mass_uncertainty_comes_from_g() -> None:
    assert uc.solar_mass.relative_uncertainty == pytest.approx(2.2e-5, rel=0.03)
    ratio = uc.solar_mass.conversion(uc.earth_mass)
    assert ratio.is_exact
    assert float(ratio.factor) == pytest.approx(332_946.0, rel=1e-6)


# -- estimated and nominal units ----------------------------------------------------------------


def test_ancient_units_are_correlated_within_a_system() -> None:
    assert uc.roman_uncia.conversion(uc.pes).is_exact
    foot = uc.pes.relative_uncertainty
    amphora = uc.amphora.relative_uncertainty
    assert foot is not None
    assert amphora is not None
    assert amphora == pytest.approx(3 * foot)
    assert uc.hekat.conversion(uc.royal_cubit**3).factor == Fraction(1, 30)


def test_disputed_and_informal_units() -> None:
    assert uc.megalithic_yard.certainty is Certainty.ESTIMATED
    assert uc.megalithic_yard.relative_uncertainty is None
    assert uc.pinch.certainty is Certainty.NOMINAL
    assert uc.pinch.conversion_factor(uc.us_teaspoon) == Fraction(1, 16)
    assert uc.smoot.certainty is Certainty.NOMINAL


def test_quantity_conversion_keeps_working() -> None:
    marathon = (26.2 * u.mi).to(uc.furlong)
    assert marathon.value == pytest.approx(209.6)
