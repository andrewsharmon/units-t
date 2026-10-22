from fractions import Fraction

import pytest

from units_t import Certainty, UncertaintyTerm
from units_t import units as u
from units_t.provenance import measured, nominal

DALTONISH = measured("test constant", 1e-9, "a made-up measured constant")


def test_exact_units_have_no_terms() -> None:
    assert u.mi.is_exact
    assert u.mi.certainty is Certainty.EXACT
    assert u.mi.relative_uncertainty == 0.0


def test_terms_propagate_through_algebra() -> None:
    thing = u.kg.scaled(3, "thing", uncertainty=DALTONISH)
    assert (thing * u.m).relative_uncertainty == pytest.approx(1e-9)
    assert (thing**2).relative_uncertainty == pytest.approx(2e-9)
    assert (thing ** Fraction(1, 2)).relative_uncertainty == pytest.approx(0.5e-9)


def test_shared_terms_cancel() -> None:
    thing = u.kg.scaled(3, "thing", uncertainty=DALTONISH)
    millithing = thing.scaled(Fraction(1, 1000), "mthing")
    conversion = millithing.conversion(thing)
    assert conversion.factor == Fraction(1, 1000)
    assert conversion.is_exact
    assert (thing / thing).is_exact


def test_independent_terms_add_in_quadrature() -> None:
    a = u.m.scaled(1, "a", uncertainty=measured("a", 3e-6, "a"))
    b = u.m.scaled(1, "b", uncertainty=measured("b", 4e-6, "b"))
    assert a.conversion(b).relative_uncertainty == pytest.approx(5e-6)


def test_unquantified_term_makes_uncertainty_unknown() -> None:
    vague = u.m.scaled(1, "vague", uncertainty=nominal("vague", "who knows"))
    precise = u.m.scaled(1, "p", uncertainty=DALTONISH)
    assert (vague * precise).relative_uncertainty is None
    assert (vague * precise).certainty is Certainty.NOMINAL


def test_metadata_does_not_affect_equality() -> None:
    uncertain_metre = u.m.scaled(1, "m?", "metre-ish", uncertainty=DALTONISH)
    assert uncertain_metre == u.m


def test_exact_term_is_rejected() -> None:
    with pytest.raises(ValueError):
        UncertaintyTerm("x", Certainty.EXACT, 0.0, "pointless")


def test_sources_propagate() -> None:
    assert any(s.key == "Yard-Pound-1959" for s in (u.mi / u.h).sources)


def test_explain_mentions_terms_and_sources() -> None:
    thing = u.kg.scaled(3, "thing", uncertainty=DALTONISH)
    text = thing.conversion(u.kg).explain()
    assert "measured" in text
    assert "test constant" in text
    assert "BIPM" in text
