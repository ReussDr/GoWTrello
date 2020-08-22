"""
Common helper functions for interpreting Gems of War Data
"""

TROOPS_REQ_FOR_ASCENSION = [5, 10, 25, 50, 100]
PETS_REQ_FOR_ASCENSION = [5, 10, 15]

RARITY_LOOKUP = ["Zero",
                 "Common",
                 "Rare",
                 "Ultra-Rare",
                 "Epic",
                 "Legendary",
                 "Mythic"]

KINGDOM_FACTION_MAP = {
    "Adana" : "",
    "Blackhawk": "",
    "Blighted Lands": "Fell Roost",
    "Bright Forest": "Sunken Fleet",
    "Broken Spire": "",
    "Darkstone": "All-Seeing Eye",
    "Dhrak-Zum": "Illithia",
    "Divinion Fields": "Wild Court",
    "Dragon's Claw": "",
    "Drifting Sands": "The Deep Hive",
    "Forest of Thorns": "Primal Rift",
    "Ghulvania": "",
    "Glacial Peaks": "Mirrored Halls",
    "Grosh-Nak": "",
    "Karakoth": "",
    "Khaziel": "",
    "Khetar": "Fang Moor",
    "Leonis Empire": "City of Thieves",
    "Maugrim Woods": "",
    "Merlantis": "Sea of Sorrow",
    "Mist of Scales": "Dark Pits",
    "Pan's Vale": "The Warrens",
    "Pridelands": "",
    "Shentang": "Lyrasza's Lair",
    "Silverglade": "Silver Necropolis",
    "Sin of Maraj": "Depths of Sin",
    "Stormheim": "Frostfire Keep",
    "Suncrest": "Stonesong Eyrie",
    "Sword's Edge": "Crypt Keepers",
    "Urskaya": "Werewoods",
    "Whitehelm": "Hall of Guardians",
    "Wild Plains": "",
    "Zaejin": "Amanithrax",
    "Zhul'Kari": "",
}

NON_KINGDOMS = [
    "Apocalypse",
    "Guardians",
    "Primal",
    "The Vault",
]


def is_kingdom(name):
    """
    Return true if name is a Kingdom (one of the 34 in Krystara)
    :param name: name of the (potential) Kingdom
    """
    if name in KINGDOM_FACTION_MAP:
        return True
    return False


def is_faction(name):
    """
    Returns true if name is an Underworld Faction
    :param name: name of the (potential) Faction
    """
    if name in KINGDOM_FACTION_MAP.values():
        return True
    return False


def is_non_kingdom(name):
    """
    Returns true if name is a non-Kingdom
    :param name: name of the (potential) non-Kingdom
    """
    if name in NON_KINGDOMS:
        return True
    return False


def lookup_kingdom_from_faction(name):
    """
    Return the Kingdom name that corresponds to the specified Faction (if any)
    :param name: name of the (potential) Faction
    """
    if not is_faction(name):
        return ""
    for kingdom in KINGDOM_FACTION_MAP:
        if KINGDOM_FACTION_MAP[kingdom] == name:
            return kingdom
    print("Error: Couldn't find Kingdom for faction:", name)
    return ""


def troops_needed_to_mythic(base_rarity, current_rarity, current_count):
    """
    Calculate troops needed to ascend to mythic

    :param name:           name of the Troop
    :param base_rarity:    Original Ascension of the Troop
    :param current_rarity: Current Ascension Level
    :param current_count:  Current number of that troop we have
    :return:               Number of Troops needed to Ascend to Mythic
    """
    # First, calculate the total number of that troop we would need if we had 0
    total_needed = 1
    next_iter = 0
    for i in range(base_rarity, 6):
        total_needed += TROOPS_REQ_FOR_ASCENSION[next_iter]
        next_iter += 1

    # Next, calculate how many troops we've already spent on ascension
    next_iter = 0
    total_have = current_count
    for i in range(base_rarity, current_rarity):
        total_have += TROOPS_REQ_FOR_ASCENSION[next_iter]
        next_iter += 1

    #
    if total_needed <= total_have:
        return 0
    return total_needed - total_have
