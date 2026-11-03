import pytest
from src.redaffair.case import load_case, assert_all_invariants, Case

def test_classic_load():
    c = load_case("classic")
    assert c.case_id == "classic"
    assert c.killer_key == "thatcher"
    assert_all_invariants(c)

def test_roundtrip():
    c = load_case("classic")
    d = c.to_dict()
    c2 = Case.from_dict(d)
    assert c.case_id == c2.case_id
    assert c.title == c2.title
    assert c.killer_key == c2.killer_key
    assert c.incriminating == c2.incriminating
    assert set(c.suspects.keys()) == set(c2.suspects.keys())
    assert set(c.locations.keys()) == set(c2.locations.keys())

def test_invariants_fail():
    c = load_case("classic")
    c.killer_key = "marcus"
    with pytest.raises(AssertionError):
        assert_all_invariants(c)
