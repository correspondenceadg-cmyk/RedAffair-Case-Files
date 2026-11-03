import json
import os
import tempfile

SCHEMA_VERSION = 1

def save_state(state: dict, path: str) -> bool:
    try:
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=dirname or ".", text=True)
        with os.fdopen(fd, 'w') as f:
            json.dump(state, f, indent=2)
        os.replace(tmp_path, path)
        return True
    except Exception as e:
        print(f"Save failed: {e}")
        return False

def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        if data.get("schema_version") != SCHEMA_VERSION:
            return {}
        return data
    except Exception:
        return {}

class SaveBroker:
    def __init__(self, case_id: str, save_path: str):
        self.case_id = case_id
        self.save_path = save_path
        self.dirty = False

    def mark_dirty(self):
        self.dirty = True

    def save(self, state: dict):
        if not self.dirty:
            return
        state["schema_version"] = SCHEMA_VERSION
        state["case_id"] = self.case_id
        if save_state(state, self.save_path):
            self.dirty = False
