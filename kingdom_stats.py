"""
A class for accumulating statistics about Kingdoms
"""
import gems_common


class KingdomStats:
    """
    A class to accumulate Kingdom Statistics
    """
    def __init__(self):
        # Start with a dictionary of all the Kingdoms just to make things easier
        self._totals = gems_common.KINGDOM_FACTION_MAP
        for kingdom in self._totals:
            faction = self._totals[kingdom]
            self._totals[kingdom] = {}
            self._totals[kingdom]['faction'] = faction
            self._totals[kingdom]['mythic'] = False
            self._totals[kingdom]['total_troops'] = 0
            self._totals[kingdom]['owned_troops'] = 0
            self._totals[kingdom]['fully_traited_troops'] = 0
            self._totals[kingdom]['mythic_troops'] = 0
            self._totals[kingdom]['faction_fully_traited_troops'] = 0
            self._totals[kingdom]['faction_mythic_troops'] = 0


    def add_troop(self, troop):
        """
        Add a troop to Kingdom Stats

        :param troop: Troop to add
        """
        kingdom = troop.get_kingdom()

        # If it's not a Kingdom Proper, return
        if gems_common.is_non_kingdom(kingdom):
            return

        self._totals[kingdom]['total_troops'] += 1
        if troop.get_count() > 0:
            self._totals[kingdom]['owned_troops'] += 1
        if troop.get_base_rarity() == 6 and troop.get_count() > 0:
            self._totals[kingdom]['mythic'] = True
        if troop.get_traitcount() == 3:
            self._totals[kingdom]['fully_traited_troops'] += 1
            if troop.get_faction() != "":
                self._totals[kingdom]['faction_fully_traited_troops'] += 1
        if troop.get_curr_rarity() == 6 and troop.get_count() > 0:
            self._totals[kingdom]['mythic_troops'] += 1
            if troop.get_faction() != "":
                self._totals[kingdom]['faction_mythic_troops'] += 1

        #print(self._totals[kingdom])

    def print_csv(self, csv_file_name):
        """
        Print the Kingdom Stats to a csv file
        :param csv_file_name: name of the csv file
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write("Kingdom,Faction,Mythic,Total Troops,Owned Troops,3x Traited Troops,")
            csv_file.write("Mythic Troops,Faction 3x Traited Troops,Faction Mythic Troops\n")
            for kingdom in self._totals:
                csv_file.write(kingdom + ",")
                csv_file.write(self._totals[kingdom]['faction'] + ",")
                if self._totals[kingdom]['mythic']:
                    csv_file.write("yes,")
                else:
                    csv_file.write("no,")
                csv_file.write(str(self._totals[kingdom]['total_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['owned_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['fully_traited_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['mythic_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['faction_fully_traited_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['faction_mythic_troops']) + ",")
                csv_file.write("\n")
