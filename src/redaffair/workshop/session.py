import json
from .generator import generate_case
from ..case.persistence import save_state

class WorkshopSession:
    def __init__(self):
        self.draft = None
        self.seed = 0

    def generate(self, seed, location_set="orbital_cruiseline", cast_universe="mixed"):
        self.seed = seed
        self.draft = generate_case(seed, location_set, cast_universe)
        return self.draft

    def promote(self):
        if not self.draft:
            return False
        return True

    def save_draft(self, path):
        if not self.draft:
            return False
        state = {
            "schema_version": 1,
            "case_id": self.draft.case_id,
            "title": self.draft.title,
            "seed": self.draft.seed,
            "killer": self.draft.killer_key,
        }
        return save_state(state, path)
