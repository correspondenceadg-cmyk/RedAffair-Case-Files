import random
from ..case.cast import LEGACY, EXTENDED

SLOT_TEMPLATES = {
    "weapon": ["A recently fired gun.", "A bloodstained knife.", "A heavy blunt object."],
    "cash": ["A stack of unmarked credits.", "A dropped wallet full of chits.", "A broken cash register."],
    "paper": ["A torn letter.", "A suspicious receipt.", "A forged ID card."],
    "digital": ["A datachip.", "A wiped comms log.", "A corrupted security feed."],
    "chemical": ["A vial of poison.", "A sedative injector.", "A strange powder."]
}

def get_suspects(rng: random.Random, universe="mixed", count=7):
    pool = {}
    if universe in ("legacy", "mixed"):
        pool.update(LEGACY)
    if universe in ("extended", "mixed"):
        pool.update(EXTENDED)
    
    keys = list(pool.keys())
    selected = rng.sample(keys, min(count, len(keys)))
    return {k: pool[k] for k in selected}
