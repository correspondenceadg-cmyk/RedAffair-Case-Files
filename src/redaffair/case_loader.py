from __future__ import annotations

try:
    from .case import load_case, Case
    from .case.persistence import load_state, save_state, SaveBroker
except ImportError:
    from case import load_case, Case
    from case.persistence import load_state, save_state, SaveBroker


# load_case_for_play(classic) -> Case with save state merged
def load_case_for_play(case_id: str = "classic") -> tuple[Case, SaveBroker]:
    state = load_state(case_id)
    case = load_case(case_id, save_state=state)
    broker = SaveBroker(case_id)
    return case, broker


def save_current_state(case_id: str, state: dict) -> bool:
    return save_state(case_id, state)
