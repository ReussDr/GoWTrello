"""
Module for Weapon class (for Gems of War Data)
"""

import gow_common

TRAITS_TO_MAX = [0, 5, 6, 7, 8, 9, 10, 10]

# Weapons listed in gowdb.com that are not available
WEAPONS_UNOBTAINABLE = [
    "Blighted Weapon",              # Blighted Lands
    "Bright Forest Weapon",         # Bright Forest
    "C6 W1",                        # Bright Forest
    "Blue Doomed Weapon",           # Broken Spire
    "Broken Spire Weapon",          # Broken Spire
    "Brown Doomed Weapon",          # Broken Spire
    "Campaign 2 Weapon A",          # Broken Spire
    "Campaign 2 Weapon B",          # Broken Spire
    "Campaign 2 Weapon C",          # Broken Spire
    "Green Doomed Weapon",          # Broken Spire
    "Purple Doomed Weapon",         # Broken Spire
    "Red Doomed Weapon",            # Broken Spire
    "Tauros Invasion Weapon",       # Broken Spire
    "Yellow Doomed Weapon",         # Broken Spire
    "Darkstone Raid Boss Weapon",   # Darkstone
    "Darkstone Weapon",             # Darkstone
    "Dhrak-Zum Weapon",             # Dhrak-Zum
    "Divinion Fields Weapon",       # Divinion Fields
    "Dragon's Claw Weapon",         # Dragon's Claw
    "Drifting Sands Weapon",        # Drifting Sands
    "Forest Weapon",                # Forest of Thorns
    "Ghulvania Weapon",             # Ghulvania
    "Glacial Weapon",               # Glacial Peaks
    "Grosh-Nak Weapon",             # Grosh-Nak
    "Karakoth Weapon",              # Karakoth
    "Khetar Weapon",                # Khetar
    "Khaziel Weapon",               # Khaziel
    "Khetari",                      # Khetar
    "Maugrim Weapon",               # Maugrim Woods
    "Merlantis Weapon",             # Merlantis
    "Mist of Scales Weapon",        # Mist of Scales
    "Shentang Weapon",              # Shentang
    "Wild Orb",                     # Silverglade
    "Suncrest Weapon",              # Suncrest
    "Urskaya Weapon",               # Urskaya
    "Divine Invasion Weapon",       # Whitehelm
    "Whitehelm Weapon",             # Whitehelm
]

# List of Weapons, current not listed in gowdb.com
WEAPONS_MISSING = {
#    "Norbert's Turnip": "Zaejin",
}

WEAPONS_PAID = {
    "Wrenchmaster 5000",            # Adana
    "Skullblade",                   # Blackhawk
    "Chaos Blade",                  # Blighted Lands
    "Fey Wand",                     # Bright Forest
    "Goblin Crusher",               # Broken Spire
    "Soultrap",                     # Darkstone
    "Daemon's Leash",               # Dhrak Zum
    "Eternal Flame",                # Divinion Fields
    "Prey Seeker",                  # Dragon’s Claw
    "Sands of Time",                # Drifting Sands
    "Yasmine's Chalice",            # Forest of Thorns
    "Chain Flail",                  # Ghulvania
    "Nature's Wrath",               # Glacial Peaks
    "Skull Cleaver",                # Grosh-Nak
    "Staff of Madness",             # Karakoth
    "Deepstone",                    # Khaziel
    "Merchant's Blade",             # Leonis Empire
    "Crimson Insignia",             # Maugrim Woods - This one was also a special giveaway at PAX Aus 2015
    "Undine's Trident",             # Merlantis
    "Kris Knife",                   # Mist of Scales
    "Crescendo",                    # Pan’s Vale
    "Sun Chakram",                  # Pridelands
    "Festival Staff",               # Shen Tang
    "Sun and Moon",                 # Silverglade
    "Tome of Sin",                  # Sin of Maraj
    "Frost Reaver",                  # Stormheim
    "Farsight Orb",                 # Suncrest
    "Order and Chaos",              # Swords Edge
    "Bear Totem",                   # Urskaya
    "Celestial Staff",              # Whitehelm
    "Bullroarer",                   # Wild Plains
    "Boom-Boom",                    # Zaejin
    "Spider's Kiss",                # Zhul’Kari
}

class Weapon:
    """
    Weapon class to hold data about Gems of War Weapons
    """
    def __init__(self, name, count, rarity, kingdom, traitcount):
        self._vals = {}
        self._vals['name'] = name
        self._vals['count'] = count
        self._vals['rarity'] = rarity
        self._vals['traitcount'] = traitcount
        self._vals['kingdom'] = ""
        self._vals['paid'] = name in WEAPONS_PAID

        if gow_common.is_kingdom(kingdom):
            self._vals['kingdom'] = kingdom
        else:
            print("Error: Couldn't find kingdom:", kingdom)

    @classmethod
    def gen_weapon_from_json(cls, json_record):
        """
        Alternate constructor.  Allows you pass in a json_record, and it'll parse all the data out

        :param json_record: The json record (from gowdb inventory)
        :return:            The constructed Weapon object
        """
        if json_record['name'] in WEAPONS_UNOBTAINABLE:
            if 'count' in json_record and json_record['count'] > 0:
                print("Error: Unobtainable Weapon Owned", json_record['name'])
            return None
        if json_record['name'] in WEAPONS_MISSING:
            print("Error: Weapon", json_record['name'], "was previously not available in gowdb.com")
        if 'count' not in json_record:
            json_record['count'] = 0
        if 'traitCount' not in json_record:
            json_record['traitCount'] = 0

        self = cls(name=json_record['name'],
                   count=json_record['count'],
                   rarity=json_record['rarityId'],
                   kingdom=json_record['kingdomName'],
                   traitcount=json_record['traitCount'],
                   )
        return self

    @staticmethod
    def get_csv_header():
        """
        Returns a string which can be written to a csv file (creates a header row)
        """
        return "Name,Count,Traits,Kingdom,Rarity,Paid"

    def get_csv_record(self):
        """
        Returns a string which can be written to a csv file (creates a row for this class)
        """
        return self._vals['name'] + "," + str(self._vals['count']) + ","\
               + str(self._vals['traitcount']) + "," + self._vals['kingdom'] + ","\
               + str(self._vals['rarity']) + "," + str(self._vals['paid'])

    def print(self):
        """
        Prints Weapon information
        """
        # TODO Add a better print function
        print(self._vals['name'])

    @staticmethod
    def print_weapon_csv(csv_file_name, weapon_array):
        """
        Helper function to create a full csv file with weapon information

        :param csv_file_name: filename for the csv file
        :param weapon_array:   array of weapons to print
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write(Weapon.get_csv_header())
            csv_file.write("\n")
            for weapon in weapon_array:
                if weapon is not None:
                    csv_file.write(weapon.get_csv_record())
                    csv_file.write("\n")

    def is_max(self):
        """

        :return:
        """
        if TRAITS_TO_MAX[self._vals['rarity']] == self._vals['traitcount']:
            return True
        return False

    def get_kingdom(self):
        """
        Retrieve the kingdom for this weapon
        """
        return self._vals['kingdom']

    def get_rarity(self):
        """
        Retrieve the base rarity for this weapon
        """
        return self._vals['rarity']

    def get_traitcount(self):
        """
        Retrieve the trait count for this weapon
        """
        return self._vals['traitcount']

    def get_count(self):
        """
        Retrieve the count for this weapon
        """
        return self._vals['count']
