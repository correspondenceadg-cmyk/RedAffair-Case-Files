from . import load_case, Case
from .persistence import load_state, save_state, SaveBroker
from .registry import lookup

def load_case_for_play(case_id: str, save_path: str = None) -> Case:
    entry = lookup(case_id)
    if not entry:
        raise ValueError(f"Case not found: {case_id}")
    
    case = load_case(case_id)
    
    if save_path:
        state = load_state(save_path)
        if state:
            _apply_state(case, state)
            
    return case

def _apply_state(case: Case, state: dict):
    if "player_lean" in state:
        case.player_lean = state["player_lean"]
    if "current_location" in state:
        pass
