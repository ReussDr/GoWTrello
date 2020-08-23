"""
Module for Pet Class
"""
import gems_common

PETS_RESCUEABLE = [
    "Auraio",
    "Baby Beard",
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
    "Griffling",
    "Grimlet",
    "Guppy",
    "Hellpuppy",
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
    "Dire Rose",
    "Dr. Sno",
    "Eye Pod",
    "Frog Prince",
    "Hamsterthalamus",
    "Hare-o-Plane",
    "Joust Mouse",
    "Minirino",
    "Miniskito",
    "Minito Mori",
    "Minnow",
    "Mirror Mimic",
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
    "Dragonkitty",
    "Dragonpuppy",
    "Hoglet",
    "Holiday Shrub",
    "Hoodoo Doll",
    "Kurandarito",
    "Lil' Freedom",
    "Little Bang",
    "Mask-supial",
    "McMimic",
    "Micro Muffin",
    "Micro Muffin X",
    "Ninja Cat",
    "Prancer",
    "Puppy Pirate",
    "Rat of Fortune",
    "Sharki",
    "Skullbeak",
    "Tailchaser",
    "Tiny Torte",
    "Urskoala",
    "Valentiny",
    "War Corgi",
    "X-Ball",
]


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
        if kingdom not in gems_common.KINGDOM_FACTION_MAP and \
                kingdom not in gems_common.NON_KINGDOMS:
            print("Error: Can't find kingdom for", name)
        self._vals['source'] = self.get_pet_type(name)
        if self._vals['source'] == "Unknown":
            print("Error: Can't find source for", name)
        self._vals['count_needed'] = gems_common.pets_needed_to_mythic(3,
                                                                       self._vals['rarity'],
                                                                       self._vals['count'])

    @classmethod
    def gen_pet_from_json(cls, json_record):
        """
        Alternate constructor.  Allows you pass in a json_record, and it'll parse all the data out

        :param json_record: The json record (from gowdb inventory)
        :return:            The constructed Pet object
        """
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

    def get_rarity(self):
        """
        Retrieve the rarity for this pet
        """
        return self._vals['rarity']

    def get_curr_rarity(self):
        """
        Retrieve the current rarity for this pet
        """
        return self._vals['curr_rarity']

    def get_count(self):
        """
        Retrieve the count for this pet
        """
        return self._vals['count']
