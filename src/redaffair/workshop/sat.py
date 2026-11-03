def _propagate(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = [x for x in clause if x != -literal]
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def _dpll(clauses, symbols):
    if not clauses:
        return True
    if [] in clauses:
        return False
    if not symbols:
        return False
    p = symbols.pop()
    rest = symbols.copy()
    return _dpll(_propagate(clauses, p), rest.copy()) or _dpll(_propagate(clauses, -p), rest.copy())

def solve(clauses, symbols):
    return _dpll(clauses, symbols.copy())
