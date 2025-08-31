# inventory.py - Système d'inventaire et d'équipement
class Item:
    def __init__(self, name, item_type, description, value, **kwargs):
        self.name = name
        self.type = item_type  # weapon, armor, consumable, etc.
        self.description = description
        self.value = value
        
        # Attributs spécifiques selon le type
        for key, value in kwargs.items():
            setattr(self, key, value)

class Inventory:
    def __init__(self):
        self.items = []
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.max_size = 20
        self.is_open = False
    
    def add_item(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def equip(self, item):
        if item in self.items and item.type in self.equipped:
            # Déséquiper l'item actuel s'il y en a un
            if self.equipped[item.type]:
                self.unequip(item.type)
            
            self.equipped[item.type] = item
            self.items.remove(item)
    
    def unequip(self, slot):
        if self.equipped[slot]:
            self.items.append(self.equipped[slot])
            self.equipped[slot] = None
    
    def toggle(self):
        self.is_open = not self.is_open
    
    def use_consumable(self, item, target):
        if item in self.items and item.type == "consumable":
            effect = item.effect
            if hasattr(target, effect["attribute"]):
                current_value = getattr(target, effect["attribute"])
                setattr(target, effect["attribute"], min(
                    getattr(target, "max_" + effect["attribute"], current_value + effect["amount"]),
                    current_value + effect["amount"]
                ))
            self.remove_item(item)
