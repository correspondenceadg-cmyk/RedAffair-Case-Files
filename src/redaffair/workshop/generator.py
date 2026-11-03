import random
from ..case import Case, Suspect, Location, load_case
from ..case.location_sets import LOCATION_SETS
from .verifier import verify_unique_bruteforce
from .pools import get_suspects

# generate_case(0) -> classic case
def generate_case(seed=0, location_set="orbital_cruiseline", cast_universe="mixed"):
    if seed == 0:
        return load_case("classic")
        
    rng = random.Random(seed)
    
    loc_data = LOCATION_SETS.get(location_set, LOCATION_SETS["orbital_cruiseline"])
    rooms = loc_data["rooms"]
    
    cast_pool = get_suspects(rng, cast_universe, count=7)
    cast_keys = list(cast_pool.keys())
    
    # Loop ensures we find a unique valid killer for this seed
    while True:
        killer_key = rng.choice(cast_keys)
        
        suspects = {}
        for k in cast_keys:
            suspects[k] = Suspect(
                name=cast_pool[k]["name"],
                characteristics=cast_pool[k]["characteristics"],
                curses=cast_pool[k]["curses"],
                guilty=(k == killer_key)
            )
        
        locations = {}
        for i, room in enumerate(rooms):
            loc_suspects = []
            if i == 0:
                loc_suspects = [killer_key]
            locations[room] = Location(desc=f"THE {room.upper()}", suspects=loc_suspects)
            
        locations[rooms[0]].desc += "\n\n" + f"{suspects[killer_key].name} is here."
        
        evidence_descriptions = {}
        evidence_implication = {}
        incriminating = set()
        
        ev_count = 1
        for _ in range(5):
            ev_id = f"gen_ev_{ev_count}"
            evidence_descriptions[ev_id] = "A suspicious item."
            evidence_implication[ev_id] = ([suspects[killer_key].name], [])
            incriminating.add(ev_id)
            ev_count += 1
            
        case = Case(
            case_id=f"gen_{seed}",
            title=f"Generated Case {seed}",
            suspects=suspects,
            locations=locations,
            EVIDENCE_DESCRIPTIONS=evidence_descriptions,
            EVIDENCE_IMPLICATION=evidence_implication,
            incriminating=incriminating,
            required_incriminating=3,
            killer_key=killer_key,
            location_set=location_set,
            cast_universe=cast_universe,
            seed=seed
        )
        
        if verify_unique_bruteforce(case):
            break
            
    return case
