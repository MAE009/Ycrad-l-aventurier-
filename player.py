# player.py - Classe du joueur et système de classes
class Player:
    def __init__(self, name, starting_class):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.position = [400, 300]  # Position initiale
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.inventory = []
        self.gold = 50
        
        # Système de classes
        self.classes = {
            "warrior": Warrior(),
            "archer": Archer(),
            "mage": Mage(),
            "thief": Thief()
        }
        self.current_class = self.classes[starting_class]
        self.skills = self.current_class.skills
        
    def move(self, dx, dy):
        self.position[0] += dx * 3  # Vitesse de déplacement
        self.position[1] += dy * 3
    
    def attack(self, target):
        damage = self.current_class.calculate_damage(self)
        target.take_damage(damage)
        return damage
    
    def take_damage(self, damage):
        # Réduire les dégâts en fonction de l'armure
        actual_damage = max(1, damage - (self.equipment["armor"].defense if self.equipment["armor"] else 0))
        self.hp -= actual_damage
        return actual_damage
    
    def use_skill(self, skill_index, target):
        if skill_index < len(self.skills):
            skill = self.skills[skill_index]
            if self.mp >= skill.mp_cost:
                self.mp -= skill.mp_cost
                return skill.use(self, target)
        return 0
    
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Amélioration des stats selon la classe
        self.max_hp += self.current_class.hp_growth
        self.max_mp += self.current_class.mp_growth
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Apprentissage de nouvelles compétences
        if self.level in self.current_class.skill_levels:
            new_skill = self.current_class.skill_levels[self.level]
            self.skills.append(new_skill)
    
    def change_class(self, new_class):
        if new_class in self.classes:
            self.current_class = self.classes[new_class]
            # Conserver les compétences de base mais adapter aux nouvelles
            self.skills = [self.current_class.basic_skill] + self.skills[1:]

class Class:
    def __init__(self, name, hp_growth, mp_growth, damage_multiplier):
        self.name = name
        self.hp_growth = hp_growth
        self.mp_growth = mp_growth
        self.damage_multiplier = damage_multiplier
        self.skills = []
        self.skill_levels = {}
        self.basic_skill = None
    
    def calculate_damage(self, player):
        base_damage = player.equipment["weapon"].damage if player.equipment["weapon"] else 5
        return int(base_damage * self.damage_multiplier)

class Warrior(Class):
    def __init__(self):
        super().__init__("Guerrier", 20, 5, 1.2)
        self.basic_skill = Skill("Coup d'épée", 0, 10)
        self.skills = [self.basic_skill]
        self.skill_levels = {
            3: Skill("Coup puissant", 10, 25),
            5: Skill("Cri de guerre", 15, 0)  # 0 dégâts mais effet de statut
        }

class Archer(Class):
    def __init__(self):
        super().__init__("Archer", 10, 10, 1.0)
        self.basic_skill = Skill("Tir rapide", 5, 8)
        self.skills = [self.basic_skill]
        self.skill_levels = {
            3: Skill("Tir multiple", 15, 6),  # Multi-cibles
            5: Skill("Flèche empoisonnée", 20, 10)  # Dégâts sur le temps
        }

class Mage(Class):
    def __init__(self):
        super().__init__("Mage", 5, 20, 0.8)
        self.basic_skill = Skill("Boule de feu", 10, 15)
        self.skills = [self.basic_skill]
        self.skill_levels = {
            3: Skill("Éclair", 15, 20),
            5: Skill("Barrière magique", 20, 0)  # Protection
        }

class Thief(Class):
    def __init__(self):
        super().__init__("Voleur", 8, 12, 1.1)
        self.basic_skill = Skill("Coup furtif", 5, 12)
        self.skills = [self.basic_skill]
        self.skill_levels = {
            3: Skill("Attaque surprise", 10, 18),
            5: Skill("Vol à la tire", 0, 5)  # Dégâts + vol d'or
        }

class Skill:
    def __init__(self, name, mp_cost, base_damage):
        self.name = name
        self.mp_cost = mp_cost
        self.base_damage = base_damage
    
    def use(self, user, target):
        damage = self.base_damage + (user.level * 2)
        target.take_damage(damage)
        return damage
