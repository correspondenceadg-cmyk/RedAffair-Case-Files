import json
import pytest
from src.redaffair.workshop.session import WorkshopSession
from src.redaffair.workshop.verifier import validate_import
from src.redaffair.case import load_case

def test_workshop_lifecycle(tmp_path):
    session = WorkshopSession()
    draft = session.generate(42)
    assert draft is not None
    assert draft.killer_key != ""
    
    path = tmp_path / "draft.json"
    assert session.save_draft(str(path))
    assert path.exists()

def test_validate_import():
    c = load_case("classic")
    data = json.dumps(c.to_dict())
    
    ok, msg = validate_import(data)
    assert ok, msg

def test_validate_import_fail_schema():
    ok, msg = validate_import("{}")
    assert not ok
    assert "Gate 2 Failed" in msg

def test_validate_import_fail_invariants():
    c = load_case("classic")
    c.killer_key = "marcus"
    data = json.dumps(c.to_dict())
    ok, msg = validate_import(data)
    assert not ok
    assert "Gate 3 Failed" in msg
