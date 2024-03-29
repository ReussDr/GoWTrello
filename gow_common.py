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
    "Adana": "Tinker Town",
    "Blackhawk": "The Black Heart",
    "Blighted Lands": "Fell Roost",
    "Bright Forest": "Sunken Fleet",
    "Broken Spire": "Fire Rift",
    "Darkstone": "All-Seeing Eye",
    "Dhrak-Zum": "Illithia",
    "Divinion Fields": "Wild Court",
    "Dragon's Claw": "Wyrmrun",
    "Drifting Sands": "The Deep Hive",
    "Forest of Thorns": "Primal Rift",
    "Ghulvania": "Dark Court",
    "Glacial Peaks": "Mirrored Halls",
    "Grosh-Nak": "Dripping Caverns",
    "Hellcrag": "Obsidian Depths",
    "Karakoth": "Duergaroth",
    "Khaziel": "Emperinazar",
    "Khetar": "Fang Moor",
    "Leonis Empire": "City of Thieves",
    "Maugrim Woods": "Hell Gate",
    "Merlantis": "Sea of Sorrow",
    "Mist of Scales": "Dark Pits",
    "Nexus": "Umbral Nexus",
    "Pan's Vale": "The Warrens",
    "Pridelands": "Indrajit's Palace",
    "Shentang": "Lyrasza's Lair",
    "Silverglade": "Silver Necropolis",
    "Sin of Maraj": "Depths of Sin",
    "Stormheim": "Frostfire Keep",
    "Suncrest": "Stonesong Eyrie",
    "Sword's Edge": "Crypt Keepers",
    "Urskaya": "Werewoods",
    "Whitehelm": "Hall of Guardians",
    "Wild Plains": "The Labyrinth",
    "Zaejin": "Amanithrax",
    "Zhul'Kari": "Eldrazhor",
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
    for i in range(0, 6 - base_rarity):
        total_needed += TROOPS_REQ_FOR_ASCENSION[i]

    # Next, calculate how many troops we've already spent on ascension
    total_have = current_count
    for i in range(0, current_rarity - base_rarity):
        total_have += TROOPS_REQ_FOR_ASCENSION[i]

    # If we have more than we need, return 0, otherwise subtract and return
    if total_needed <= total_have:
        return 0
    return total_needed - total_have

def pets_needed_to_mythic(base_rarity, current_rarity, current_count):
    """
    Calculate troops needed to ascend to mythic

    :param name:           name of the Pet
    :param base_rarity:    Original Ascension of the Pet
    :param current_rarity: Current Ascension Level
    :param current_count:  Current number of that pet we have
    :return:               Number of Pets needed to Ascend to Mythic
    """
    # First, calculate the total number of that troop we would need if we had 0
    total_needed = 1
    for i in range(0, 6 - base_rarity):
        total_needed += PETS_REQ_FOR_ASCENSION[i]

    # Next, calculate how many troops we've already spent on ascension
    total_have = current_count
    for i in range(0, current_rarity - base_rarity):
        total_have += PETS_REQ_FOR_ASCENSION[i]

    # If we have more than we need, return 0, otherwise subtract and return
    if total_needed <= total_have:
        return 0
    return total_needed - total_have
