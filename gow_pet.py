"""
Module for Pet Class
"""
import gow_common

PETS_RESCUEABLE = [
    "Auraio",
    "Baby Beard",
    "Beelz",
    "Billy Kid",
    "Black Beast-kin",
    "Bright Beetle",
    "Chomp Chomp Chomp",
    "Crabbie",
    "Crimson Batling",
    "Dawn Bird",
    "Eyelet",
    "Falabella",
    "Fennekit",
    "Feyrie",
    "Flutter",
    "Gargurgle",
    "Giantini",
    "Gobblekin",
    "Griffling",
    "Grimlet",
    "Guppy",
    "Hairy Hoarder",
    "Hellpuppy",
    "Hot Head",
    "Itty Bitty Yeti",
    "Kit Sith",
    "Leafette",
    "Lil' Kerby",
    "Little Lupus",
    "Lucky",
    "Magmapillar",
    "Manticub",
    "Martlet",
    "Minfernus",
    "Mini Maw",
    "Mini Mimic",
    "Mini Moa",
    "Minishroom",
    "Minitaur",
    "Moon Moon",
    "Ogrikin",
    "Owlbunny",
    "Peace Pigeon",
    "Pegaset",
    "Pinguin",
    "Puddling",
    "Puppybot",
    "Rocki",
    "Rockweiler",
    "Sacred Cub",
    "Shortlong",
    "Shrunken Head",
    "Shrynx",
    "Shymera",
    "Sir Botlet IV",
    "Slimeball",
    "Smallpaca",
    "Snakelet",
    "Snow Bunny",
    "Snowball",
    "Spiderling",
    "Squidlet",
    "Swampie",
    "Tanglebush",
    "Tinycorn",
    "Tiny Tentacle",
    "Toy Soldier",
    "Trogpole",
    "Twigant",
    "Urskine",
    "Weenie Wyvern",
    "Whelp",
    "Wimp",
    "Wyrmling",
]

PETS_FACTION = [
    "Bin Chicken",
    "Bonicorn",
    "Bulb-Biter",
    "Cactnid Kid",
    "Dark Helmut",
    "Dinotaur",
    "Dire Rose",
    "Dr. Sno",
    "Eye Pod",
    "Frog Prince",
    "Hamsterthalamus",
    "Hare-o-Plane",
    "Itsy Bitsy Drider",
    "Joust Mouse",
    "Kobold Kitty",
    "Mephisquideles",
    "Minirino",
    "Miniskito",
    "Minito Mori",
    "Minnow",
    "Mirror Mimic",
    "Pet-o-bot",
    "Rattlebone",
    "Sad Panda",
    "Semi Deminaga",
    "Sir Ted",
    "Tiny Dancer",
]

PETS_COSMETIC = [
    "<3",
    "Bat Cat",
    "Bunnilope",
    "Bunny Chick",
    "Compact Cookie",
    "Dragonkitty",
    "Dragonpuppy",
    "Hoglet",
    "Holiday Shrub",
    "Hoodoo Doll",
    "Howler",
    "Kurandarito",
    "Lamplet",
    "Lil' Freedom",
    "Little Bang",
    "Love Panda",
    "Lucky Ox",
    "Mask-supial",
    "McMimic",
    "Micro Muffin",
    "Micro Muffin X",
    "Mimicophagus",
    "Ninja Cat",
    "Ozzie",
    "Prancer",
    "Puppy Pirate",
    "Quetzantini",
    "Rat of Fortune",
    "Revered Dragonkitty",
    "Sharki",
    "Shelf on an Elf",
    "Skullbeak",
    "Spell Spaniel",
    "Tailchaser",
    "Tiny Torte",
    "Uncalico Jack",
    "Urskoala",
    "Valentiny",
    "War Corgi",
    "X-Ball",
]

PETS_UNOBTAINABLE = [
    "Droid-bot",    # Android Exclusive
    "Mei",          # Cosmetic, Unknown Source
    "Steam Puppy",  # Steam Exclusive
]

# List of Pets, current not listed in gowdb.com
PETS_MISSING = {
    "Tail Chaser":          "Pridelands",
    "Kuranarito":           "Urskaya",
}


class Pet:
    """
    Pet class for Gems of War
    """
    def __init__(self, name, count, rarity, kingdom, level):
        self._vals = {}
        self._vals['name'] = name
        self._vals['count'] = count
        self._vals['rarity'] = rarity
        self._vals['kingdom'] = kingdom
        self._vals['level'] = level
        if kingdom not in gow_common.KINGDOM_FACTION_MAP and \
                kingdom not in gow_common.NON_KINGDOMS:
            print("Error: Can't find kingdom for", name)
        self._vals['source'] = self.get_pet_type(name)
        if self._vals['source'] == "Unknown":
            print("Error: Can't find source for", name)
        self._vals['count_needed'] = gow_common.pets_needed_to_mythic(3,
                                                                      self._vals['rarity'],
                                                                      self._vals['count'])

    @classmethod
    def gen_pet_from_json(cls, json_record):
        """
        Alternate constructor.  Allows you pass in a json_record, and it'll parse all the data out

        :param json_record: The json record (from gowdb inventory)
        :return:            The constructed Pet object
        """
        if json_record['name'] in PETS_UNOBTAINABLE:
            return None
        if json_record['name'] in PETS_MISSING:
            print("Error: Pet", json_record['name'], "was previously not available in gowdb.com")
        if 'count' not in json_record:
            json_record['count'] = 0
        if 'level' not in json_record:
            json_record['level'] = 1

        self = cls(name=json_record['name'],
                   count=json_record['count'],
                   rarity=json_record['ascensionRarityId'],
                   kingdom=json_record['kingdomName'],
                   level=json_record['level'])
        return self

    @staticmethod
    def get_csv_header():
        """
        Returns a string which can be written to a csv file (creates a header row)
        """
        return "Name,Level,Count,Needed,Kingdom,Rarity,Source"

    def get_csv_record(self):
        """
        Returns a string which can be written to a csv file (creates a row for this pet)
        """
        return self._vals['name'] + "," + str(self._vals['level']) + ","\
               + str(self._vals['count']) + "," + str(self._vals['count_needed']) + ","\
               + self._vals['kingdom'] + ","\
               + str(self._vals['rarity']) + "," + self._vals['source']

    def print(self):
        """
        Prints Pet information
        """
        # TODO Add a better print function
        print(self._vals['name'])

    @staticmethod
    def print_pet_csv(csv_file_name, pet_array):
        """
        Helper function to create a full csv file with pet information

        :param csv_file_name: filename for the csv file
        :param pet_array:     array of pets to print
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write(Pet.get_csv_header())
            csv_file.write("\n")
            for pet in pet_array:
                if pet is not None:
                    csv_file.write(pet.get_csv_record())
                    csv_file.write("\n")

    @staticmethod
    def get_pet_type(name):
        """
        Return whether the pet is obtained through Delves, Rescues or is Cosmetic

        :param name: name of the pet
        :return:     Delve/Rescueable/Cosmetic
        """
        if name in PETS_FACTION:
            return "Delve"
        if name in PETS_RESCUEABLE:
            return "Rescuable"
        if name in PETS_COSMETIC:
            return "Cosmetic"
        return "Unknown"

    def get_kingdom(self):
        """
        Retrieve the kingdom for this pet
        """
        return self._vals['kingdom']

    def get_count(self):
        """
        Retrieve the count for this pet
        """
        return self._vals['count']

    def get_level(self):
        """
        Retrieve the level for this pet
        """
        return self._vals['level']
