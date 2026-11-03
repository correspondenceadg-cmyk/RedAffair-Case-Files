import random

def get_classic_data():
    RESERVED_KEY_THX1138 = "thatcher"

    suspect_descriptions = {
        "marcus": (
            "Aiden Adams slumps against the cash register like any employee who's realized the universe hates him, his boss tolerates him, and his mother only may have liked him. His beard is the kind that's seen everything in the perpetual nightlife scene that lures in honeys, hicks, hacks, hackers, and horrors– mostly horrors. He wears a diner uniform standard: black button-up, black pants, red tie, that way you never see it stained with what might be coffee or might be the remnants of a collapsed college student. His eyes are deep wells of calm resignation, the kind you develop when you've watched people die, or maybe even the kind you develop when you're why people die. A syntharette sits crooked behind his ear, and one glows between his lips, because even in space, some men can't let go of their addictions."
        ),
        "napoleon": (
            'Bladovich "Blake" Jughashvili occupies a booth like he\'s planning a wedding alone, and he intends to crash it. ''Heart of Gold, Head of Lead'', reads a sententia in obscure Na-Min lettering emblazoned across his neck from behind and under his ear down towards his chin. He\'s buff, but still shorter than you\'d expect, shorter than he\'d like, and shorter than he would willingly admit. The pompadour adds a few inches to his height, but not his dignity. His hands are on the table, shaking like someone who\'s completely innocent, and scared out of their wits; maybe someone who\'s guilty, and just wasn\'t cut out for murder and secret keeping. The napkins scattered around him are covered in various bodily fluids, all from his face. For what? Nobody knows. Probably not even him.'
        ),
        "cleopatra": (
            "Alice Oliverae stands by the back door with the bearing of a woman who's met every goal she laid out in life and found them wanting. Her kohl-rimmed eyes and obsidian rimmed glasses have witnessed the fall of rivals and the rise of ever disappointing replacements. Gold bangles clink on her wrists with every gesture, her outfit is outlandish but somehow still tame. Gold, makeup, and two pins in long stockings made up with gold thread that just doesn't end. She doesn't occupy space so much as allow it the remarkable privilege of containing her."
        ),
        "thatcher": (
            "Nyx Singénero lounges about the back office like they've already been cleared by the investigation. Their posture is a monument to the conviction that they are right and you are merely an inconvenience. The synthjade and anodized chain around their neck catches the flickering white-washed light and glares in tandem with Nyx right at you with what feels like spite, but may be mild annoyance. Their hair is an auburn tinted burgundy, pulled into a bun and held in place with chopsticks placed with unwavering certainty. When they speak, their voice has the texture of gravel being crushed into smaller, more compliant gravel. They smell like an ashtray and sound like every smoke they've ever had left enough tar behind to preserve the mesozoic.  There's something in their eyes – not warmth, exactly, but the cold fusion of absolute conviction. Their feet are on their desk at the end of two crossed legs, but they don't seem to be waiting for you to speak. They seem to already know what you're going to say. Maybe they just know everything."
        ),
        "janitor": "Elliot Luka sweeps the floor with the resigned air of a man who knows that Sisyphus is content, if only because he is Sisyphus. His stained speedsuit and calloused hands speak of endless circuits against invasive pathogens, pests, and careless spills. He rarely speaks, but his eyes flick toward every sound. He's squirrelly, yet composed enough that most wouldn't notice. You do.",
        "cook": "Adeline Malovega stands over the carbon steel griddle, eyes locked a thousand miles through the cook-top beyond the floor. The murder has shut down her kitchen and, apparently, her mind. Tattoos flow around her forearms past her biceps into unique sleeves, the true meaning of which only she would know. Her hair is up in a bun with a hairnet wrapped around her brow and lips that twitch as she breaks her catatonia to notice you.",
        "patron": "Alexander Hemlock sits in the corner booth, a cup of cold black coffee before him. His hands tremble, but his eyes are sharp – possibly nerves, possibly a neurodisease. He’s been here since before the murder, and the staff treat him like furniture; not a beautiful armoire, but a living‑room coffee table that’s never seen a coaster and is as replaceable as it is functional."
    }

    suspects = {
        "marcus": {
            "name": "Aiden Adams",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Personal differences about the appropriate use of power – the kind that end in firings, perhaps even body bags.",
            "guilty": False,
            "characteristics": ["stoic", "bearded", "calm", "philosophical"],
            "curses": ["chem-sucker", "sinkhook", "fucking pig", "federal gangster", "murder jockey"],
            "exonerated": False
        },
        "napoleon": {
            "name": 'Bladovich "Blake" Jughashvili',
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Turns out they used to date, maybe it was a bad breakup, maybe the kind that leaves blood on the cutting room floor.",
            "guilty": False,
            "characteristics": ["short", "intense", "militaristic", "ambitious"],
            "curses": ["synthrot", "neural-plushie", "prescription grade fool", "leakskull", "spiritual hernia"],
            "exonerated": False
        },
        "cleopatra": {
            "name": "Alice Oliverae",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Breakdowns in business negotiations, making 'hostile takeover' mean exactly what it sounds like.",
            "guilty": False,
            "characteristics": ["regal", "serpentine", "charismatic", "patient"],
            "curses": ["joy thief", "state ghoul", "cashcop", "moonboot-licker", "chitterlings egg"],
            "exonerated": False
        },
        RESERVED_KEY_THX1138: {
            "name": "Nyx Singénero",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "She stood up for herself against Nyx's bullying. Sometimes putting your foot down brings the rest of you along for at least six feet more.",
            "guilty": True,
            "characteristics": ["detached", "strong", "unusual", "calculating"],
            "curses": ["state sponsored thug", "gas-cow", "auctioneer of justice", "unbelievably fucking stupid asshole", "viscera venture capitalist"],
            "exonerated": False
        },
        "janitor": {
            "name": "Elliot Luka",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "The victim accused him of stealing a valuable ring. He was written up, his pay docked, and spent his next several days searching for it, even on his day off, even after everyone assumed he was merely pretending to look.",
            "guilty": False,
            "characteristics": ["quiet", "observant", "nervous", "diligent"],
            "curses": ["cheese dick", "pig bitch", "evolved yeast infection", "bureaucratic non-entity", "nosey fucking freak"],
            "exonerated": False
        },
        "cook": {
            "name": "Adeline Malovega",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "The victim was her landlord, often demanding rent when she ate, sometimes three weeks in a row. Some people just can't stand a leech. Can you relate?",
            "guilty": False,
            "characteristics": ["reliable", "frenetic", "avoidant", "unpredictable"],
            "curses": ["Mr. Jerk", "death-jockey", "short-order disappointment", "needle-dick double bitch", "space-pig"],
            "exonerated": False
        },
        "patron": {
            "name": "Alexander Hemlock",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "He has none, but his whereabouts are unaccounted for by anyone else but him. He claims to have used the bathroom just before the incident, but others claim they didn't see him actually walk that direction, but instead out the front door.",
            "guilty": False,
            "characteristics": ["forgetful", "blasé", "lonely", "old-fashioned"],
            "curses": ["pussywillow", "cuck", "achey half-dead punk", "idiot child", "gun sucking piss sniffing shitheel"],
            "exonerated": False
        }
    }

    suspect_aliases = {
        "marcus": "marcus",
        "aiden": "marcus",
        "adams": "marcus",
        "aiden adams": "marcus",
        "napoleon": "napoleon",
        "bladovich": "napoleon",
        "blake": "napoleon",
        "jughashvili": "napoleon",
        "blake jughashvili": "napoleon",
        "bladovich jughashvili": "napoleon",
        "cleopatra": "cleopatra",
        "alice": "cleopatra",
        "oliverae": "cleopatra",
        "alice oliverae": "cleopatra",
        RESERVED_KEY_THX1138: RESERVED_KEY_THX1138,
        "nyx": RESERVED_KEY_THX1138,
        "singénero": RESERVED_KEY_THX1138,
        "nyx singénero": RESERVED_KEY_THX1138,
        "elliot": "janitor",
        "luka": "janitor",
        "elliot luka": "janitor",
        "adeline": "cook",
        "malovega": "cook",
        "adeline malovega": "cook",
        "alex": "patron",
        "alexander": "patron",
        "hemlock": "patron",
        "alexander hemlock": "patron",
    }

    revealed_characteristic = {
        "marcus": "detached",
        "napoleon": "strong",
        "cleopatra": "unusual",
        "janitor": "calculating",
        "cook": "frenetic",
        "patron": "unusual",
        RESERVED_KEY_THX1138: None
    }

    locations = {
        "counter": {
            "desc": (
                "THE COUNTER – A scratched carbonite slab that's seen more elbows than a gala dance floor with Fred Astaire and Bob Fosse. The cash register is smashed open, PCB, chits, change, and Valerian Draughma spilled across the floor like so many things have been over the years, leaving a sticky film beneath your shoes. The entrance is sealed with a field of plasma that hums something like a funeral dirge. Maybe you're imagining that last bit, but visually, audibly, and tactically if you must, you do know the field is there.\n\n"
                + suspect_descriptions["marcus"] + "\n\n" + suspect_descriptions["janitor"]
            ),
            "items": [],
            "suspects": ["marcus", "janitor"],
            "searchable": ["aiden_alibi", "luka_alibi"]
        },
        "dining": {
            "desc": (
                "THE DINING AREA – Booths line the walls placed in opposition with a white table between them, and the walls undecorated except for the art deco murals that fill the otherwise unremarkable space; one to each wall. Upholstered in synthleather and what was once blue vinyl, they are now faded and cracking across every surface except one patch now the color of dried blood and what was once, presumably, someone's personality. Napkins, sauce, seasoning, and marmalade are strewn across one tabletop, the rest being various gradations of clean, none of which seem hygienic. The jukebox is stuck on a single song – an avant garde noise album, now academically classical hundreds of years later and light-years away, but it vibrates your fillings.\n\n"
                + suspect_descriptions["napoleon"] + "\n\n" + suspect_descriptions["patron"]
            ),
            "items": [],
            "suspects": ["napoleon", "patron"],
            "searchable": ["blake_alibi", "hemlock_missing"],
            "hidden_revolver": True
        },
        "kitchen": {
            "desc": (
                "THE KITCHEN – Stainless steel griddles that haven't been stainless since the most recent Big Bang. A food can full of what's either canned food or cleaning solvents sits atop the griddle. The back door is hermetically sealed, its porthole showing nothing but the indifferent void. Every kitchen has its secrets, but you feel something extra weighing down the ether in this one. You intend to find what it is, whatever it takes, and whoever's responsible.\n\n"
                + suspect_descriptions["cleopatra"] + "\n\n" + suspect_descriptions["cook"] +
                "\nA corkboard hangs beside the back door, pinned with old schedules, a faded menu, and a flier."
            ),
            "items": ["candlestick", "label"],
            "suspects": ["cleopatra", "cook"],
            "searchable": ["alice_alibi", "adeline_timestamps"],
            "examinables": ["corkboard", "freezer"]
        },
        "office": {
            "desc": (
                "THE BACK OFFICE – A cramped drywall cage full of stale smoke and broken promises of raises, promotions, and staff openings. "
                "A torn sheet of paper flutters near the desk.\n\n"
                + suspect_descriptions[RESERVED_KEY_THX1138]
            ),
            "items": ["poison vial", "ring_or_id"],
            "suspects": [RESERVED_KEY_THX1138],
            "searchable": ["nyx_message"],
            "body_examinable": False,
            "bullet_found": False
        },
        "bathroom": {
            "desc": (
                "THE BATHROOM – A cramped, flicker-lit cubicle. The air smells of cheap disinfectant and stale regret. "
                "The victim lies here. She’s propped against the wall like someone sat her down for a chat she’ll never finish. "
                "A single gunshot wound to the temple – neat, professional, almost polite. "
                "Blood has pooled in the cracks of a linoleum floor that screamed despair long before it became a crime scene."
            ),
            "items": [],
            "suspects": [],
            "searchable": [],
            "body_examinable": True,
            "datachip_found": False,
            "victim_id_found": False
        },
        "freezer": {
            "desc": "FREEZER – A cramped sub-zero storage locker. Frost creeps over plastic crates and a half-empty case of synth-crab.",
            "items": [],
            "suspects": [],
            "searchable": [],
            "body_examinable": False
        }
    }

    MISLEADING_CLUES = {
        "marcus": ["aiden_says_alice_promoted", "aiden_says_alice_paycheck", "aiden_says_victim_angry"],
        "cleopatra": ["alice_blake_screenshots", "alice_victim_msg_afraid", "alice_victim_cant_stay_home", "dining_ice"],
        "napoleon": ["blake_nyx_bully", "blake_nyx_called_out", "blake_victim_distant"],
        RESERVED_KEY_THX1138: ["nyx_aiden_resented", "nyx_alice_promoted_over_victim", "nyx_victim_didnt_want_return"],
        "janitor": ["luka_says_cook_threatened", "luka_says_patron_was_outside", "luka_says_ring_was_planted"],
        "cook": ["adeline_says_janitor_stole_ring", "adeline_says_alice_argued", "adeline_says_victim_was_armed", "apartment_flyers"],
        "patron": ["hemlock_says_blake_threatened", "hemlock_says_airlock_heard", "hemlock_says_nyx_was_calm", "bathroom_syntharette"]
    }

    MISLEADING_DIALOGUE = {
        "luka_says_cook_threatened": "'That cook... I heard her say she'd shut Marsha up for good.'",
        "luka_says_patron_was_outside": "'The old man? He went outside right before the shot. I swear I heard the airlock cycle.'",
        "luka_says_ring_was_planted": "'The ring... I think someone else took it, or maybe she lost it. I'm being framed. Marsha was a bitch anyway.'",
        "adeline_says_janitor_stole_ring": "'Elliot? He's been obsessed with that ring. Probably sold it to cover his debts.'",
        "adeline_says_alice_argued": "'Alice and Marsha had a screaming match. Something about a promotion, or a client...I don't really remember.'",
        "adeline_says_victim_was_armed": "'Marsha carried a small knife. She wasn't defenseless. She was ruthless and cruel. I'm not surprised she got got.'",
        "hemlock_says_blake_threatened": "'That short fellow? He was muttering threats under his breath all evening.'",
        "hemlock_says_airlock_heard": "'I heard the airlock hiss. Someone came or went right before the bang.'",
        "hemlock_says_nyx_was_calm": "'Nyx? They were the calmest person in the room when it happened. Suspiciously calm.'",
        "aiden_says_alice_promoted": "'Alice never got the promotion that she wanted. That's motive enough.'",
        "aiden_says_alice_paycheck": "'Alice's paycheck was docked because of Marsha. She was furious. At least, that's how I remember it.'",
        "aiden_says_victim_angry": "'Marsha was angry at everyone. It was only a matter of time. I don't know what it was, but she was in a dark place, and she always made that everyone else's problem too.'",
        "alice_blake_screenshots": "'Blake sent threatening messages to Marsha. I have screenshots. Here, let me send them to you.'",
        "alice_victim_msg_afraid": "'Marsha told me she was scared to be here. I'm not sure why she was here, but she was.'",
        "alice_victim_cant_stay_home": "'Marsha said she couldn't stay in her apartment anymore. Someone was harassing her.'",
        "blake_nyx_bully": "'Nyx bullied Marsha constantly. It was psychological warfare. I don't know if they were together or if Nyx was just holding her hostage.'",
        "blake_nyx_called_out": "'Nyx was called out by Marsha in front of everyone. Humiliated. She didn't react, but we all know she was waiting for the right moment.'",
        "blake_victim_distant": "'Marsha had become distant lately. She knew something was coming. I tried to reach out to her. She just wouldn't let me.'",
        "nyx_aiden_resented": "'Aiden resented Marsha for reporting him to management. He had plenty run-ins with her, and every one was something he'd whine about like a school-girl.'",
        "nyx_alice_promoted_over_victim": "'Alice leapfrogged Marsha for that promotion. She'd waited years for that spot, and she didn't think Alice deserved it.'",
        "nyx_victim_didnt_want_return": "'Marsha didn't want to come back here. She knew it wasn't safe. She just couldn't stay in her apartment either, I'm sure you've heard the rumors, right? How Blake was terrorizing her?'"
    }

    MOTIVE_GOSSIP = {
        "marcus": ("cleopatra", "'I heard that Alice had a breakdown in business negotiations. Something about a hostile takeover that went south.'", "marcus_gossip_cleopatra"),
        "napoleon": ("marcus", "'Aiden? He had personal differences with Marsha over the use of power. I heard he was close to being fired.'", "napoleon_gossip_marcus"),
        "cleopatra": ("napoleon", "'Blake used to date Marsha. Bad breakup. I'm talking the kind that leaves blood on the cutting room floor.'", "cleopatra_gossip_napoleon"),
        "janitor": ("cook", "'That cook... I overheard her saying Marsha was her landlord. Always demanding rent. She called her a leech.'", "janitor_gossip_cook"),
        "cook": ("janitor", "'Elliot? Marsha accused him of stealing a ring. He spent days looking for it, even after everyone thought he was faking.'", "cook_gossip_janitor"),
        "patron": ("thatcher", "'Nyx... Marsha stood up to them once. I mean Marsha, I mean. She didn't back down. Nyx hates being challenged.'", "patron_gossip_thatcher"),
        RESERVED_KEY_THX1138: ("patron", "'Hemlock? He claims he was in the bathroom, but I saw him go out the front door. He's hiding something.'", "nyx_gossip_patron")
    }

    CONFRONT_DIALOGUE = {
        "marcus": "'I... I didn't mean to cause trouble. She just pushed too hard, okay? But that doesn't mean I killed her!'",
        "napoleon": "'Yeah, we dated. So what? It ended badly. That doesn't make me a murderer!'",
        "cleopatra": "'Hostile takeover? Please. My hands are clean. I was on a bus when it happened!'",
        "janitor": "'The ring? I never stole it! She was a liar. I was just trying to find it to clear my name!'",
        "cook": "'So she was my landlord. So what? I didn't kill her over rent. That's insane.'",
        "patron": "'I went to the bathroom. The airlock? I don't know what you're talking about. I'm old, not stupid.'",
        RESERVED_KEY_THX1138: "'You've got nothing. I've been in this office the whole time. Ask anyone who actually matters.'"
    }

    ADELINE_ESCAPE_REACTIONS = {
        "marcus": "Adeline? Idk. She never was one for conflict. I'm guessing she got cold feet and just bounced. Maybe she's hoping you exonerate her by the end of this. Maybe she's just got cold blood. I guess you'll be the first to know.",
        "napoleon": "Oh, the little frycook lady? Yeah, I saw her run through here, and I assumed you were right behind her. Then, she disappeared out the airlock and was gone. Why did she run? Do you know? No? Maybe she realized you were onto her.",
        "cleopatra": "Yeah, I think we both know what just happened. What do you want from me? An excuse? An explanation? I have neither and I expect you to learn to cope with that fact sooner than later, detective.",
        "janitor": "Yeah, I saw her. She rushed past with a haste I'd never seen from her. I'm sure she's just scared out of her wits, the poor thing. She's probably run home to hide under a blanket and hope you find the killer before she's next.",
        "cook": "I-I'm.... I'm sorry! I can't think straight! This is all just so fucked up! I don't know! I don't know!! I'm not ok. PLEASE, please, understand, I'm scared. I'm so scared. Adeline bursts into tears. A sense of pity opens up in your stomach, and a sense of dread grips you as you realize this poor creature could be manipulating you. It's unlikely, you think, but the possibility is still unsettling, and still not ruled out just yet.",
        "patron": "Huh? What? Escape? Who? I didn't see anything. And I don't care.",
        RESERVED_KEY_THX1138: "Adeline ran out the door? Hahaha....that poor thing. She's harmless, but she's also stupid. I'm sure she knows it's a felony to flee an active crime scene like that, but I'm also sure her reasons were poorly thought through and likely more of a mess than she was after the murder. What do you want from me? I have nothing else to say about this."
    }

    EVIDENCE_DESCRIPTIONS = {
        "aiden_alibi": "Payphone log. Aiden was on a call at time of death.",
        "luka_alibi": "Wet floor sign and pristine sheen near the counter. Elliot's alibi.",
        "blake_alibi": "Time-stamped napkin. Blake's scribblings from all evening.",
        "blake_alibi_confirmed": "Blake's alibi verified via handwriting scan. Consistent.",
        "hemlock_missing": "Old coffee receipt, hours before the murder. Doesn't confirm his whereabouts.",
        "alice_alibi": "Bus ticket stub. Alice arrived just before or after the shot.",
        "alice_alibi_confirmed": "Alice's alibi verified by transit database. Legitimate ticket.",
        "adeline_timestamps": "Stock bucket label with timestamped order docket. Adeline's alibi.",
        "adeline_alibi_confirmed": "Adeline's alibi verified by freezer logs. She was in the freezer at time of death.",
        "nyx_message": "Torn paper. Nyx's handwriting. An angry letter to the victim.",
        "unknown_revolver": "A revolver, recently fired. The murder weapon.",
        "aiden_footprint": "Tracks outside the back porthole. Too big to be Aiden's.",
        "blake_witness": "Someone with strong posture left the office after the bang.",
        "alice_witness": "Loud argument from the office. Nyx and the victim.",
        "luka_swept": "Someone walked towards the office with a determined stride.",
        "adeline_heard": "Loud argument from the office. A woman's voice and someone calm.",
        "hemlock_yelling": "Heated yelling near the office. Words were unclear.",
        "cook_landlord": "Adeline revealed the victim was her landlord.",
        "marcus_gossip_cleopatra": "Aiden says Alice had a breakdown in business negotiations.",
        "napoleon_gossip_marcus": "Blake says Aiden had personal differences with the victim over power.",
        "cleopatra_gossip_napoleon": "Alice says Blake and the victim had a bad breakup.",
        "janitor_gossip_cook": "Elliot says Adeline's landlord was the victim, always demanding rent.",
        "cook_gossip_janitor": "Adeline says Elliot was accused of stealing a ring and searched for days.",
        "patron_gossip_thatcher": "Hemlock says Nyx was challenged by the victim and hates being defied.",
        "nyx_gossip_patron": "Nyx says Hemlock went out the front door, not the bathroom.",
        "aiden_says_alice_promoted": "Aiden claims Alice never got the promotion she wanted.",
        "aiden_says_alice_paycheck": "Aiden says Alice's paycheck was docked because of Marsha.",
        "aiden_says_victim_angry": "Aiden says Marsha was angry at everyone.",
        "alice_blake_screenshots": "Alice claims Blake sent threatening messages to Marsha.",
        "alice_victim_msg_afraid": "Alice says Marsha was scared to be here.",
        "alice_victim_cant_stay_home": "Alice says Marsha couldn't stay in her apartment.",
        "blake_nyx_bully": "Blake says Nyx bullied Marsha constantly.",
        "blake_nyx_called_out": "Blake says Nyx was humiliated by Marsha publicly.",
        "blake_victim_distant": "Blake says Marsha had become distant lately.",
        "nyx_aiden_resented": "Nyx says Aiden resented Marsha for reporting him.",
        "nyx_alice_promoted_over_victim": "Nyx says Alice leapfrogged Marsha for a promotion.",
        "nyx_victim_didnt_want_return": "Nyx says Marsha didn't want to come back.",
        "luka_says_cook_threatened": "Elliot says Adeline threatened to shut Marsha up.",
        "luka_says_patron_was_outside": "Elliot says Hemlock went outside right before the shot.",
        "luka_says_ring_was_planted": "Elliot says the ring was planted to frame him.",
        "adeline_says_janitor_stole_ring": "Adeline says Elliot stole the ring.",
        "adeline_says_alice_argued": "Adeline says Alice and Marsha had a screaming match.",
        "adeline_says_victim_was_armed": "Adeline says Marsha carried a knife.",
        "hemlock_says_blake_threatened": "Hemlock says Blake was muttering threats.",
        "hemlock_says_airlock_heard": "Hemlock says he heard the airlock hiss.",
        "hemlock_says_nyx_was_calm": "Hemlock says Nyx was suspiciously calm.",
        "bullet_casing": "A spent bullet casing found in the office. Matches the revolver calibre.",
        "datachip": "A datachip from a loose panel in the bathroom. Contains encrypted communications.",
        "bloody_cleaver": "A bloody cleaver in the freezer. A grisly red herring.",
        "cleaver_analysis": "Scanner shows the blood is lab-meat juice, not human.",
        "galactic_id2": "Victim's real ID. Marsha Stone. No doubt about it now.",
        "apartment_flyers": "A stack of paper flyers for other apartment units in the neighborhood.",
        "dining_ice": "Ice machine with clear fingerprints on the handle.",
        "bathroom_syntharette": "A single, smoked syntharette jammed up in the vent grate.",
    }

    EVIDENCE_IMPLICATION = {
        "aiden_alibi": (["Unknown"], ["Aiden"]),
        "luka_alibi": (["Unknown"], ["Elliot"]),
        "blake_alibi": (["Unknown"], ["Blake"]),
        "blake_alibi_confirmed": (["Unknown"], ["Blake"]),
        "hemlock_missing": (["Unknown"], ["Alexander"]),
        "alice_alibi": (["Unknown"], ["Alice"]),
        "alice_alibi_confirmed": (["Unknown"], ["Alice"]),
        "adeline_timestamps": (["Unknown"], ["Adeline"]),
        "adeline_alibi_confirmed": (["Unknown"], ["Adeline"]),
        "nyx_message": (["Nyx"], []),
        "unknown_revolver": (["Nyx", "Unknown"], []),
        "aiden_footprint": (["Unknown"], ["Aiden"]),
        "blake_witness": (["Nyx"], []),
        "alice_witness": (["Nyx"], []),
        "luka_swept": (["Nyx"], []),
        "adeline_heard": (["Nyx"], []),
        "hemlock_yelling": (["Nyx"], []),
        "cook_landlord": (["Adeline"], []),
        "marcus_gossip_cleopatra": (["Alice"], []),
        "napoleon_gossip_marcus": (["Aiden"], []),
        "cleopatra_gossip_napoleon": (["Blake"], []),
        "janitor_gossip_cook": (["Adeline"], []),
        "cook_gossip_janitor": (["Elliot"], []),
        "patron_gossip_thatcher": (["Nyx"], []),
        "nyx_gossip_patron": (["Alexander"], []),
        "aiden_says_alice_promoted": (["Alice"], []),
        "aiden_says_alice_paycheck": (["Alice"], []),
        "aiden_says_victim_angry": (["Unknown"], []),
        "alice_blake_screenshots": (["Blake"], []),
        "alice_victim_msg_afraid": (["Unknown"], []),
        "alice_victim_cant_stay_home": (["Unknown"], []),
        "blake_nyx_bully": (["Nyx"], []),
        "blake_nyx_called_out": (["Nyx"], []),
        "blake_victim_distant": (["Unknown"], []),
        "nyx_aiden_resented": (["Aiden"], []),
        "nyx_alice_promoted_over_victim": (["Alice"], []),
        "nyx_victim_didnt_want_return": (["Unknown"], []),
        "luka_says_cook_threatened": (["Adeline"], []),
        "luka_says_patron_was_outside": (["Alexander"], []),
        "luka_says_ring_was_planted": (["Elliot"], []),
        "adeline_says_janitor_stole_ring": (["Elliot"], []),
        "adeline_says_alice_argued": (["Alice"], []),
        "adeline_says_victim_was_armed": (["Unknown"], []),
        "hemlock_says_blake_threatened": (["Blake"], []),
        "hemlock_says_airlock_heard": (["Unknown"], []),
        "hemlock_says_nyx_was_calm": (["Nyx"], []),
        "bullet_casing": (["Nyx"], []),
        "datachip": (["Nyx"], []),
        "bloody_cleaver": (["Unknown"], []),
        "cleaver_analysis": (["Unknown"], []),
        "galactic_id2": ([], ["Marsha"]),
        "apartment_flyers": (["Adeline"], []),
        "dining_ice": (["Unknown"], ["Napoleon"]),
        "bathroom_syntharette": (["Unknown"], []),
    }

    EVIDENCE_ALIASES = {
        "payphone log": "aiden_alibi", "phone log": "aiden_alibi", "log": "aiden_alibi", "payphone": "aiden_alibi", "p log": "aiden_alibi",
        "wet floor sign": "luka_alibi", "floor sign": "luka_alibi", "sheen": "luka_alibi", "wet floor": "luka_alibi",
        "time-stamped napkin": "blake_alibi", "napkin": "blake_alibi", "blake's napkin": "blake_alibi",
        "blake confirmed": "blake_alibi_confirmed",
        "coffee receipt": "hemlock_missing", "receipt": "hemlock_missing", "old receipt": "hemlock_missing",
        "bus ticket stub": "alice_alibi", "ticket stub": "alice_alibi", "bus ticket": "alice_alibi", "ticket": "alice_alibi", "bus stub": "alice_alibi", "b ticket": "alice_alibi", "bts": "alice_alibi",
        "alice confirmed": "alice_alibi_confirmed",
        "stock bucket": "adeline_timestamps", "order docket": "adeline_timestamps", "docket": "adeline_timestamps", "label": "adeline_timestamps",
        "adeline's alibi confirmed": "adeline_alibi_confirmed", "freezer log": "adeline_alibi_confirmed",
        "torn paper": "nyx_message", "nyx's letter": "nyx_message", "letter": "nyx_message",
        "revolver": "unknown_revolver", "gun": "unknown_revolver", "weapon": "unknown_revolver",
        "footprint": "aiden_footprint", "tracks": "aiden_footprint", "outside tracks": "aiden_footprint",
        "strong posture witness": "blake_witness", "posture witness": "blake_witness",
        "argument witness": "alice_witness", "argument": "alice_witness",
        "determined stride": "luka_swept", "stride": "luka_swept",
        "adeline heard": "adeline_heard", "woman's voice": "adeline_heard",
        "hemlock yelling": "hemlock_yelling", "yelling": "hemlock_yelling",
        "landlord motive": "cook_landlord", "landlord": "cook_landlord",
        "bullet casing": "bullet_casing", "casing": "bullet_casing",
        "datachip": "datachip", "chip": "datachip",
        "bloody cleaver": "bloody_cleaver", "cleaver": "bloody_cleaver",
        "cleaver analysis": "cleaver_analysis",
        "fake id": "galactic_id", "fake identification": "galactic_id",
        "victim's id": "galactic_id2", "real id": "galactic_id2", "marsha's id": "galactic_id2",
        "apartment flyers": "apartment_flyers", "flyers": "apartment_flyers",
        "ice machine": "dining_ice", "fingerprints": "dining_ice",
        "syntharette": "bathroom_syntharette", "vent": "bathroom_syntharette",
        "alice's motive": ["aiden_says_alice_promoted", "nyx_alice_promoted_over_victim"],
        "alice's paycheck": ["aiden_says_alice_paycheck"],
        "marsha's anger": ["aiden_says_victim_angry"],
        "blake screenshots": ["alice_blake_screenshots"],
        "marsha scared": ["alice_victim_msg_afraid"],
        "marsha left apartment": ["alice_victim_cant_stay_home"],
        "nyx bullying": ["blake_nyx_bully"],
        "nyx called out": ["blake_nyx_called_out"],
        "marsha and blake distant": ["blake_victim_distant"],
        "aiden resented marsha": ["nyx_aiden_resented"],
        "marsha didn't want return": ["nyx_victim_didnt_want_return"],
        "cook threatened": ["luka_says_cook_threatened"],
        "patron outside": ["luka_says_patron_was_outside"],
        "ring planted": ["luka_says_ring_was_planted"],
        "janitor stole ring": ["adeline_says_janitor_stole_ring"],
        "alice argued": ["adeline_says_alice_argued"],
        "marsha armed": ["adeline_says_victim_was_armed"],
        "blake threatened": ["hemlock_says_blake_threatened"],
        "airlock heard": ["hemlock_says_airlock_heard"],
        "nyx calm": ["hemlock_says_nyx_was_calm"],
    }

    EVIDENCE_VERIFY = {
        "aiden_alibi": "You scan the payphone log. Seconds later you get a ping, and unsurprisingly it is a real log. Why anyone would fake a payphone log, or more to the point, how, you don't know, but it never hurts to be careful.",
        "luka_alibi": None,
        "blake_alibi": "You scan the napkin and upload it to the handwriting database. Moments later, you get a confirmation that it is in fact Blake's handwriting. This is definitely his work, although you still can't verify the timestamp.",
        "blake_alibi_confirmed": "Blake's alibi holds up under scrutiny. The handwriting matches and the timeline is plausible.",
        "hemlock_missing": "You know a diner receipt when you see it, although that still doesn't account for Hemlock's whereabouts.",
        "alice_alibi": "You scan the bus ticket. Instantly, you get a ping confirming the legitimacy. It's definitely an officially issued ticket. Although, it never hurts to be careful.",
        "alice_alibi_confirmed": "The transit database confirms Alice was on that bus. Her alibi is airtight.",
        "adeline_timestamps": "You scan the label and compare it to the handwriting database. It's definitely a match for Adeline.",
        "adeline_alibi_confirmed": "Freezer logs confirm Adeline was inside at the time of death. She's exonerated.",
        "nyx_message": "You scan the letter fragment. Unfortunately, the database isn't able to get enough of the message to fully confirm or deny the match to Nyx. You'll have to think on this.",
        "unknown_revolver": "You scan the weapon for fingerprints, but nothing shows up. Curiously, not even the gunshot residue that normally accompanies a fired weapon is present. It's been thoroughly cleaned, probably by the killer.",
        "aiden_footprint": "You squint your eyes. There isn't much you can do from this side of the door, and you aren't equipped to go for a space-walk. You'll have to think on this.",
        "blake_witness": None,
        "alice_witness": None,
        "luka_swept": None,
        "adeline_heard": None,
        "hemlock_yelling": None,
        "cook_landlord": None,
        "marcus_gossip_cleopatra": None,
        "napoleon_gossip_marcus": None,
        "cleopatra_gossip_napoleon": None,
        "janitor_gossip_cook": None,
        "cook_gossip_janitor": None,
        "patron_gossip_thatcher": None,
        "nyx_gossip_patron": None,
        "aiden_says_alice_promoted": None,
        "aiden_says_alice_paycheck": None,
        "aiden_says_victim_angry": None,
        "alice_blake_screenshots": None,
        "alice_victim_msg_afraid": None,
        "alice_victim_cant_stay_home": None,
        "blake_nyx_bully": None,
        "blake_nyx_called_out": None,
        "blake_victim_distant": None,
        "nyx_aiden_resented": None,
        "nyx_alice_promoted_over_victim": None,
        "nyx_victim_didnt_want_return": None,
        "luka_says_cook_threatened": None,
        "luka_says_patron_was_outside": None,
        "luka_says_ring_was_planted": None,
        "adeline_says_janitor_stole_ring": None,
        "adeline_says_alice_argued": None,
        "adeline_says_victim_was_armed": None,
        "hemlock_says_blake_threatened": None,
        "hemlock_says_airlock_heard": None,
        "hemlock_says_nyx_was_calm": None,
        "bullet_casing": "You open the revolver, pull out the casing, and drop it into the slot. It's a perfect fit. This bullet was definitely fired from this gun. That much is obvious.",
        "datachip": "You plug the chip into your scanner and wait for the data to transfer. A few seconds later a notification appears:\n\"ENCRYPTED DATA\"\nYou select the option to decrypt. There's no telling when, or even if, this will finish anytime soon. You put everything away and take a deep breath. Just as your hands return to your sides, you hear a ping and pull your scanner back out of your pocket to see the screen\nEst. Decryption: 132h2m12s\nWell, that's not good. You'll have to figure something else out after all.",
        "bloody_cleaver": "You scan the cleaver, first for DNA then for prints. The prints match Adeline. She definitely handled it.",
        "cleaver_analysis": "Further analysis confirms the blood is lab‑meat juice, not human. Adeline's story checks out.",
        "galactic_id2": "This is her genuine ID. Marsha Stone. No aliases, no games.",
        "apartment_flyers": "The flyers are all for different addresses. Adeline was planning to move, maybe?",
        "dining_ice": "The prints are too smudged to match. Anyone could have touched this.",
        "bathroom_syntharette": "The brand is cheap and common. However, there's only one smoker here.",
    }

    TAMPER_ACTIONS = {
        "aiden_alibi": ("destroy", "You tear up the payphone log and drop it into the trash. Who cares? Not you."),
        "luka_alibi": ("destroy", "You drag your shoes across the floor leaving streaks. The floor is no longer clean. Maybe it was never clean."),
        "blake_alibi": ("destroy", "You tear the napkin to shreds and toss it into the trash. It's not like it'll make a difference. You're the one who makes the difference."),
        "hemlock_missing": ("destroy", "You snap open your lighter and flick. Holding the receipt over the flame causes it to flash into a puff of smoke. It's not like it was that important anyway."),
        "alice_alibi": ("destroy", "You snap open your lighter and flick the wheel. The ticket-stub burns to a crispy carbon finish and its ashes scatter across the diner. Who cares?"),
        "adeline_timestamps": ("destroy", "You wipe the bucket with a wet rag. The label dissolves almost instantly. It's like it was never there."),
        "adeline_alibi_confirmed": ("destroy", "You tear the sheet into tiny pieces and stuff them into your pocket. As far as you're concerned, there never was a log sheet."),
        "nyx_message": ("destroy", "You eat the scrap of paper quickly, swallowing with some difficulty, but you get it down. The only way to get it back would require cops to do the one thing they never do: truly investigate one of their own."),
        "unknown_revolver": ("plant", "You plant the revolver on {suspect} carefully and quietly. Whenever the police drone gets here, it'll be they who goes down for it."),
        "bullet_casing": ("plant", "You plant the spent round on {suspect}. It may not be enough, but it's something. You just need a conviction, not necessarily justice."),
        "bloody_cleaver": ("plant", "You plant the cleaver on {suspect}. It may not be enough, but it's something. After all, you only need a conviction, not necessarily justice."),
        "datachip": ("destroy", "You smash the data chip on the ground beneath your heel. Pieces scatter in every direction. If it wasn't unusable before, it sure as shit is now."),
        "alice_blake_screenshots": ("destroy", "You delete the screenshots. It's not like you cared about any of that drama anyway."),
    }

    incriminating = {"nyx_message", "unknown_revolver", "aiden_footprint", "blake_witness", "alice_witness"}
    required_incriminating = 3

    return {
        "suspects": suspects,
        "suspect_descriptions": suspect_descriptions,
        "suspect_aliases": suspect_aliases,
        "revealed_characteristic": revealed_characteristic,
        "locations": locations,
        "MISLEADING_CLUES": MISLEADING_CLUES,
        "MISLEADING_DIALOGUE": MISLEADING_DIALOGUE,
        "MOTIVE_GOSSIP": MOTIVE_GOSSIP,
        "CONFRONT_DIALOGUE": CONFRONT_DIALOGUE,
        "ADELINE_ESCAPE_REACTIONS": ADELINE_ESCAPE_REACTIONS,
        "EVIDENCE_DESCRIPTIONS": EVIDENCE_DESCRIPTIONS,
        "EVIDENCE_IMPLICATION": EVIDENCE_IMPLICATION,
        "EVIDENCE_ALIASES": EVIDENCE_ALIASES,
        "EVIDENCE_VERIFY": EVIDENCE_VERIFY,
        "TAMPER_ACTIONS": TAMPER_ACTIONS,
        "incriminating": incriminating,
        "required_incriminating": required_incriminating
    }
