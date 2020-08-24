"""
A class for accumulating statistics about Kingdoms
"""
import gow_common

MAX_POWER_TROOP_TRAITS = {
    4: 3,
    7: 5,
    11: 7,
    16: 9,
    21: 12,
    23: 14,
    25: 16,
    27: 18,
    29: 20,
    31: 22,
    33: 24,
    35: 26,
    37: 28,
    39: 30,
}

MAX_POWER_TROOP_LEVEL20 = {
    18: 10,
    20: 11,
    22: 13,
    24: 15,
    26: 17,
    28: 19,
    30: 21,
    32: 23,
    34: 25,
    36: 27,
    38: 29,
}

MAX_POWER_TROOP_MYTHIC = {
    1: 10,
    2: 22,
}

MAX_POWER_WEAPON_OWNED = {
    1: 3,
    3: 7,
    4: 12,
}

MAX_POWER_WEAPON_MAXED = {
    1: 5,
    2: 8,
    3: 14,
    4: 16,
    6: 18,
    8: 20,
    10: 24,
    12: 26,
    14: 28,
}


class KingdomStats:
    """
    A class to accumulate Kingdom Statistics
    """
    def __init__(self):
        # Start with a dictionary of all the Kingdoms just to make things easier
        self._totals = gow_common.KINGDOM_FACTION_MAP
        for kingdom in self._totals:
            faction = self._totals[kingdom]
            self._totals[kingdom] = {}
            self._totals[kingdom]['faction'] = faction

            # Troop Variables
            self._totals[kingdom]['mythic'] = False
            self._totals[kingdom]['total_troops'] = 0
            self._totals[kingdom]['owned_troops'] = 0
            self._totals[kingdom]['fully_traited_troops'] = 0
            self._totals[kingdom]['mythic_troops'] = 0
            self._totals[kingdom]['level_20_troops'] = 0
            self._totals[kingdom]['faction_fully_traited_troops'] = 0
            self._totals[kingdom]['faction_mythic_troops'] = 0

            # Pet Variables
            self._totals[kingdom]['total_pets'] = 0
            self._totals[kingdom]['owned_pets'] = 0
            self._totals[kingdom]['max_pet_level'] = 0
            self._totals[kingdom]['maxed_pets'] = 0

            # Weapon Variables
            self._totals[kingdom]['total_weapons'] = 0
            self._totals[kingdom]['owned_weapons'] = 0
            self._totals[kingdom]['maxed_weapons'] = 0


    def add_troop(self, troop):
        """
        Add a troop to Kingdom Stats

        :param troop: Troop to add
        """
        kingdom = troop.get_kingdom()

        # If it's not a Kingdom Proper, return
        if gow_common.is_non_kingdom(kingdom):
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
        if troop.get_level() == 20:
            self._totals[kingdom]['level_20_troops'] += 1

    def add_pet(self, pet):
        """
        Add a pet to Kingdom Stats

        :param pet: pet to add
        """
        kingdom = pet.get_kingdom()

        # If it's not a Kingdom Proper, return
        if gow_common.is_non_kingdom(kingdom):
            return

        self._totals[kingdom]['total_pets'] += 1
        if pet.get_count() > 0:
            self._totals[kingdom]['owned_pets'] += 1
        if pet.get_level() == 20:
            self._totals[kingdom]['maxed_pets'] += 1
        if pet.get_level() > self._totals[kingdom]['max_pet_level']:
            self._totals[kingdom]['max_pet_level'] = pet.get_level()

    def add_class(self, gow_class):
        """
        Add a class to Kingdom Stats

        :param gow_class: class to add
        """
        kingdom = gow_class.get_kingdom()

        # If it's not a Kingdom Proper, return
        if gow_common.is_non_kingdom(kingdom):
            return

        self._totals[kingdom]['class_name'] = gow_class.get_name()
        self._totals[kingdom]['class_level'] = gow_class.get_level()
        self._totals[kingdom]['class_sublevel'] = gow_class.get_sublevel()
        self._totals[kingdom]['class_traitcount'] = gow_class.get_traitcount()

    def add_weapon(self, weapon):
        """
        Add a weapon to Kingdom Stats
        :param weapon: weapon to add
        """
        kingdom = weapon.get_kingdom()

        # If it's not a Kingdom Proper, return
        if gow_common.is_non_kingdom(kingdom):
            return

        self._totals[kingdom]['total_weapons'] += 1
        if weapon.get_count() == 1:
            self._totals[kingdom]['owned_weapons'] += 1
        if weapon.is_max():
            self._totals[kingdom]['maxed_weapons'] += 1

    def print_csv(self, csv_file_name):
        """
        Print the Kingdom Stats to a csv file
        :param csv_file_name: name of the csv file
        """
        with open(csv_file_name, "w") as csv_file:
            csv_file.write("Kingdom,Faction,Mythic,Total Troops,Owned Troops,3x Traited Troops,")
            csv_file.write("Mythic Troops,Level 20 Troops,Faction 3x Traited Troops,Faction Mythic Troops,")
            csv_file.write("Total Pets,Owned Pets,Max Pet Level,Maxed Pets,")
            csv_file.write("Class Name,Level,Sublevel,Traitcount,")
            csv_file.write("Total Weapons,Owned Weapons,Maxed Weapons,")
            csv_file.write("Max Power Troop Trait,Max Power Troop Level 20,Max Power Weapon Owned\n")
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
                csv_file.write(str(self._totals[kingdom]['level_20_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['faction_fully_traited_troops']) + ",")
                csv_file.write(str(self._totals[kingdom]['faction_mythic_troops']) + ",")

                # Write Pet information
                csv_file.write(str(self._totals[kingdom]['total_pets']) + ",")
                csv_file.write(str(self._totals[kingdom]['owned_pets']) + ",")
                csv_file.write(str(self._totals[kingdom]['max_pet_level']) + ",")
                csv_file.write(str(self._totals[kingdom]['maxed_pets']) + ",")

                # Write Class information
                csv_file.write(self._totals[kingdom]['class_name'] + ",")
                csv_file.write(str(self._totals[kingdom]['class_level']) + ",")
                csv_file.write(str(self._totals[kingdom]['class_sublevel']) + ",")
                csv_file.write(str(self._totals[kingdom]['class_traitcount']) + ",")

                # Write Weapon information
                csv_file.write(str(self._totals[kingdom]['total_weapons']) + ",")
                csv_file.write(str(self._totals[kingdom]['owned_weapons']) + ",")
                csv_file.write(str(self._totals[kingdom]['maxed_weapons']) + ",")

                # Write Power Level Max
                max_power_troop_trait = 30
                for level in reversed(MAX_POWER_TROOP_TRAITS):
                    if self._totals[kingdom]['fully_traited_troops'] < level:
                        max_power_troop_trait = MAX_POWER_TROOP_TRAITS[level] - 1
                csv_file.write(str(max_power_troop_trait) + ",")

                max_power_troop_level20 = 0
                for level in reversed(MAX_POWER_TROOP_LEVEL20):
                    if self._totals[kingdom]['level_20_troops'] < level:
                        max_power_troop_level20 = MAX_POWER_TROOP_LEVEL20[level] - 1
                csv_file.write(str(max_power_troop_level20) + ",")

                max_power_weapon_owned = 30
                for level in reversed(MAX_POWER_WEAPON_OWNED):
                    if self._totals[kingdom]['owned_weapons'] < level:
                        max_power_weapon_owned = MAX_POWER_WEAPON_OWNED[level] - 1
                csv_file.write(str(max_power_weapon_owned) + ",")

                csv_file.write("\n")
