from src.redaffair.case import load_case

def test_scripted_playthrough():
    case = load_case("classic")
    assert case.killer_key == "thatcher"
