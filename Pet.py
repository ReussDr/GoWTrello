PETS_RESCUEABLE = ["Mini Mimic"]
PETS_FACTION = []
PETS_COSMETIC = ['X-Ball']
RARITY_LOOKUP = ["Zero",
                 "Common",
                 "Rare",
                 "Ultra-Rare",
                 "Epic",
                 "Legendary",
                 "Mythic"]


class Pet:
    def __init__(self, name, count, rarity):
        self._name = name
        self._count = count
        self._rarity = rarity

    def add_traitstone(self, name, count):
        if name not in self._traitstones:
            print("Error:", name, "not a valid traitstone type")
        else:
            self._traitstones[name] += count
            print(name, count, self._traitstones[name])

    def print(self):
        print(self._traitstones)

