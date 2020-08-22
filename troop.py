"""
Module for Troop class (for Gems of War Data)
"""

import gems_common

class Troop:
    """
    Troop class to hold data about Gems of War Troops
    """
    def __init__(self, name, count, base_rarity, ascended_rarity, kingdom, traitcount, level):
        self._vals = {}
        self._vals['name'] = name
        self._vals['count'] = count
        self._vals['base_rarity'] = base_rarity
        self._vals['curr_rarity'] = ascended_rarity
        self._vals['traitcount'] = traitcount
        self._vals['level'] = level
        self._vals['kingdom'] = ""
        self._vals['faction'] = ""

        if gems_common.is_kingdom(kingdom):
            self._vals['kingdom'] = kingdom
        elif gems_common.is_faction(kingdom):
            self._vals['faction'] = kingdom
            self._vals['kingdom'] = gems_common.lookup_kingdom_from_faction(kingdom)
        elif gems_common.is_non_kingdom(kingdom):
            self._vals['kingdom'] = kingdom
        else:
            print("Error: Couldn't find kingdom:", kingdom)
        self._vals['count_needed'] = gems_common.troops_needed_to_mythic(self._vals['base_rarity'],
                                                                         self._vals['curr_rarity'],
                                                                         self._vals['count'])

    @classmethod
    def gen_troop_from_json(cls, json_record):
        """
        Alternate constructor.  Allows you pass in a json_record, and it'll parse all the data out

        :param json_record: The json record (from gowdb inventory)
        :return:            The constructed Troop object
        """
        if 'count' not in json_record:
            json_record['count'] = 0
        if 'traitCount' not in json_record:
            json_record['traitCount'] = 0
        if 'level' not in json_record:
            json_record['level'] = 1
        if 'ascensionRarityId' not in json_record:
            json_record['ascensionRarityId'] = json_record['rarityId']

        self = cls(name=json_record['name'],
                   count=json_record['count'],
                   base_rarity=json_record['rarityId'],
                   ascended_rarity=json_record['ascensionRarityId'],
                   kingdom=json_record['kingdomName'],
                   traitcount=json_record['traitCount'],
                   level=json_record['level'])
        return self

    @staticmethod
    def get_csv_header():
        """
        Returns a string which can be written to a csv file (creates a header row)
        """
        return "Name,Level,Count,Needed,Traits,Kingdom,Faction,BaseRarity,AscendedRarity"

    def get_csv_record(self):
        """
        Returns a string which can be written to a csv file (creates a row for this troop)
        """
        return self._vals['name'] + "," + str(self._vals['level']) + ","\
               + str(self._vals['count']) + "," + str(self._vals['count_needed']) + ","\
               + str(self._vals['traitcount']) + ","\
               + self._vals['kingdom'] + "," + self._vals['faction'] + ","\
               + str(self._vals['base_rarity']) + "," + str(self._vals['curr_rarity'])

    def print(self):
        """
        Prints Troop information
        """
        # TODO Add a better print function
        print(self._vals['name'])

    @staticmethod
    def print_troop_csv(csv_file_name, troop_array):
        """
        Helper function to create a full csv file with troop information

        :param csv_file_name: filename for the csv file
        :param troop_array:   array of troops to print
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write(Troop.get_csv_header())
            csv_file.write("\n")
            for troop in troop_array:
                csv_file.write(troop.get_csv_record())
                csv_file.write("\n")

    def get_kingdom(self):
        """
        Retrieve the kingdom for this troop
        """
        return self._vals['kingdom']

    def get_faction(self):
        """
        Retrieve the faction for this troop
        """
        return self._vals['faction']

    def get_base_rarity(self):
        """
        Retrieve the base rarity for this troop
        """
        return self._vals['base_rarity']

    def get_curr_rarity(self):
        """
        Retrieve the current rarity for this troop
        """
        return self._vals['curr_rarity']

    def get_traitcount(self):
        """
        Retrieve the trait count for this troop
        """
        return self._vals['traitcount']

    def get_count(self):
        """
        Retrieve the count for this troop
        """
        return self._vals['count']
