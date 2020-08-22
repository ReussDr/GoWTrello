class Traitstones:
    def __init__(self):
        self._traitstones = {
            'Minor Water Traitstone': 0,
            'Minor Nature Traitstone': 0,
            'Minor Fire Traitstone': 0,
            'Minor Wind Traitstone': 0,
            'Minor Magic Traitstone': 0,
            'Minor Earth Traitstone': 0,
            'Major Water Traitstone': 0,
            'Major Nature Traitstone': 0,
            'Major Fire Traitstone': 0,
            'Major Wind Traitstone': 0,
            'Major Magic Traitstone': 0,
            'Major Earth Traitstone': 0,
            'Runic Water Traitstone': 0,
            'Runic Nature Traitstone': 0,
            'Runic Fire Traitstone': 0,
            'Runic Wind Traitstone': 0,
            'Runic Magic Traitstone': 0,
            'Runic Earth Traitstone': 0,
            'Arcane Stoic Traitstone': 0,
            'Arcane Swamp Traitstone': 0,
            'Arcane Blood Traitstone': 0,
            'Arcane Blade Traitstone': 0,
            'Arcane Spirit Traitstone': 0,
            'Arcane Shield Traitstone': 0,
            'Arcane Stealth Traitstone': 0,
            'Arcane Beast Traitstone': 0,
            'Arcane Light Traitstone': 0,
            'Arcane Venom Traitstone': 0,
            'Arcane Forest Traitstone': 0,
            'Arcane Rage Traitstone': 0,
            'Arcane Storm Traitstone': 0,
            'Arcane Dark Traitstone': 0,
            'Arcane Lava Traitstone': 0,
            'Arcane Summer Traitstone': 0,
            'Arcane Plains Traitstone': 0,
            'Arcane Mountain Traitstone': 0,
            'Arcane Death Traitstone': 0,
            'Arcane Skull Traitstone': 0,
            'Arcane Deep Traitstone': 0,
            'Celestial Traitstone': 0,
        }

    def add_traitstone(self, name, count):
        if name not in self._traitstones:
            print("Error:", name, "not a valid traitstone type")
        else:
            self._traitstones[name] += count

    def print(self):
        print(self._traitstones)

    def print_csv(self, csv_file_name):
        with open(csv_file_name, "w") as csv_file:
            for stone in self._traitstones:
                csv_file.write(stone + ",")
                csv_file.write(str(self._traitstones[stone]) + "\n")
