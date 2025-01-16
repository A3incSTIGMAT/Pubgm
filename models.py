class Item:
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type
        self.value = value

class Weapon(Item):
    def __init__(self, name, damage, value):
        super().__init__(name, "weapon", value)
        self.damage = damage

class Armor(Item):
    def __init__(self, name, defense, value):
        super().__init__(name, "armor", value)
        self.defense = defense

# Пример оружия и брони
weapons = [
    Weapon("AK-47", 35, 100),
    Weapon("M16", 30, 90),
]

armors = [
    Armor("Helmet", 15, 50),
    Armor("Bulletproof Vest", 20, 120),
]

items = weapons + armors
