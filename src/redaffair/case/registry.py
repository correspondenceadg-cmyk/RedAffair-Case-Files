CASE_SELECT_ENTRIES = {
    "classic": {
        "case_id": "classic",
        "display_name": "The Red Affair",
        "module": "redaffair.case.classic",
        "seed": 0,
        "location_set": "spaceship",
        "cast_universe": "legacy",
    },
}

def lookup(case_id: str):
    return CASE_SELECT_ENTRIES.get(case_id)
