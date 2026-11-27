from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional


# Cast

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
    walk_on: bool = False
    alibi: str = ""
    description: str = ""
    room_assignment: str = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)


@dataclass
class Victim:
    name: str = "Marsha Stone"
    description: str = ""

    def get(self, key, default=None):
        return getattr(self, key, default)


# Locations

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

    def get(self, key, default=None):
        return getattr(self, key, default)


# Unified investigation item (evidence or clue)

@dataclass
class InvestigationItem:
    item_id: str
    display_name: str
    item_type: str = "evidence"  # "evidence" | "clue"
    prose: str = ""
    room: str = ""
    spot: str = ""
    acquisition: str = "examine"  # search | examine | take | body_search | coercion | container_open
    found_by_body_search: bool = False
    found_by_coercion: bool = False
    category: str = "Custom"
    implicates: List[str] = field(default_factory=list)
    exonerates: List[str] = field(default_factory=list)
    misleading: bool = False
    incriminating: bool = False
    aliases: List[str] = field(default_factory=list)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __post_init__(self):
        if self.item_type not in ("evidence", "clue"):
            raise ValueError(f"item_type must be 'evidence' or 'clue', got {self.item_type!r}")
        if self.acquisition not in ("search", "examine", "take", "body_search", "coercion", "container_open"):
            raise ValueError(f"acquisition invalid: {self.acquisition!r}")
        if self.acquisition == "body_search":
            self.found_by_body_search = True
        if self.acquisition == "coercion":
            self.found_by_coercion = True
        if self.item_type == "clue":
            if self.implicates or self.exonerates:
                raise ValueError(f"Clue {self.item_id} cannot implicate or exonerate")


# Coercion

@dataclass
class CoercionRule:
    suspect_key: str
    trigger: str = ""
    effect: str = ""

    def get(self, key, default=None):
        return getattr(self, key, default)


# Events

@dataclass
class SpecialEvent:
    event_id: str
    event_type: str = "BLACKOUT"  # BLACKOUT | UNEXPECTED_VISITOR | DECOMPRESSION | CONFESSION | SUSPECT_ESCAPE | LOCKDOWN
    trigger_mode: str = "free"  # "free" | "scripted"
    trigger: str = ""
    prose: str = ""

    def __post_init__(self):
        valid = ("BLACKOUT", "UNEXPECTED_VISITOR", "DECOMPRESSION", "CONFESSION", "SUSPECT_ESCAPE", "LOCKDOWN")
        if self.event_type not in valid:
            raise ValueError(f"event_type invalid: {self.event_type!r}")
        if self.trigger_mode not in ("free", "scripted"):
            raise ValueError(f"trigger_mode invalid: {self.trigger_mode!r}")

    def get(self, key, default=None):
        return getattr(self, key, default)


# Dialogue

@dataclass
class DialogueNode:
    node_id: str
    category: str = "motive"
    speaker: str = ""
    target: str = ""
    text: str = ""

    def get(self, key, default=None):
        return getattr(self, key, default)


# Case

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
    items: Dict[str, InvestigationItem] = field(default_factory=dict)
    coercion_rules: List[CoercionRule] = field(default_factory=list)
    special_events: List[SpecialEvent] = field(default_factory=list)
    dialogue_nodes: List[DialogueNode] = field(default_factory=list)
    victim: Optional[Victim] = None
    alibi_map: Dict[str, str] = field(default_factory=dict)
    walk_on_limit: int = 2
    cast_limit: int = 10
    event_limit: int = 6

    def to_dict(self) -> dict:
        d = asdict(self)
        d["incriminating"] = list(self.incriminating)
        d["MOTIVE_GOSSIP"] = {k: list(v) for k, v in self.MOTIVE_GOSSIP.items()}
        d["EVIDENCE_IMPLICATION"] = {k: list(v) for k, v in self.EVIDENCE_IMPLICATION.items()}
        d["TAMPER_ACTIONS"] = {k: list(v) for k, v in self.TAMPER_ACTIONS.items()}
        d["schema_version"] = 1
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Case":
        d = dict(d)
        d.pop("schema_version", None)

        suspects = {k: Suspect(**v) for k, v in d.get("suspects", {}).items()}
        locations = {k: Location(**v) for k, v in d.get("locations", {}).items()}
        items = {k: InvestigationItem(**v) for k, v in d.get("items", {}).items()}
        coercion_rules = [CoercionRule(**v) for v in d.get("coercion_rules", [])]
        special_events = [SpecialEvent(**v) for v in d.get("special_events", [])]
        dialogue_nodes = [DialogueNode(**v) for v in d.get("dialogue_nodes", [])]
        victim_raw = d.get("victim")
        victim = Victim(**victim_raw) if victim_raw else None

        mg = {k: tuple(v) for k, v in d.get("MOTIVE_GOSSIP", {}).items()}
        ei = {k: tuple(v) for k, v in d.get("EVIDENCE_IMPLICATION", {}).items()}
        ta = {k: tuple(v) for k, v in d.get("TAMPER_ACTIONS", {}).items()}

        return cls(
            case_id=d.get("case_id", ""),
            title=d.get("title", ""),
            suspects=suspects,
            locations=locations,
            suspect_descriptions=d.get("suspect_descriptions", {}),
            suspect_aliases=d.get("suspect_aliases", {}),
            revealed_characteristic=d.get("revealed_characteristic", {}),
            MISLEADING_CLUES=d.get("MISLEADING_CLUES", {}),
            MISLEADING_DIALOGUE=d.get("MISLEADING_DIALOGUE", {}),
            MOTIVE_GOSSIP=mg,
            CONFRONT_DIALOGUE=d.get("CONFRONT_DIALOGUE", {}),
            ADELINE_ESCAPE_REACTIONS=d.get("ADELINE_ESCAPE_REACTIONS", {}),
            EVIDENCE_DESCRIPTIONS=d.get("EVIDENCE_DESCRIPTIONS", {}),
            EVIDENCE_IMPLICATION=ei,
            EVIDENCE_ALIASES=d.get("EVIDENCE_ALIASES", {}),
            EVIDENCE_VERIFY=d.get("EVIDENCE_VERIFY", {}),
            TAMPER_ACTIONS=ta,
            incriminating=set(d.get("incriminating", [])),
            required_incriminating=d.get("required_incriminating", 3),
            killer_key=d.get("killer_key", ""),
            player_lean=d.get("player_lean", ""),
            location_set=d.get("location_set", ""),
            cast_universe=d.get("cast_universe", ""),
            seed=d.get("seed", 0),
            items=items,
            coercion_rules=coercion_rules,
            special_events=special_events,
            dialogue_nodes=dialogue_nodes,
            victim=victim,
            alibi_map=d.get("alibi_map", {}),
            walk_on_limit=d.get("walk_on_limit", 2),
            cast_limit=d.get("cast_limit", 10),
            event_limit=d.get("event_limit", 6),
        )

    def rebuild_flat_evidence(self):
        """Derive flat evidence dicts from items. No-op if items is empty."""
        if not self.items:
            return
        for item_id, item in self.items.items():
            short = item.prose.split(".")[0].strip() if item.prose else item.display_name
            self.EVIDENCE_DESCRIPTIONS[item_id] = short
            self.EVIDENCE_IMPLICATION[item_id] = (list(item.implicates), list(item.exonerates))
            self.EVIDENCE_ALIASES[item.display_name.lower()] = item_id
            for alias in item.aliases:
                self.EVIDENCE_ALIASES[alias.lower()] = item_id
            if item.item_type == "evidence" and (item.implicates or item.incriminating):
                self.incriminating.add(item_id)


def load_case(case_id: str) -> Case:
    from .classic import get_classic_data
    from . import flavor

    if case_id == "classic":
        data = get_classic_data()
        return Case(
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
            seed=0,
        )
    raise ValueError(f"Unknown case_id: {case_id}")


def resolve_suspect(name: str, aliases: Dict[str, str]) -> Optional[str]:
    if not name:
        return None
    return aliases.get(name.strip().lower())


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

    if case.items:
        primaries = [k for k, s in case.suspects.items() if not s.walk_on]
        assert len(primaries) <= case.cast_limit, f"Cast exceeds limit: {len(primaries)} > {case.cast_limit}"
        walks = [k for k, s in case.suspects.items() if s.walk_on]
        assert len(walks) <= case.walk_on_limit, f"Walk-ons exceed limit: {len(walks)} > {case.walk_on_limit}"
        assert len(case.special_events) <= case.event_limit, f"Special events exceed limit: {len(case.special_events)} > {case.event_limit}"

        for item_id, item in case.items.items():
            if item.item_type == "clue":
                assert not item.implicates and not item.exonerates, f"Clue {item_id} has implication data"
            for target in item.implicates + item.exonerates:
                if target == "Unknown":
                    continue
                assert any(target in s.name for s in case.suspects.values()), \
                    f"Item {item_id} references unknown suspect {target}"

    if case.victim and case.victim.name:
        assert case.victim.name.strip(), "Victim name is empty"
