import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_src_root = _here / "src" / "redaffair"
_pkg_root = _here

if _src_root.exists() and (_src_root / "case").exists():
    if str(_src_root) not in sys.path:
        sys.path.insert(0, str(_src_root))
elif (_pkg_root / "case").exists():
    if str(_pkg_root) not in sys.path:
        sys.path.insert(0, str(_pkg_root))

from case import load_case, Case
from case.persistence import load_state


def load_case_for_play(case_id: str, save_path: str = None) -> Case:
    case = load_case(case_id)
    if save_path:
        state = load_state(save_path)
        if state:
            _apply_state(case, state)
    return case


def _apply_state(case: Case, state: dict):
    if "player_lean" in state:
        case.player_lean = state["player_lean"]
