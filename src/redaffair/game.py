import random, sys, os, textwrap

sfx_queue = None
cheat_unlimited_cuffs = False
cheat_god_mode = False
cheat_infinite_countenance = False
active_case_id = "classic"
active_seed = 0

def play_game():
    RED = '\033[31m'
    BLACK_BG = '\033[40m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'

    TOTAL_NON_MISLEADING = 21

    def clear_screen():
        print("##CLEARSCREEN##")

    def get_first_name(full_name):
        return full_name.split()[0]

    clear_screen()
    print(RED + BLACK_BG + BOLD +
        "The Red Affair\n\n"
        "A greasy spoon-dive at the edge of the Pillars of Creation. No sound travels\n"
        "through the vacuum of space, but the constant debris, gas, and radiation that\n"
        "beats on the clear polymerate windows makes it sound like the whine of creation\n"
        "on a loop like a scratched magneto-disc.\n"
        "The air scrubber is on the fritz, but that's not why it's so stuffy in here,\n"
        "or why the coffee tastes perhaps a little more than just recycled. A body is\n"
        "cooling in the back, and it's your job to figure out why.\n\n"
        "Outside the porthole: The Grand Void, silence only ever punctuated by\n"
        "the occasional existential scream of a dying star, planet, or god.\n\n"
        "The airlock is sealed. The unmanned aerospace police drone is a few hours out.\n"
        "Somewhere in this fluorescent flickering palisade of sin, a killer waits."
    + RESET)
    print()
    input("Press Enter to begin...")
    clear_screen()

    player_name = input(f"{RED}{BLACK_BG}Your name, detective, if you subscribe to such niceties: {RESET}").strip()
    if not player_name:
        player_name = "Myla-Dean"
    print(f"\n{RED}{BLACK_BG}The name's {player_name}. Licensed to poke around in other people's misery.\n")
    print(f"The universe doesn't care. But you should, and here you are.{RESET}\n")

    LEANINGS = ["communist", "fascist", "liberal", "anarchist"]
    print(f"{RED}{BLACK_BG}Before we begin – your, um- political leanings?")
    print("(It matters as much as anything matters in a pressurized tin can. Turns out? Quite a lot.)")
    print("1. Communist – Strong and welcoming. The people united will never be defeated.")
    print("2. Fascist – Order above all. Strength through unity. Terrifying.")
    print("3. Liberal – The free market solves everything. Adorable.")
    print("4. Anarchist – No gods, no masters, no parking tickets. Chaotic.")
    while True:
        choice = input(f"Choose your delusion (1-4): {RESET}").strip()
        if choice == '1':
            player_lean = "communist"
            break
        elif choice == '2':
            player_lean = "fascist"
            break
        elif choice == '3':
            player_lean = "liberal"
            break
        elif choice == '4':
            player_lean = "anarchist"
            break
        else:
            print("Oh, come on. Don't tell me you're one of those ''radical centrist'' types. You're -you're not, are you?")
    print(f"\nA {player_lean} detective. The universe adjusts its expectations accordingly. You probably should as well.\n")
    input("Press Enter to step in through the airlock...and into the lockdown.")
    clear_screen()

    RESERVED_KEY_THX1138 = "thatcher"

    # ---------- Case Loading ----------
    try:
        from .case_loader import load_case_for_play
    except ImportError:
        from case_loader import load_case_for_play

    case_to_load = globals().get('active_case_id', 'classic')
    case = load_case_for_play(case_to_load)

    # ---------- Political Leanings ----------
    lean_pool = ["communist"]*2 + ["fascist"]*2 + ["liberal"]*2 + ["anarchist"]*2
    random.shuffle(lean_pool)
    lean_pool.pop()
    shuffled_leans = lean_pool[:]
    suspect_leans = {
        "marcus": shuffled_leans[0],
        "napoleon": shuffled_leans[1],
        "cleopatra": shuffled_leans[2],
        "janitor": shuffled_leans[3],
        "cook": shuffled_leans[4],
        "patron": shuffled_leans[5],
        RESERVED_KEY_THX1138: shuffled_leans[6]
    }

    suspects = case.suspects
    locations = case.locations
    suspect_descriptions = case.suspect_descriptions
    suspect_aliases = case.suspect_aliases
    revealed_characteristic = case.revealed_characteristic
    MISLEADING_CLUES = case.MISLEADING_CLUES
    MISLEADING_DIALOGUE = case.MISLEADING_DIALOGUE
    MOTIVE_GOSSIP = case.MOTIVE_GOSSIP
    CONFRONT_DIALOGUE = case.CONFRONT_DIALOGUE
    ADELINE_ESCAPE_REACTIONS = case.ADELINE_ESCAPE_REACTIONS
    EVIDENCE_DESCRIPTIONS = case.EVIDENCE_DESCRIPTIONS
    EVIDENCE_IMPLICATION = case.EVIDENCE_IMPLICATION
    EVIDENCE_ALIASES = case.EVIDENCE_ALIASES
    EVIDENCE_VERIFY = case.EVIDENCE_VERIFY
    TAMPER_ACTIONS = case.TAMPER_ACTIONS
    incriminating = case.incriminating
    required_incriminating = case.required_incriminating

    for k, s in suspects.items():
        s["lean"] = suspect_leans.get(k, "communist")

    # ---------- Dynamic Expansions ----------
    freezer_unlocked = False
    freezer_cleaver_found = False
    bathroom_panel_revealed = False
    revolver_found = False
    bullet_found_in_office = False
    label_taken = False
    victim_id_found = False

    ring_or_id = random.choice(["signet ring", "galactic_id"])
    locations["office"]["items"].remove("ring_or_id")
    locations["office"]["items"].append(ring_or_id)

    # ---------- Game State ----------
    current_location = "counter"
    inventory = ["notepad"]
    if player_lean == "liberal":
        inventory.append("credits_wad")
    handcuffs = 3
    clues = set()
    body_examined = False
    game_over = False
    traits_revealed = set()
    trust = {}
    nyx_escape_offered = False
    nyx_escaped = False
    corruption_planted = None
    tainted_evidence = False
    talk_history = {}
    countenance_used = False

    for s in suspects:
        trust[s] = 1 if suspects[s]["lean"] == player_lean else 0

    # ---------- Player Stats ----------
    player = {
        "hp": 30,
        "max_hp": 30,
        "level": 1,
        "xp": 0,
        "xp_to_next": 3,
        "base_damage": 5.0,
        "regular_hit_chance": 0.20,
        "special_hit_chance": 0.10
    }

    # ---------- Helper Functions ----------
    def evidence_display_name(clue_id):
        return EVIDENCE_DESCRIPTIONS.get(clue_id, clue_id).split('.')[0].strip()

    def is_misleading(clue_id):
        for v in MISLEADING_CLUES.values():
            if clue_id in v:
                return True
        return False

    # ---------- HUD ----------
    def hud():
        print(RED + BLACK_BG + "╔══ HUD ═══════════════════════════════════════════╗")
        print(f"║ Location: {current_location.ljust(8)}  Cuffs: {handcuffs}/3    HP: {player['hp']}/{player['max_hp']}   ║")
        print(f"║ Evidence: {len(clues)}/{TOTAL_NON_MISLEADING}                            ║")
        print("╚══════════════════════════════════════════════════╝" + RESET)

    # ---------- Evidence Management ----------
    def add_evidence(ev_id):
        if ev_id not in clues:
            clues.add(ev_id)
            print(f"{RED}📋 Evidence: {evidence_display_name(ev_id)} ({len(clues)}/{TOTAL_NON_MISLEADING}){RESET}")
            player["xp"] += 1
            if player["xp"] >= player["xp_to_next"]:
                level_up()

    def remove_evidence(ev_id):
        if ev_id in clues:
            clues.remove(ev_id)
            print(f"{RED}📋 Evidence lost: {evidence_display_name(ev_id)} ({len(clues)}/{TOTAL_NON_MISLEADING}){RESET}")

    # ---------- Level Up ----------
    def level_up():
        player["level"] += 1
        player["xp"] = 0
        player["xp_to_next"] += 2
        player["max_hp"] += 5
        player["hp"] = player["max_hp"]
        player["base_damage"] += 0.5
        reg_increase = random.randint(5, 10) / 100.0
        spec_increase = random.randint(5, 10) / 100.0
        player["regular_hit_chance"] = min(player["regular_hit_chance"] + reg_increase, 0.95)
        player["special_hit_chance"] = min(player["special_hit_chance"] + spec_increase, 0.95)
        print(f"{RED}🎉 LEVEL UP! Level {player['level']}. HP: {player['hp']}/{player['max_hp']}{RESET}")
        if sfx_queue: sfx_queue.put('lvlup')

    # ---------- Trust ----------
    def trust_change(sus, amount):
        trust[sus] = max(0, min(3, trust[sus] + amount))
        if amount > 0:
            print(f"Trust with {get_first_name(suspects[sus]['name'])} up ({trust[sus]}/3)")
        elif amount < 0:
            print(f"Trust with {get_first_name(suspects[sus]['name'])} down ({trust[sus]}/3)")

    # ---------- Reveal Characteristic ----------
    def reveal_characteristic(sus):
        if sus == RESERVED_KEY_THX1138:
            print(f"{get_first_name(suspects[sus]['name'])} lights a smoke in their hand and waves dismissively: 'The killer? I have no idea. I was contemplating things that actually mattered.'")
            return
        trait = revealed_characteristic[sus]
        if trait not in traits_revealed:
            traits_revealed.add(trait)
            print(f"{get_first_name(suspects[sus]['name'])} leans in: 'The killer was definitely {trait}. I just know it. I mean, they'd have to be to do something like that.'")
            print(f"   (Clue: {trait})")
        else:
            print(f"{get_first_name(suspects[sus]['name'])} already told you. You weren't listening...were you...?")

    def check_traits():
        if len(traits_revealed) >= 3:
            killer_traits = suspects[RESERVED_KEY_THX1138]["characteristics"]
            if sum(1 for t in traits_revealed if t in killer_traits) >= 3:
                return True
        return False

    # ---------- Location Description ----------
    def describe_location():
        loc = locations[current_location]
        desc = loc["desc"]
        if current_location == "dining" and revolver_found:
            desc += "\nThe napkin dispenser is empty – you already liberated its secret."
        if current_location == "office":
            if bullet_found_in_office:
                desc += "\nA spent bullet casing glints under the desk."
        if current_location == "bathroom" and body_examined:
            desc += "\nThe body remains, patient as only the dead can be."
            if bathroom_panel_revealed:
                desc += "\nA loose panel behind the toilet hints at secrets."
        sus_keys = loc.get("suspects", [])
        for sus_key in sus_keys:
            s = suspects[sus_key]
            if s["exonerated"]:
                desc += f"\n\n{get_first_name(s['name'])} is here, but they've been completely exonerated. Not worth your time."
            elif s["alive"] and not s["detained"] and not s["defeated"]:
                desc += f"\n\n{get_first_name(s['name'])} is here. Trust: {trust[sus_key]}/3 – fragile as a soap bubble."
                desc += f"\nPolitical lean: {s['lean']}"
            elif s["detained"]:
                desc += f"\n\n{get_first_name(s['name'])} is handcuffed, radiating silent fury."
            elif s["defeated"]:
                desc += f"\n\n{get_first_name(s['name'])} is unconscious, dreaming whatever dreams a bruised ego conjures."
        print(desc)

    # ---------- Movement ----------
    def move(direction):
        nonlocal current_location
        if direction == "freezer":
            if not freezer_unlocked:
                print("The freezer door is locked tight. Maybe there's a reason to check in here...")
                return
        if direction in locations:
            current_location = direction
            clear_screen()
            hud()
            describe_location()
        else:
            print("Not a room. Try: counter, dining, kitchen, office, bathroom, freezer.")

    # ---------- Search ----------
    def search():
        nonlocal revolver_found, bullet_found_in_office, bathroom_panel_revealed, freezer_unlocked, freezer_cleaver_found, label_taken, victim_id_found
        loc = locations[current_location]
        if current_location == "dining" and loc.get("hidden_revolver") and not revolver_found:
            revolver_found = True
            inventory.append("revolver")
            print("In Plain View: cold metal made for someone with even colder blood; a revolver. It's definitely recently fired – the barrel still whispers gunpowder to anyone who will pay attention.")
            add_evidence("unknown_revolver")
            return
        if current_location == "office" and revolver_found and not bullet_found_in_office:
            bullet_found_in_office = True
            print("A spent bullet casing, half hidden beneath the desk. It matches the revolver's calibre.")
            add_evidence("bullet_casing")
            return
        if current_location == "bathroom" and bathroom_panel_revealed and not locations["bathroom"]["datachip_found"]:
            locations["bathroom"]["datachip_found"] = True
            print("You pry open the loose panel. Inside: a datachip, cold and unmarked.")
            add_evidence("datachip")
            inventory.append("datachip")
            return
        if current_location == "bathroom" and body_examined and not victim_id_found:
            victim_id_found = True
            inventory.append("galactic_id2")
            add_evidence("galactic_id2")
            print("You find a second ID card tucked inside her jacket. It's real. Marsha Stone.")
            return
        if current_location == "freezer":
            if not freezer_cleaver_found and "cook_landlord" in talk_history:
                freezer_cleaver_found = True
                print("Buried under synth-crab: a cleaver stained with something dark and ominous.")
                add_evidence("bloody_cleaver")
                return
            elif "adeline_timestamps" in clues and "adeline_alibi_confirmed" not in clues:
                add_evidence("adeline_alibi_confirmed")
                print("A log sheet on the freezer door confirms Adeline was inside at the time of the murder. Solid alibi.")
                return
        if current_location == "counter" and "aiden_alibi" not in clues:
            print("Payphone log. Aiden was on a call at time of death. It's hard to be in two places at once, but you've seen stranger things.")
            add_evidence("aiden_alibi")
            trust_change("marcus", 1)
            return
        if current_location == "counter" and "luka_alibi" not in clues:
            print("A wet floor sign and a pristine sheen near the counter. Elliot's work, no doubt.")
            add_evidence("luka_alibi")
            trust_change("janitor", 1)
            return
        if current_location == "dining" and "blake_alibi" not in clues:
            print("Time-stamped napkin. Blake's scribblings. He was here all evening writing some sort of...polemic? Seems pretty unlikely he's your man.")
            add_evidence("blake_alibi")
            trust_change("napoleon", 1)
            return
        if current_location == "dining" and "hemlock_missing" not in clues:
            print("An old coffee receipt. The timestamp is hours before the murder, but it doesn't confirm his whereabouts during.")
            add_evidence("hemlock_missing")
            trust_change("patron", 1)
            return
        if current_location == "kitchen" and "alice_alibi" not in clues:
            print("Bus ticket stub. The schedule readout on your personal device confirms Alice would have arrived just before the shot, maybe even just after. Well, that dog just don't hunt.")
            add_evidence("alice_alibi")
            trust_change("cleopatra", 1)
            return
        if current_location == "kitchen" and "adeline_timestamps" not in clues:
            print("A stock bucket with a timestamped order docket. Adeline's alibi checks out, at least on the surface.")
            add_evidence("adeline_timestamps")
            trust_change("cook", 1)
            freezer_unlocked = True
            print("Adeline hands you the freezer key. 'Here, have a look if you want.'")
            return
        if current_location == "office" and "nyx_message" not in clues:
            inventory.append("torn thesis")
            add_evidence("nyx_message")
            print(f"Torn paper. {suspects[RESERVED_KEY_THX1138]['name']}'s handwriting. Hard to make out... clearly an angry letter preceded by at least a couple more.")
            return
        print("Nothing. Nothing worth mentioning anyway, just grease, despair, and the miasma of mystery.")

    # ---------- Examine ----------
    def examine(item):
        nonlocal body_examined, bathroom_panel_revealed, victim_id_found
        if item == "body" and current_location == "bathroom":
            if not body_examined:
                body_examined = True
                print("The victim appears to be between the ages of 25 and 30. Feminine. Her clothes are intact, the wallet still clutched in her fist. She's approximately 5 feet tall. Her makeup is done, smeared only by the blood. You wonder what foundation she used.\n\nThe victim's face: mild surprise. Death wasn't so much terrifying as it was rude. Between the eyes is a bullet wound: neat, centered, professional even. Someone knew what they were doing.\n\nYou carefully search her pockets. Inside her jacket you find a real ID: Marsha Stone. That's her name. The one upstairs is a clear fake, but it's still up in the air as to what it was used for exactly.")
                if not victim_id_found:
                    victim_id_found = True
                    inventory.append("galactic_id2")
                    add_evidence("galactic_id2")
            else:
                print("The body remains. It hasn't changed. Corpses rarely do.")
                if not bathroom_panel_revealed and trust["janitor"] >= 3:
                    bathroom_panel_revealed = True
                    print("You notice something new: a loose panel behind the toilet. The janitor must have mentioned it.")
            return
        if item == "corkboard" and current_location == "kitchen":
            print("The corkboard is a collage of fading schedules, a yellowed menu, and a crisp flier for 'Reyes Properties'. The same name as on the victim's ID, if you've seen it.")
            if "galactic_id" in inventory or "galactic_id2" in inventory:
                print("The connection clicks: the victim owned the complex where Adeline lives.")
            return
        if item == "freezer" and current_location == "kitchen":
            if freezer_unlocked:
                print("The walk-in freezer hums softly. You can now enter it properly. Try 'go freezer'.")
            else:
                print("The walk-in freezer door is locked. You'd need a reason to open it.")
            return
        if item in ["signet ring", "galactic_id"] and item in locations[current_location]["items"]:
            if item == "signet ring":
                print("A heavy silver ring, engraved with the initials E.R. It feels cold and important.")
            else:
                print("The ID reads 'E. Reyes' with a photo of the victim. It's clearly a forgery.")
            inventory.append(item)
            locations[current_location]["items"].remove(item)
            return
        if item == "poison vial" and item in locations[current_location]["items"]:
            print("A small vial of clear liquid. It smells faintly of almonds. Cyanide, maybe. Or just bad coffee syrup.")
            inventory.append(item)
            locations[current_location]["items"].remove(item)
            return
        if item in ("notepad", "notes", "notebook"):
            show_notepad()
            return

        # ---------- Evidence Lookup via Aliases ----------
        ev_id = EVIDENCE_ALIASES.get(item.lower())
        if ev_id is None:
            if item in EVIDENCE_DESCRIPTIONS:
                ev_id = item
        if isinstance(ev_id, list):
            found = next((eid for eid in ev_id if eid in clues), None)
            if found is None:
                found = ev_id[0]
            ev_id = found
        if ev_id:
            desc = EVIDENCE_DESCRIPTIONS.get(ev_id, "No description.")
            impl, exon = EVIDENCE_IMPLICATION.get(ev_id, (["Unknown"], []))
            impl_str = ", ".join(impl) if impl else "None"
            exon_str = ", ".join(exon) if exon else "None"
            print(f"{desc}\nImplicates: {impl_str}\nExonerates: {exon_str}")
            verify = EVIDENCE_VERIFY.get(ev_id)
            if verify is not None:
                print(verify)
                if ev_id == "blake_alibi" and "blake_alibi_confirmed" not in clues:
                    add_evidence("blake_alibi_confirmed")
                if ev_id == "alice_alibi" and "alice_alibi_confirmed" not in clues:
                    add_evidence("alice_alibi_confirmed")
            return
        print(f"You give the {item} a good look over. It's definitely a {item}. What were you expecting?")

    # ---------- Notepad ----------
    def show_notepad():
        if not clues:
            print(RED + BLACK_BG + "╔══ NOTEPAD ═══════════════════════════════════════╗")
            print("║ The notepad is empty. Nothing to review yet.      ║")
            print("╚══════════════════════════════════════════════════╝" + RESET)
        else:
            print(RED + BLACK_BG + "╔══ NOTEPAD ═══════════════════════════════════════╗")
            shown_meta = set()
            for c in sorted(clues):
                meta = None
                for alias, ids in EVIDENCE_ALIASES.items():
                    if isinstance(ids, list) and c in ids:
                        meta = alias
                        break
                if meta:
                    if meta not in shown_meta:
                        shown_meta.add(meta)
                        name = meta
                        sources = [evidence_display_name(sc) for sc in ids if sc in clues]
                        combined_desc = f"║  • {name}  [Sources: {', '.join(sources)}]"
                        if any(is_misleading(sc) for sc in ids):
                            combined_desc = f"║  {GRAY}• {name} (suspicious)  [Sources: {', '.join(sources)}]{RESET}"
                        print(combined_desc)
                else:
                    display_name = evidence_display_name(c)
                    if c == "galactic_id":
                        display_name = "Fake ID"
                    elif c == "galactic_id2":
                        display_name = "Victim's ID"
                    impl, exon = EVIDENCE_IMPLICATION.get(c, (["Unknown"], []))
                    impl_str = ", ".join(impl) if impl else "None"
                    exon_str = ", ".join(exon) if exon else "None"
                    line = f"║  • {display_name}  [Implicates: {impl_str}; Exonerates: {exon_str}]"
                    if is_misleading(c):
                        line = f"║  {GRAY}• {display_name} (suspicious)  [Implicates: {impl_str}; Exonerates: {exon_str}]{RESET}"
                    print(line)
            print("╚══════════════════════════════════════════════════╝" + RESET)

    # ---------- Take ----------
    def take(item):
        loc = locations[current_location]
        if item == "label" and "label" in loc["items"]:
            loc["items"].remove("label")
            inventory.append("label")
            print("You peel the label off the container. Hopefully, Adeline won't notice. She seems harmless, but if she isn't, she's truly unstable.")
            return
        if item in loc["items"]:
            loc["items"].remove(item)
            inventory.append(item)
            print(f"Pocketed: {item}. Maybe you can find some use for it, or just a keep it as a souvenir of this...establishment.")
            if sfx_queue: sfx_queue.put('take')
        else:
            print("It's not here. Maybe it was never here. Maybe nothing is.")

    # ---------- Talk ----------
    def talk(sus):
        nonlocal nyx_escape_offered, freezer_unlocked
        if not sus:
            print("Who did you want to talk to? Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander (or their last names).")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' is not a person here. Try: Aiden Adams, Blake Jughashvili, Alice Oliverae, Nyx Singénero, Elliot Luka, Adeline Malovega, Alexander Hemlock.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been completely cleared. Anything they say is now officially irrelevant.")
            return
        if not s["alive"] or s["defeated"]:
            print("They're beyond conversation. The void has claimed their attention.")
            return
        if s["hostile"]:
            print(f"{get_first_name(s['name'])} fixes you with a stare that could curdle deuterium. No conversation today.")
            return
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print(f"{get_first_name(s['name'])} isn't here. Space is big. This diner is small. Try the right room.")
            return

        print(f"\n{RED}You approach {get_first_name(s['name'])}. The air shifts.{RESET}")
        print(f"Trust: {trust[sus]}/3 | Lean: {s['lean']}")
        
        if s["detained"]:
            print("The cuffs have a way of making people uncooperative. Trust can only go down from here.")
            trust[sus] = max(0, trust[sus] - 1)

        if trust[sus] == 3 and revealed_characteristic[sus] not in traits_revealed:
            reveal_characteristic(sus)

        if sus == "cook" and trust[sus] >= 2:
            if "cook_landlord" not in talk_history:
                talk_history["cook_landlord"] = True
                print(f"{get_first_name(s['name'])} suddenly blurts out: 'Marsha... she was my landlord. Always hounding me for rent. Can you believe it?'")
                freezer_unlocked = True

        if sus == RESERVED_KEY_THX1138 and trust[sus] == 3 and not nyx_escape_offered:
            nyx_escape_offered = True
            print(f"\nNyx gives you a long, appraising look. There's something there that you only realize as their lips part and they issue an appeal to your better, perhaps your worst, nature, 'You know, detective... we could help each other.' Your blood runs cold and your heart beats a little faster. You know what they're asking, the only question is whether or not you will.")
            choice = input("Let Nyx escape? (y/n): ").strip().lower()
            if choice == 'y':
                nyx_escape_ending()
                return
            else:
                print("Nyx shrugs. 'Your loss, detective.' The moment passes, but you will never forget it.")

        while True:
            print("\nWhat do you say?")
            options = ["alibi"]
            if trust[sus] >= 1:
                options.append("motive")
            if trust[sus] >= 2:
                if sus == RESERVED_KEY_THX1138 and "nyx_message" in clues:
                    options.append("the torn paper")
                if sus == RESERVED_KEY_THX1138 and revolver_found:
                    options.append("the revolver")
                if sus == "marcus" and "aiden_footprint" not in clues:
                    options.append("anything odd outside")
                if sus == "napoleon" and "blake_witness" not in clues:
                    options.append("did you see anything")
                if sus == "cleopatra" and "alice_witness" not in clues:
                    options.append("the argument")
                if sus == "janitor" and "luka_swept" not in clues:
                    options.append("the floor")
                if sus == "cook" and "adeline_heard" not in clues:
                    options.append("the office")
                if sus == "patron" and "hemlock_yelling" not in clues:
                    options.append("the noise")
            if trust[sus] >= 3:
                gossip_clue = None
                for speaker, (target, _, clue_id) in MOTIVE_GOSSIP.items():
                    if target == sus and clue_id in clues:
                        gossip_clue = clue_id
                        break
                if gossip_clue:
                    options.append(f"confront {get_first_name(suspects[sus]['name'])}")

            if suspects["cook"].get("escaped", False) and sus != "cook":
                options.append("Adeline's escape")

            for i, opt in enumerate(options, 1):
                print(f"{i}. Ask about {opt}")
            print("0. Step away")
            choice = input("> ").strip()
            if choice == "0":
                break
            if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
                print("That dog don't hunt. Try something else.")
                continue
            topic = options[int(choice)-1]
            talk_key = (sus, topic)

            if talk_key in talk_history and topic != f"confront {get_first_name(suspects[sus]['name'])}":
                print(f"You've already gone over that with {get_first_name(s['name'])}. Nothing new to add.")
                continue

            talk_history[talk_key] = True
            curse = random.choice(s["curses"]) if s["curses"] else ""

            if topic == "alibi":
                if sus == "marcus":
                    print(f"'You {curse}! Check the payphone log. I was talking to my mother in Serduz on Proxima B. It's not that complicated.'")
                    if "aiden_alibi" not in clues:
                        add_evidence("aiden_alibi")
                        trust_change("marcus", 1)
                elif sus == "napoleon":
                    print("'Wait, where is it? It's not in my pocket, but I swear, I was writing at that time. I even wrote the time I began. There's a napkin around here somewhere on it that proves my innocence, I promise you!'")
                    if "blake_alibi" not in clues:
                        add_evidence("blake_alibi")
                        trust_change("napoleon", 1)
                elif sus == "cleopatra":
                    print(f"'What, little ol' me? Well, my bus ticket clears me. Check it yourself. Hey, why not call the Transit Authority and confirm the ticket too?'")
                    if "alice_alibi" not in clues:
                        add_evidence("alice_alibi")
                        trust_change("cleopatra", 1)
                elif sus == "janitor":
                    print("'I was mopping the floor by the counter the whole time. I always do the bathrooms thrice a day; morning, after lunch rush, closing. Check the floor, see the sheen? Notice the wet floor sign. It’s still up.'")
                    if "luka_alibi" not in clues:
                        add_evidence("luka_alibi")
                        trust_change("janitor", 1)
                elif sus == "cook":
                    print("'I was prepping vegetables when the shit hit the fan. The stock bucket label is all time‑stamped. Please, take the label and check it out. Alice and I were chatting after she finished her call.'")
                    freezer_unlocked = True
                    print("She hands you the freezer key.")
                    if "adeline_timestamps" not in clues:
                        add_evidence("adeline_timestamps")
                        trust_change("cook", 1)
                elif sus == "patron":
                    print("'I’ve been sitting here all evening. The staff can confirm I never left this booth except to drain the old lead pipe.'")
                    if "hemlock_missing" not in clues:
                        add_evidence("hemlock_missing")
                        trust_change("patron", 1)
                elif sus == RESERVED_KEY_THX1138:
                    print(f"'Working. Office. Alone. Is that a crime?' *Muttering '{curse}' under breath. Syntharette twitching.")
            elif topic == "motive":
                if sus in MOTIVE_GOSSIP:
                    target, gossip_text, clue_id = MOTIVE_GOSSIP[sus]
                    print(f"{get_first_name(suspects[sus]['name'])} leans in: {gossip_text}")
                    if clue_id not in clues:
                        add_evidence(clue_id)
                    trust_change(sus, 1)
                else:
                    print(f"{get_first_name(suspects[sus]['name'])} stays silent on that topic.")
            elif topic == "the torn paper":
                print(f"{get_first_name(s['name'])} glances at the scrap. 'Mine. Obviously. I'm not sure what you expect to do with it, detective.'")
                if sus == RESERVED_KEY_THX1138:
                    print(f"They snatch it back before you can put it away. '{curse}!'")
                    trust_change(sus, -1)
                    if "torn thesis" in inventory:
                        inventory.remove("torn thesis")
            elif topic == "the revolver":
                if sus == RESERVED_KEY_THX1138:
                    print(f"For a moment, but just a moment, something flickers; their face an old neon sign on its last leg that hardly says anything completely. 'Never seen it before, detective.' The lie is obvious, but not why.")
                    trust_change(sus, -1)
            elif topic == "anything odd outside" and sus == "marcus":
                print("'I saw some tracks out the back porthole. They're too big to be mine, I know that. I know a lot of things. It's a curse sometimes.'")
                add_evidence("aiden_footprint")
                trust_change("marcus", 1)
            elif topic == "did you see anything" and sus == "napoleon":
                print("'I heard someone that was leaving the office after the bang. They had strong posture, I think, because of the sound the footsteps made.'")
                add_evidence("blake_witness")
                trust_change("napoleon", 1)
            elif topic == "the argument" and sus == "cleopatra":
                print(f"'I heard loud voices from the office. {suspects[RESERVED_KEY_THX1138]['name']} and Marsha. Nothing civil about it, but then, when are *they* ever civil? '")
                add_evidence("alice_witness")
                trust_change("cleopatra", 1)
            elif topic == "the floor" and sus == "janitor":
                print("'Someone walked towards the office with a determined stride. Strong, purposeful. Not a casual stroll.'")
                add_evidence("luka_swept")
                trust_change("janitor", 1)
            elif topic == "the office" and sus == "cook":
                print("'I heard a loud argument from the office. A woman’s voice, and someone responding calmly. Chilling.'")
                add_evidence("adeline_heard")
                trust_change("cook", 1)
            elif topic == "the noise" and sus == "patron":
                print("'There was yelling near the office. I couldn’t make out the words, but it was heated.'")
                add_evidence("hemlock_yelling")
                trust_change("patron", 1)
            elif topic == "Adeline's escape":
                if sus in ADELINE_ESCAPE_REACTIONS:
                    print(ADELINE_ESCAPE_REACTIONS[sus])
                else:
                    print("They don't seem to have anything to say about that.")
            elif topic.startswith("confront "):
                if sus in CONFRONT_DIALOGUE:
                    print(f"{get_first_name(suspects[sus]['name'])} stares at you: {CONFRONT_DIALOGUE[sus]}")
                    trust_change(sus, -1)
                else:
                    print("They just stare at you, unmoved.")

    # ---------- Threaten ----------
    def threaten(sus):
        if not sus:
            print("Who are you trying to intimidate?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match any suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("Exonerated. Even you aren't cruel enough to threaten them now.")
            return
        if not s["alive"] or s["defeated"]:
            print("Beyond intimidation. The void has already claimed that privilege.")
            return
        if s["detained"]:
            print("Cuffed. Threatening them now is just poor sportsmanship.")
            return
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print("Threatening the air. Bold. Ineffective.")
            return
        curse = random.choice(s["curses"]) if s["curses"] else ""

        success = random.random()
        if player_lean == "liberal" and "credits_wad" in inventory:
            success -= 0.25
        elif player_lean == "fascist":
            success += 0.15

        if success < 0.5:
            print(f"You invade {get_first_name(s['name'])}'s space. The tension rises and the pressure is on.")
            if trust[sus] == 0:
                print(f"{get_first_name(s['name'])} reacts violently. 'I don't have to listen to this!' They are now hostile.")
                s["hostile"] = True
                return
            if sus == "marcus":
                print(f"He cracks. 'Fine! I saw {suspects[RESERVED_KEY_THX1138]['name']} near the office right before the gunshot, you jerk! Now back off!! Please?!'")
                trust_change("marcus", 1)
            elif sus == "napoleon":
                if "bloody_cleaver" in clues:
                    print(f"He stammers, his eyes darting towards the kitchen. 'I saw Adeline threatening Marsha earlier! I swear! I was just writing!'")
                    if "luka_says_cook_threatened" not in clues:
                        add_evidence("luka_says_cook_threatened")
                    trust_change("napoleon", 1)
                else:
                    print(f"He flinches. 'The janitor! Elliot! He was acting all weird about Marsha's ring! I saw him hiding near the back!'")
                    if "luka_says_ring_was_planted" not in clues:
                        add_evidence("luka_says_ring_was_planted")
                    trust_change("napoleon", 1)
            elif sus == "cleopatra":
                if "bloody_cleaver" in clues:
                    print(f"She scoffs. 'Oh, please. You found the fry-cook's toy. She had no motive, just a landlord problem. If you're looking for malice, don't look at Adeline.'")
                    if "adeline_says_janitor_stole_ring" not in clues:
                        add_evidence("adeline_says_janitor_stole_ring")
                    trust_change("cleopatra", 1)
                else:
                    print(f"She laughs. 'You dare intimidate me?' Your ego dissolves. Trust completely evaporates.")
                    for s2 in suspects:
                        if s2 != sus:
                            trust_change(s2, -1)
            elif sus == "janitor":
                print(f"He stammers. 'Okay! Okay! I saw {suspects[RESERVED_KEY_THX1138]['name']} go into the office just before it happened. Please don't hurt me!'")
                trust_change("janitor", 1)
            elif sus == "cook":
                print("She stares through you. 'Threats? In my kitchen? You're either brave or stupid.' She doesn't break, but you see a flicker of fear.")
            elif sus == "patron":
                print("He chuckles. 'Son, I've been threatened by people twice your size and half your nerve. You'll need to do better.'")
            elif sus == RESERVED_KEY_THX1138:
                print(f"Their face hardens into something between complete disdain and total disregard. 'No proof, no case, no hope, detective.' They seem much more hostile now. Congratulations.")
                s["hostile"] = True
        else:
            print(f"Your threat falls flat. {get_first_name(s['name'])} laughs at you.")

    # ---------- Detain ----------
    def detain(sus):
        nonlocal handcuffs
        if not cheat_unlimited_cuffs and handcuffs <= 0:
            print("You reach for your cuffs and find no more.")
            return
        if not sus:
            print("Cuff whom?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been cleared. You'd be arresting an innocent person – wait, you've done that before.")
            return
        if not s["alive"] or s["defeated"] or s["detained"]:
            print("You've already detained this one. Another set of cuffs would be redundant, don't you think?")
            return
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print("They're not in here and ain't telekinetic. Not yet, anyway.")
            return
        if not cheat_unlimited_cuffs:
            handcuffs -= 1
        s["detained"] = True
        remaining = "∞" if cheat_unlimited_cuffs else handcuffs
        print(f"Click-click-click-click. {get_first_name(s['name'])} now sports a used set of state-issued jewelry. {remaining} remaining.")
        if sfx_queue: sfx_queue.put('cuffs')

    # ---------- Fight ----------
    def fight(sus):
        if not sus:
            print("Fight who? The existential void?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been exonerated. Even you have standards.")
            return
        if not s["alive"] or s["defeated"]:
            print("Already on the floor. Kicking them now is excessive.")
            return
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print("Shadowboxing. Very existential. Very pointless.")
            return
            
        if s["detained"]:
            print("You raise your weapon against a restrained suspect. They cannot fight back. It takes two hits.")
            print(f"{get_first_name(s['name'])} is dead. This is a cold-blooded execution.")
            s["hp"] = 0
            s["defeated"] = True
            check_total_carnage()
            return

        curse = random.choice(s["curses"]) if s["curses"] else ""
        print(f"\n{RED}⚔ The air is electric. You and {get_first_name(s['name'])} circle the area like binary stars on a collision course. There may yet be another murder. At least it'll be easy to solve.{RESET}")
        if sfx_queue: sfx_queue.put('fight')
        while player["hp"] > 0 and s["hp"] > 0:
            if cheat_god_mode:
                player["hp"] = player["max_hp"]
            print(f"\nYour HP: {player['hp']}/{player['max_hp']} | {get_first_name(s['name'])} HP: {s['hp']}")
            print("1. Calculated strike  2. Desperate swing  3. Tactical retreat")
            act = input("> ").strip()
            if act == "3":
                print("Discretion is the most fundamental component of not dying. You retreat, hoping they forgive this trespass.")
                return
            elif act == "1":
                dmg = int(round(player["base_damage"]))
                s["hp"] -= dmg
                print(f"Clean hit. {dmg} damage. Good work.")
                if sfx_queue: sfx_queue.put('hit')
            elif act == "2":
                roll = random.random()
                if roll < player["special_hit_chance"]:
                    dmg_float = player["base_damage"] * 1.25
                    dmg = int(round(dmg_float))
                    s["hp"] -= dmg
                    print(f"Lucky break, detective. You land a devastating blow! {dmg} damage.")
                    if sfx_queue: sfx_queue.put('hit')
                elif roll < player["special_hit_chance"] + player["regular_hit_chance"]:
                    dmg = int(round(player["base_damage"]))
                    s["hp"] -= dmg
                    print(f"Wild-eyed, but effective. Be careful, detective. {dmg} damage.")
                    if sfx_queue: sfx_queue.put('hit')
                else:
                    print("Your swing goes wide! No damage.")
                    if sfx_queue: sfx_queue.put('miss')
            else:
                print("Indecision could cost your life. No damage.")
            if s["hp"] <= 0:
                s["hp"] = 0
                s["defeated"] = True
                print(f"{get_first_name(s['name'])} collapses, eyes rolled back and lips muttering '{curse}' before their animus fades.")
                check_total_carnage()
                return
            edmg = random.randint(3, 6)
            if cheat_god_mode:
                edmg = 0
            player["hp"] -= edmg
            print(f"{get_first_name(s['name'])} strikes back. {edmg} damage. You see murder in their eyes.")
            if player["hp"] <= 0:
                player["hp"] = 0
                print("Darkness rolls over you. The void encompasses your vision bit by bit. Somewhere, a jukebox plays your funeral dirge, and no one realizes it. Game over, detective.")
                if sfx_queue: sfx_queue.put('gameover')
                sys.exit(0)

    def check_total_carnage():
        if all(suspects[k]["defeated"] for k in suspects):
            ending_carnage()

    # ---------- Tamper / Plant ----------
    def tamper(item, suspect=None):
        nonlocal corruption_planted, tainted_evidence
        ev_id = EVIDENCE_ALIASES.get(item.lower())
        if ev_id is None:
            if item in EVIDENCE_DESCRIPTIONS:
                ev_id = item
        if isinstance(ev_id, list):
            found = next((eid for eid in ev_id if eid in clues), None)
            if found is None:
                found = ev_id[0]
            ev_id = found
        if ev_id is None or ev_id not in TAMPER_ACTIONS:
            print("That item can't be tampered with.")
            return
        action_type, msg = TAMPER_ACTIONS[ev_id]
        if action_type == "destroy":
            if ev_id in clues:
                remove_evidence(ev_id)
            else:
                print("You don't have that evidence.")
                return
            print(msg)
        elif action_type == "plant":
            if not suspect:
                print("You need to specify a suspect to plant on. Use 'tamper revolver for Alice'")
                return
            resolved = resolve_suspect(suspect)
            if not resolved:
                print("Invalid suspect.")
                return
                
            if resolved == RESERVED_KEY_THX1138:
                current_hits = len(clues.intersection(incriminating))
                if current_hits >= required_incriminating:
                    print("The evidence is already sufficient. This won't change anything.")
                else:
                    print("You plant the evidence. It provides the missing link.")
                    tainted_evidence = True
                    clues.add(ev_id)
            else:
                corruption_planted = resolved
                print(msg.format(suspect=get_first_name(suspects[resolved]['name'])))

            if ev_id == "unknown_revolver" and "revolver" in inventory:
                inventory.remove("revolver")
            elif ev_id == "bullet_casing" and "bullet_casing" not in inventory:
                print("You don't have the bullet casing.")
                return
            elif ev_id == "bloody_cleaver" and "bloody_cleaver" not in inventory:
                print("You don't have the cleaver.")
                return
                
    # ---------- Accuse ----------
    def accuse(sus):
        nonlocal handcuffs, corruption_planted, tainted_evidence
        if not sus:
            print("Accuse who? Make up your mind, detective.")
            return
        if sus.startswith("tamper "):
            parts = sus[7:].split(" for ")
            if len(parts) == 2 and parts[1].strip():
                tamper(parts[0].strip(), parts[1].strip())
            else:
                tamper(parts[0].strip())
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match anyone. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        if sfx_queue: sfx_queue.put('accuse')

        if sus != RESERVED_KEY_THX1138 and trust[sus] >= 3:
            print(f"{get_first_name(suspects[sus]['name'])} stares at you in disbelief. 'This is a pure betrayal!'")
            suspects[sus]["hostile"] = True

        if sus == "cook" and not suspects["cook"]["exonerated"] and not suspects["cook"]["detained"] and not suspects["cook"]["defeated"]:
            ending_escape()
            return
        if nyx_escaped and corruption_planted and sus == corruption_planted:
            corruption_ending()
            return
        if sus != RESERVED_KEY_THX1138 and suspects[RESERVED_KEY_THX1138]["detained"]:
            secret_ending()
            return
        if sus != RESERVED_KEY_THX1138:
            ending_fail()
            return
        if len(clues.intersection(incriminating)) < required_incriminating:
            print(f"{get_first_name(suspects[RESERVED_KEY_THX1138]['name'])} smirks. 'Let's say I did. Who in Existence would believe you? You've got nothing on me.'")
            return
        if suspects[RESERVED_KEY_THX1138]["detained"]:
            if tainted_evidence:
                ending_correct_tainted()
            else:
                ending_correct()
            return
            
        print(f"\nYou point at {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}. 'You.' The word hangs like a bullet; slipping behind their eyes and through their mental folds as the realization dawns on them. You're pointing at them, and you're not backing down.")
        print(f"You both notice at the same time: they're unrestrained. '{player_name}, you absolute fool!' They lunge.")
        fight(RESERVED_KEY_THX1138)
        if suspects[RESERVED_KEY_THX1138]["defeated"] and not suspects[RESERVED_KEY_THX1138]["detained"]:
            if cheat_unlimited_cuffs or handcuffs > 0:
                if not cheat_unlimited_cuffs:
                    handcuffs -= 1
                suspects[RESERVED_KEY_THX1138]["detained"] = True
                rem = "∞" if cheat_unlimited_cuffs else handcuffs
                print(f"You slap the cuffs on {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}. {rem} remaining. Justice never tasted so bloody and sweet. Good job, detective. They're sure to tell stories of this one at the station.")
            else:
                print("You don't have any cuffs left, but they're out cold. The police drone will handle it. Probably. You light a smoke and watch over them making sure they're still breathing ready to issue another state-sanctioned beat-down if necessary.")
            if tainted_evidence:
                ending_correct_tainted()
            else:
                ending_correct()
        elif suspects[RESERVED_KEY_THX1138]["defeated"] and suspects[RESERVED_KEY_THX1138]["detained"]:
            if tainted_evidence:
                ending_correct_tainted()
            else:
                ending_correct()
        else:
            ending_fail()

    # ---------- Endings ----------
    def secret_ending():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print(f"\nWrong accusation. You made the wrong bet. Very wrong.")
        print(f"Behind you: a soft click. You spin. {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}, one wrist free, working on the other.")
        print(f"'Did you really think these standard restraints could hold me?' They smile. The predator turns prey, but it dawns on you they're damn good at being either.")
        print(f"'Entertaining, {player_name}. Truly. But I have a schedule to keep, and you have a new problem to explain.'")
        print("They're gone before you can move. The airlock cycles. Moments later the police drone arrives to an empty office and a restaurant full of fools. Too bad, detective. They'll definitely tell this story although you'd certainly wish they wouldn't.")
        print(f"\n{RED}GAME OVER – SECRET ENDING{RESET}")
        game_over = True
        sys.exit(0)

    def nyx_escape_ending():
        nonlocal nyx_escaped
        print("Nyx parts their lips once more to reveal their toxic solvent-based smile. Their eyes flash the recognition that's only ever shared between two predators in league with each other. You immediately begin to consider how you'll spin this to the police drone. But perhaps there's another way...")
        nyx_escaped = True
        suspects[RESERVED_KEY_THX1138]["alive"] = False
        suspects[RESERVED_KEY_THX1138]["exonerated"] = False
        print("Nyx vanishes through the back office. The airlock cycles. You're alone with the mess and a choice.")
        print("You can plant the revolver on someone and accuse them to close the case. Dirty, but effective.")

    def corruption_ending():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('victory')
        item_name = "unknown"
        if corruption_planted:
            if "revolver" not in inventory and "bloody_cleaver" not in inventory:
                item_name = "revolver"
            else:
                item_name = "evidence"
        print(f"You plant the {item_name} and make your accusation. The frame holds. The police drone accepts your report without question.")
        print("A dirty cop ending. Justice is served cold, and you're the one holding the freezer door open.")
        print(f"{RED}GAME OVER – CORRUPTION ENDING{RESET}")
        game_over = True
        sys.exit(0)

    def ending_escape():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print("Adeline's eyes widen. 'You think it was me? No, no, no...' She bolts for the back door!")
        print("She escapes into the void before you can react. The case just got harder.")
        print(f"{RED}GAME OVER – ESCAPE ENDING{RESET}")
        game_over = True
        sys.exit(0)

    def ending_correct():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('victory')
        k = suspects[RESERVED_KEY_THX1138]
        print(f"\n{RED}Everything clicks into place. The whole crooked design.{RESET}")
        print(f"'{get_first_name(k['name'])}, in the office, with the revolver. Marsha Stone killed in cold blood. For ego? For fun? For the oldest reason there ever was: because you could.'")
        print(f"{get_first_name(k['name'])} deflates like a punctured air mattress under the crushing weight of the fat man known as consequences. 'Yes, you meddling {random.choice(k['curses'])}. Fine! I did it. And I'd do it again. I'd do it all again without a second god-damned thought.'")
        print("The confession hangs in the air, hideous and undeniable. You make your notes.")
        for sus in suspects:
            if sus == RESERVED_KEY_THX1138: continue
            s = suspects[sus]
            if s["alive"] and not s["defeated"] and not s["exonerated"]:
                curse = random.choice(s["curses"]) if s["curses"] else "sprocket-head"
                print(f"{get_first_name(s['name'])} stares. 'Them? All along? That...makes sense...'")
        print("\nMoments later, the police drone docks with a hydraulic hiss. Justice arrives on autopilot, but it lands, as it is wont to do, in your hands. Good job, detective. You're sure to get a bonus for this one.\n")
        if suspects[RESERVED_KEY_THX1138]["detained"]:
            print(f"You watch as the drone hooks their cuffs, generates an ionic iso-field around their unconscious body, and takes off to the station only a nano-parsec away, give or take. You feel a sense of fullness in your heart, and it's not cholesterol. Good, job, {player_name}.")
        else:
            print(f"You watch as the drone explores a bit looking for the regulation attachment and finding nothing. It instead spouts forth a telescoping flexible tentacle that wraps around their wrist. It generates an ionic iso-field around their unconscious body, and takes off to the station only a nano-parsec away, give or take. You feel a sense of fullness in your heart, and it's not cholesterol. Good, job, {player_name}.")
        print(f"\n{RED}Game Over.{RESET}")
        game_over = True
        sys.exit(0)

    def ending_correct_tainted():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('victory')
        k = suspects[RESERVED_KEY_THX1138]
        print(f"\n{RED}You force the pieces to fit.{RESET}")
        print(f"You point at {get_first_name(k['name'])}. 'You.'")
        print(f"{get_first_name(k['name'])} sneers. 'You've got nothing, detective.'")
        print("You present the evidence. It's enough. Barely. The police drone accepts your report.")
        print("The conviction holds. For now.")
        print("\nWeeks later, the appeal goes through. The fabricated evidence is discovered. The conviction is vacated. You are stripped of your license, facing charges of evidence tampering.")
        print(f"But {get_first_name(k['name'])} is off the streets. The crooked design is broken, even if you broke yourself doing it.")
        print(f"\n{RED}GAME OVER – TAINTED ENDING{RESET}")
        game_over = True
        sys.exit(0)

    def ending_fail():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        k = suspects[RESERVED_KEY_THX1138]
        print("\nYour accusation shatters against the truth like glass against bulkhead.")
        print(f"{get_first_name(k['name'])} has no skeletons in their closet, at least none that are people. 'Poor {player_name}. So close. Yet so... not.'")
        print("The killer's out the back before the drone docks. By the time authorities arrive: you're trembling with frustration, confusion, and shame.")
        for sus in suspects:
            if sus != RESERVED_KEY_THX1138:
                s = suspects[sus]
                if s["alive"] and not s["defeated"] and not s["exonerated"]:
                    print(f"{get_first_name(s['name'])} shakes their head. This failure has left them feeling betrayed and more importantly, to you anyway, disappointed.")
        print(f"The drone files its report. Somewhere in a distant solar system, it moves across the desk of your superiors, and with that your reputation shrinks further. You're sure to catch hell for this one, {player_name}.\n")
        print(f"{RED}GAME OVER{RESET}")
        game_over = True
        sys.exit(0)

    def ending_carnage():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print("You look back across the bar. Everyone's dead. Dead folk tell no tales, but there's sure to be plenty living who watch your live-streamed execution. The detective who went completely mad and committed mass murder. Good job, I guess, detective. Maybe you'll solve a case in the next life.\n\nGAME OVER")
        game_over = True
        sys.exit(0)

    # ---------- Countenance ----------
    def countenance():
        nonlocal countenance_used, handcuffs, required_incriminating
        if not cheat_infinite_countenance and countenance_used:
            print("You've already called upon your Countenance. The moment has passed.")
            return
        countenance_used = True

        if player_lean == "liberal":
            if "credits_wad" not in inventory:
                print("You reach for your credits, but your pockets are empty. The Countenance fizzles.")
                return
            print("You flash a fat stack of credits. The bribe is tempting, and the target takes it.")
        elif player_lean == "fascist":
            print("You stand at attention and invoke the State's authority. Your threats are now far more intimidating.")
        elif player_lean == "communist":
            handcuffs += 1
            print("You speak into your cufflinks, whether anyone notices or not is immaterial. A commissar materialises from the ventilation shaft, slaps a fresh pair of cuffs into your palm, and vanishes. This is sure to be useful. (+1 cuffs)")
        elif player_lean == "anarchist":
            sus_keys = locations[current_location].get("suspects", [])
            target_sus = None
            for key in sus_keys:
                if not suspects[key]["exonerated"] and not suspects[key]["defeated"]:
                    target_sus = key
                    break
            if not target_sus:
                print("Nobody here to spread the message to. The Countenance fizzles.")
                return
            s = suspects[target_sus]
            name = get_first_name(s['name'])
            print(f"You scrawl a simple message on a napkin. 'All property is theft' and hand it to {name}.")
            if s["lean"] == "anarchist":
                trust_change(target_sus, 2)
            elif s["lean"] == "communist":
                trust_change(target_sus, 1)
            else:
                if trust[target_sus] == 0:
                    if s["lean"] == "fascist":
                        print(f"{name} tears the napkin up. 'How dare you!' They are now hostile.")
                        s["hostile"] = True
                    else:
                        print(f"{name} ignores you. They already don't trust you.")
                else:
                    trust_change(target_sus, -2)
        else:
            print("Your Countenance manifests in an unexpected way. Nothing happens.")
        if cheat_infinite_countenance:
            countenance_used = False

    # ---------- Inventory ----------
    def show_inventory():
        ev_list = '\n'.join(f' - {evidence_display_name(e)}' for e in sorted(clues)) if clues else "You've got nothing. The void stares back. Don't blink."
        print(f"Inventory: {', '.join(inventory) if inventory else 'empty pockets'}\nCuffs: {handcuffs}/3\nHP: {player['hp']}/{player['max_hp']}\n\nEvidence ({len(clues)}/{TOTAL_NON_MISLEADING}):\n{ev_list}")

    # ---------- Theory Command ----------
    def theory(sus):
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print("Unknown suspect for theory.")
            return
        
        s = suspects[sus]
        name = get_first_name(s['name'])
        
        alibi_map = {
            "marcus": "aiden_alibi",
            "napoleon": "blake_alibi",
            "cleopatra": "alice_alibi",
            "janitor": "luka_alibi",
            "cook": "adeline_timestamps",
            "patron": "hemlock_missing",
            RESERVED_KEY_THX1138: None
        }

        print(f"\n{RED}THEORY SCRATCHPAD: {name}{RESET}")
        print(f"Known motives: {s['motive']}")

        while True:
            print("\nSelect evidence to evaluate:")
            available_evidence = sorted(list(clues))
            
            if not available_evidence:
                print("You have no evidence to evaluate.")
                break
                
            for i, ev_id in enumerate(available_evidence, 1):
                print(f"{i}. {evidence_display_name(ev_id)}")
            print("0. Exit theory board")

            choice = input("> ").strip()
            if choice == "0":
                break
            if not choice.isdigit() or not (1 <= int(choice) <= len(available_evidence)):
                print("Invalid selection.")
                continue

            ev_id = available_evidence[int(choice)-1]
            impl, exon = EVIDENCE_IMPLICATION.get(ev_id, ([], []))

            implicates_sus = any(imp.lower() in s['name'].lower() for imp in impl) or (sus == case.killer_key and "Unknown" in impl)
            exonerates_sus = any(ex.lower() in s['name'].lower() for ex in exon)

            if implicates_sus:
                print(f"• {evidence_display_name(ev_id)} -> DECISIVE: This connects strongly to {name}.")
            elif exonerates_sus:
                print(f"• {evidence_display_name(ev_id)} -> CONTRADICTS: This points away from {name}.")
            else:
                print(f"• {evidence_display_name(ev_id)} -> CONSISTENT: This doesn't rule {name} in or out.")

            if alibi_map.get(sus) == ev_id:
                print("(Note: Alibis can be faked or misinterpreted. This alone is not proof.)")

        print(f"\nYou close the file on {name}. The pieces don't form a complete picture yet.")

    # ---------- Shortcuts & Command Parsing ----------
    EASTER_EGG_PHRASE = "Im an existentialist-absurdist-gnostic-agnostic-secular-true path unitarian-marxist-leninist-maoist multi-level marketer."

    shortcuts = {
        'g': 'go', 'l': 'look', 's': 'search', 'e': 'examine', 't': 'talk',
        'th': 'threaten', 'd': 'detain', 'f': 'fight', 'a': 'accuse',
        'i': 'inventory', 'inv': 'inventory', 'h': 'help', '?': 'help',
        'q': 'quit', 'x': 'examine', 'c': 'countenance',
        'v': 'theory', 'tamper': 'tamper', 'n': 'notepad'
    }

    def expand_command(raw):
        raw = raw.strip()
        if not raw:
            return None
        if raw.lower() == EASTER_EGG_PHRASE.lower():
            print("You realize once today is over, tomorrow will never come. Red will fade to black, and you will wake up in another reality, as another person, and this experience may never truly grow roots and flourish in your psyche. You will simply move onto the next life.")
            return None
        parts = raw.split()
        first = parts[0].lower()
        if first in ("notepad", "notes", "notebook"):
            return "notepad"
        if first in shortcuts:
            shortcut = shortcuts[first]
            if shortcut == 'go':
                return f"go {' '.join(parts[1:])}" if len(parts) > 1 else "go"
            elif shortcut == 'talk':
                return f"talk {' '.join(parts[1:])}" if len(parts) > 1 else "talk"
            elif shortcut == 'threaten':
                return f"threaten {' '.join(parts[1:])}" if len(parts) > 1 else "threaten"
            elif shortcut == 'detain':
                return f"detain {' '.join(parts[1:])}" if len(parts) > 1 else "detain"
            elif shortcut == 'fight':
                return f"fight {' '.join(parts[1:])}" if len(parts) > 1 else "fight"
            elif shortcut == 'accuse':
                return f"accuse {' '.join(parts[1:])}" if len(parts) > 1 else "accuse"
            elif shortcut == 'examine':
                return f"examine {' '.join(parts[1:])}" if len(parts) > 1 else "examine"
            elif shortcut == 'look':
                return "look"
            elif shortcut == 'search':
                return "search"
            elif shortcut == 'inventory':
                return "inventory"
            elif shortcut == 'help':
                return "help"
            elif shortcut == 'quit':
                return "quit"
            elif shortcut == 'countenance':
                return "countenance"
            elif shortcut == 'notepad':
                return "notepad"
            elif shortcut == 'theory':
                return f"theory {' '.join(parts[1:])}" if len(parts) > 1 else "theory"
            elif shortcut == 'tamper':
                return f"tamper {' '.join(parts[1:])}" if len(parts) > 1 else "tamper"
        return raw

    # ---------- Help Text ----------
    def help_text():
        print("""
╔══════════════════════════════════════════════════╗
║                 RED AFFAIR: CASE FILES           ║
╠══════════════════════════════════════════════════╣
║ A body cools in the back room. Time drips like   ║
║ stale coffee. Your wits are your weapon.         ║
║                                                  ║
║ Movement:                                        ║
║   GO <place>   (g) – move to a room (counter,    ║
║                      dining, kitchen, office,    ║
║                      bathroom, freezer)          ║
║   LOOK         (l) – examine your surroundings   ║
║                                                  ║
║ Investigation:                                   ║
║   SEARCH       (s) – find hidden clues           ║
║   EXAMINE <obj>(e/x)– inspect an item or clue    ║
║   TAKE <item>       – pick up an object          ║
║   TALK <suspect>(t) – question a patron          ║
║   THREATEN <suspect> (th) – apply pressure       ║
║   THEORY <suspect> (v) – review what you know    ║
║   NOTEPAD     (n) – review collected evidence    ║
║     (also notes, notebook)                       ║
║                                                  ║
║ Action:                                          ║
║   DETAIN <suspect> (d) – handcuff (3 pairs)      ║
║   FIGHT <suspect> (f)  – resort to violence      ║
║   ACCUSE <suspect> (a) – name the killer         ║
║   TAMPER <item> for <suspect> – plant evidence    ║
║   TAMPER <item>          – destroy evidence      ║
║                                                  ║
║ General:                                         ║
║   INVENTORY    (i)  – check pockets and evidence ║
║   COUNTENANCE  (c)  – use your political ability ║
║   HELP         (h/?)– this list                 ║
║   QUIT         (q)  – abandon the case           ║
║                                                  ║
║ Suspects: Aiden, Blake, Alice, Nyx,              ║
║           Elliot, Adeline, Alexander              ║
╚══════════════════════════════════════════════════╝""")

    # ---------- Game Loop ----------
    clear_screen()
    hud()
    describe_location()
    while not game_over:
        hud()
        raw = input(f"{RED}> {RESET}").strip()
        if not raw:
            continue
        expanded = expand_command(raw)
        if not expanded:
            continue
        parts = expanded.split()
        verb = parts[0]
        noun = " ".join(parts[1:]) if len(parts) > 1 else ""

        if verb == "go":
            move(noun)
        elif verb == "look":
            clear_screen()
            hud()
            describe_location()
        elif verb == "search":
            search()
        elif verb == "examine":
            examine(noun)
        elif verb == "take":
            take(noun)
        elif verb == "talk":
            talk(noun)
        elif verb == "threaten":
            threaten(noun)
        elif verb == "detain":
            detain(noun)
        elif verb == "fight":
            fight(noun)
        elif verb == "accuse":
            accuse(noun)
        elif verb == "countenance":
            countenance()
        elif verb == "inventory":
            show_inventory()
        elif verb == "help":
            help_text()
        elif verb == "quit":
            print("You step back through the airlock. For now, the case remains unsolved; one day going cold. The stars don't care. Neither do you.")
            sys.exit(0)
        elif verb in ("notepad", "notes", "notebook"):
            show_notepad()
        elif verb == "theory":
            theory(noun)
        elif verb == "tamper":
            accuse(f"tamper {noun}")
        else:
            print("Unrecognized command. This must be your first homicide detail. Type 'help' or 'h' for assistance.")

if __name__ == "__main__":
    play_game()
