import json
import re
import os
import time
from .sat import solve
from ..case import Case, assert_all_invariants

# convictable(case, "thatcher") -> True
def convictable(case, suspect_key):
    if suspect_key not in case.suspects:
        return False
    suspect = case.suspects[suspect_key]
    if suspect.exonerated:
        return False
    hits = 0
    for clue_id in case.incriminating:
        impl, _ = case.EVIDENCE_IMPLICATION.get(clue_id, ([], []))
        if any(imp in suspect.name for imp in impl) or (suspect_key == case.killer_key and "Unknown" in impl):
            hits += 1
    return hits >= case.required_incriminating

def verify_unique_bruteforce(case):
    convicts = [k for k in case.suspects if convictable(case, k)]
    return len(convicts) == 1

def verify_unique_sat(case):
    suspects = list(case.suspects.keys())
    symbols = list(range(1, len(suspects) + 1))
    clauses = []
    clauses.append(symbols)
    for i in range(len(symbols)):
        for j in range(i+1, len(symbols)):
            clauses.append([-symbols[i], -symbols[j]])
    for i, k in enumerate(suspects):
        var = symbols[i]
        if convictable(case, k):
            clauses.append([var])
        else:
            clauses.append([-var])
    return solve(clauses, symbols)

def verify_all(case):
    bf = verify_unique_bruteforce(case)
    sat = verify_unique_sat(case)
    convicts = [k for k in case.suspects if convictable(case, k)]
    return {
        "bruteforce": bf,
        "sat": sat,
        "convictable": convicts,
        "killer": case.killer_key
    }

def _check_templates(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(k, str) and "[FLAVOR:" in k:
                return False
            if not _check_templates(v): return False
    elif isinstance(data, list):
        for v in data:
            if not _check_templates(v): return False
    elif isinstance(data, str):
        if "[FLAVOR:" in data:
            return False
    return True

# validate_import("{}") -> (False, "Gate 1 Failed (JSON parse)")
def validate_import(json_str):
    try:
        data = json.loads(json_str)
    except Exception as e:
        return False, f"Gate 1 Failed (JSON parse): {e}"

    if data.get("schema_version") != 1:
        return False, "Gate 2 Failed (Schema version mismatch)"

    try:
        case = Case.from_dict(data)
    except Exception as e:
        return False, f"Gate 1 Failed (from_dict): {e}"

    try:
        assert_all_invariants(case)
    except Exception as e:
        return False, f"Gate 3 Failed (Invariants): {e}"

    if not verify_unique_bruteforce(case):
        return False, "Gate 4 Failed (Bruteforce uniqueness)"

    if not verify_unique_sat(case):
        return False, "Gate 5 Failed (SAT uniqueness)"

    if not _check_templates(data):
        return False, "Gate 6 Failed (Template completeness)"

    return True, "Import successful"

def save_failed_import(json_str):
    os.makedirs("imports", exist_ok=True)
    path = f"imports/failed_{int(time.time())}.json"
    with open(path, "w") as f:
        f.write(json_str)
    return path
