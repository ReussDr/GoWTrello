#TODO Move rarity lookup to common
RARITY_LOOKUP = ["Zero",
                 "Common",
                 "Rare",
                 "Ultra-Rare",
                 "Epic",
                 "Legendary",
                 "Mythic"]


class Troop:
    def __init__(self, name, count, base_rarity, ascended_rarity, kingdom, traitcount, level):
        self._name = name
        self._count = count
        self._base_rarity = base_rarity
        self._ascended_rarity = ascended_rarity
        self._kingdom = kingdom
        self._traitcount = traitcount
        self._level = level
        #TODO Faction
        #self._faction = faction

    @classmethod
    def gen_troop_from_json(cls, json_record):
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
        return "Name,Level,Count,Traits,Kingdom,BaseRarity,AscendedRarity"

    def get_csv_record(self):
        return self._name + "," + str(self._level) + "," + str(self._count) + ","\
               + str(self._traitcount) + "," + self._kingdom + ","\
               + str(self._base_rarity) + "," + str(self._ascended_rarity)

    def print(self):
        # TODO Add a better print function
        print(self._name)

    @staticmethod
    def print_troop_csv(csv_file_name, troop_array):
        with open(csv_file_name, "w") as csv_file:
            csv_file.write(Troop.get_csv_header())
            csv_file.write("\n")
            for troop in troop_array:
                csv_file.write(troop.get_csv_record())
                csv_file.write("\n")
