from src.redaffair.workshop.generator import generate_case
from src.redaffair.case import assert_all_invariants
from src.redaffair.workshop.verifier import verify_unique_bruteforce, verify_unique_sat

def test_10k_seeds():
    killers = set()
    for seed in range(1, 10001):
        case = generate_case(seed)
        assert_all_invariants(case)
        assert verify_unique_bruteforce(case)
        assert verify_unique_sat(case)
        killers.add(case.killer_key)
        
    assert len(killers) > 1, "Killer variation failed: generated only one killer across 10k seeds"

def test_determinism():
    for seed in [42, 100, 999]:
        c1 = generate_case(seed)
        c2 = generate_case(seed)
        assert c1.killer_key == c2.killer_key
        assert c1.case_id == c2.case_id
        assert c1.suspects == c2.suspects
        assert c1.locations == c2.locations
