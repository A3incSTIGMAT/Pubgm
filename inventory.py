# inventory.py

# Классы для оружия и брони
class Weapon:
    def __init__(self, name, damage, cost, weapon_type):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.weapon_type = weapon_type

class Armor:
    def __init__(self, name, defense, cost, armor_type):
        self.name = name
        self.defense = defense
        self.cost = cost
        self.armor_type = armor_type

# Класс инвентаря
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def show_inventory(self):
        return [item.name for item in self.items]

