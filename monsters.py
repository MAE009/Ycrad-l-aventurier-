# monsters.py - Système de monstres et boss
class Monster:
    def __init__(self, monster_type, level, position):
        self.type = monster_type
        self.name = monster_type.capitalize()
        self.level = level
        self.position = position
        self.hp = self.max_hp = 20 + (level * 10)
        self.damage = 5 + level
        self.xp_reward = 10 + (level * 5)
        self.gold_reward = 5 + level
        self.loot_table = []
    
    def take_damage(self, damage):
        self.hp -= damage
        return damage
    
    def attack(self, target):
        damage = self.damage
        return target.take_damage(damage)
    
    def generate_loot(self):
        # Générer du loot aléatoire basé sur la table de butin
        import random
        loot = []
        for item, chance in self.loot_table:
            if random.random() < chance:
                loot.append(item)
        return loot

class Slime(Monster):
    def __init__(self, level, position):
        super().__init__("slime", level, position)
        self.hp = self.max_hp = 15 + (level * 8)
        self.damage = 3 + level
        self.loot_table = [("Gelée visqueuse", 0.7), ("Petite potion", 0.3)]

class Rat(Monster):
    def __init__(self, level, position):
        super().__init__("rat", level, position)
        self.hp = self.max_hp = 12 + (level * 6)
        self.damage = 4 + level
        self.loot_table = [("Queue de rat", 0.5), ("Fromage volé", 0.2)]

class Boss(Monster):
    def __init__(self, boss_name, level, position):
        super().__init__(boss_name, level, position)
        self.hp = self.max_hp = 100 + (level * 50)
        self.damage = 15 + (level * 3)
        self.xp_reward = 100 + (level * 25)
        self.gold_reward = 50 + (level * 10)
        self.special_attacks = []
    
    def use_special_attack(self, target):
        # Logique pour les attaques spéciales des boss
        pass

class Korvash(Boss):
    def __init__(self, level, position):
        super().__init__("Korvash le Dévoreur", level, position)
        self.loot_table = [("Épée maudite", 0.4), ("Amulette des marais", 0.6)]
        self.special_attacks = ["Empoisonnement", "Étreinte mortelle"]
