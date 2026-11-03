from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class Suspect:
    name: str
    alive: bool = True
    hostile: bool = False
    detained: bool = False
    defeated: bool = False
    hp: int = 25
    motive: str = ""
    guilty: bool = False
    lean: str = ""
    characteristics: List[str] = field(default_factory=list)
    curses: List[str] = field(default_factory=list)
    exonerated: bool = False

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

@dataclass
class Location:
    desc: str = ""
    items: List[str] = field(default_factory=list)
    suspects: List[str] = field(default_factory=list)
    searchable: List[str] = field(default_factory=list)
    examinables: List[str] = field(default_factory=list)
    body_examinable: bool = False
    hidden_revolver: bool = False
    bullet_found: bool = False
    datachip_found: bool = False
    victim_id_found: bool = False

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

@dataclass
class Case:
    case_id: str
    title: str
    suspects: Dict[str, Suspect] = field(default_factory=dict)
    locations: Dict[str, Location] = field(default_factory=dict)
    suspect_descriptions: Dict[str, str] = field(default_factory=dict)
    suspect_aliases: Dict[str, str] = field(default_factory=dict)
    revealed_characteristic: Dict[str, Optional[str]] = field(default_factory=dict)
    MISLEADING_CLUES: Dict[str, List[str]] = field(default_factory=dict)
    MISLEADING_DIALOGUE: Dict[str, str] = field(default_factory=dict)
    MOTIVE_GOSSIP: Dict[str, tuple] = field(default_factory=dict)
    CONFRONT_DIALOGUE: Dict[str, str] = field(default_factory=dict)
    ADELINE_ESCAPE_REACTIONS: Dict[str, str] = field(default_factory=dict)
    EVIDENCE_DESCRIPTIONS: Dict[str, str] = field(default_factory=dict)
    EVIDENCE_IMPLICATION: Dict[str, tuple] = field(default_factory=dict)
    EVIDENCE_ALIASES: Dict[str, Any] = field(default_factory=dict)
    EVIDENCE_VERIFY: Dict[str, Optional[str]] = field(default_factory=dict)
    TAMPER_ACTIONS: Dict[str, tuple] = field(default_factory=dict)
    incriminating: set = field(default_factory=set)
    required_incriminating: int = 3
    killer_key: str = ""
    player_lean: str = ""
    location_set: str = ""
    cast_universe: str = ""
    seed: int = 0

def load_case(case_id: str) -> Case:
    from .classic import get_classic_data
    from . import flavor
    
    if case_id == "classic":
        data = get_classic_data()
        c = Case(
            case_id="classic",
            title=flavor.FLAVOR["case_classic_title"],
            suspects={k: Suspect(**v) for k, v in data["suspects"].items()},
            locations={k: Location(**v) for k, v in data["locations"].items()},
            suspect_descriptions=data["suspect_descriptions"],
            suspect_aliases=data["suspect_aliases"],
            revealed_characteristic=data["revealed_characteristic"],
            MISLEADING_CLUES=data["MISLEADING_CLUES"],
            MISLEADING_DIALOGUE=data["MISLEADING_DIALOGUE"],
            MOTIVE_GOSSIP=data["MOTIVE_GOSSIP"],
            CONFRONT_DIALOGUE=data["CONFRONT_DIALOGUE"],
            ADELINE_ESCAPE_REACTIONS=data["ADELINE_ESCAPE_REACTIONS"],
            EVIDENCE_DESCRIPTIONS=data["EVIDENCE_DESCRIPTIONS"],
            EVIDENCE_IMPLICATION=data["EVIDENCE_IMPLICATION"],
            EVIDENCE_ALIASES=data["EVIDENCE_ALIASES"],
            EVIDENCE_VERIFY=data["EVIDENCE_VERIFY"],
            TAMPER_ACTIONS=data["TAMPER_ACTIONS"],
            incriminating=data["incriminating"],
            required_incriminating=data["required_incriminating"],
            killer_key="thatcher",
            location_set="spaceship",
            cast_universe="legacy",
            seed=0
        )
        return c
    raise ValueError(f"Unknown case_id: {case_id}")

def resolve_suspect(name: str, aliases: Dict[str, str]) -> Optional[str]:
    if not name:
        return None
    name = name.strip().lower()
    return aliases.get(name)

def assert_all_invariants(case: Case):
    assert case.case_id
    assert case.killer_key in case.suspects
    
    killer = case.suspects[case.killer_key]
    killer_hits = 0
    for ev_id in case.incriminating:
        impl, _ = case.EVIDENCE_IMPLICATION.get(ev_id, ([], []))
        if any(imp in killer.name for imp in impl) or (case.killer_key == "thatcher" and "Unknown" in impl):
            killer_hits += 1
    assert killer_hits >= case.required_incriminating, f"Killer hits {killer_hits} < {case.required_incriminating}"
    assert not killer.exonerated
    
    for k, sus in case.suspects.items():
        if k == case.killer_key:
            continue
        hits = 0
        for ev_id in case.incriminating:
            impl, _ = case.EVIDENCE_IMPLICATION.get(ev_id, ([], []))
            if any(imp in sus.name for imp in impl):
                hits += 1
        assert hits <= 1, f"Non-killer {k} has {hits} incriminating hits > 1"
