from .sat import solve

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
