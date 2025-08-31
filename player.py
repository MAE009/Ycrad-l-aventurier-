# player.py - Système de joueur avancé avec classes et compétences
import pygame
import math

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
        self.position = [400, 300]
        self.speed = 3.0
        self.is_moving = False
        self.direction = "down"  # down, up, left, right
        self.gold = 50
        
        # Équipement
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        # Inventaire
        self.inventory = []
        self.max_inventory_size = 20
        
        # Système de classes
        self.classes = {
            "warrior": Warrior(),
            "archer": Archer(),
            "mage": Mage(),
            "thief": Thief()
        }
        self.current_class = self.classes[starting_class]
        self.skills = self.current_class.get_skills_for_level(1)
        
        # Stats de base
        self.stats = {
            "strength": 10,
            "dexterity": 10,
            "intelligence": 10,
            "defense": 5,
            "critical_chance": 0.05,
            "critical_multiplier": 1.5
        }
        
        # Cooldowns des compétences
        self.skill_cooldowns = {}
    
    def update(self, control_system, environment, npcs, dt):
        """Met à jour le joueur avec les entrées de contrôle"""
        dx, dy = control_system.get_movement_vector()
        
        # Mettre à jour la direction
        if dx > 0: self.direction = "right"
        elif dx < 0: self.direction = "left"
        if dy > 0: self.direction = "down"
        elif dy < 0: self.direction = "up"
        
        if dx != 0 or dy != 0:
            self.is_moving = True
            
            # Normaliser le vecteur de mouvement pour les déplacements diagonaux
            if dx != 0 and dy != 0:
                magnitude = math.sqrt(dx**2 + dy**2)
                dx /= magnitude
                dy /= magnitude
            
            # Calculer la nouvelle position
            new_x = self.position[0] + dx * self.speed
            new_y = self.position[1] + dy * self.speed
            
            # Vérifier les collisions
            if not self.check_collisions([new_x, new_y], environment, npcs):
                self.position[0] = new_x
                self.position[1] = new_y
        else:
            self.is_moving = False
        
        # Mettre à jour les cooldowns
        self.update_cooldowns(dt)
    
    def update_cooldowns(self, dt):
        """Met à jour les cooldowns des compétences"""
        for skill_name in list(self.skill_cooldowns.keys()):
            self.skill_cooldowns[skill_name] -= dt
            if self.skill_cooldowns[skill_name] <= 0:
                del self.skill_cooldowns[skill_name]
    
    def check_collisions(self, position, environment, npcs):
        """Vérifie les collisions avec l'environnement et les PNJs"""
        # Collision avec l'environnement
        if environment.check_collision(position):
            return True
        
        # Collision avec les PNJs
        for npc in npcs:
            distance = self.calculate_distance(position, npc.position)
            if distance < 25:  # Rayon de collision
                return True
        
        return False
    
    def calculate_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def attack(self, target):
        """Attaque basique"""
        base_damage = self.calculate_damage()
        damage = target.take_damage(base_damage)
        
        # Chance de coup critique
        if self.check_critical_hit():
            damage *= self.stats["critical_multiplier"]
            damage = int(damage)
            return damage, True  # Retourne les dégâts et si c'est un critique
        
        return damage, False
    
    def calculate_damage(self):
        """Calcule les dégâts en fonction de la classe et des stats"""
        base_damage = 5
        if self.equipment["weapon"]:
            base_damage = self.equipment["weapon"].damage
        
        # Bonus selon la classe et les stats
        if self.current_class.name == "Guerrier":
            base_damage += self.stats["strength"] * 2
        elif self.current_class.name == "Archer":
            base_damage += self.stats["dexterity"] * 1.5
        elif self.current_class.name == "Mage":
            base_damage += self.stats["intelligence"] * 1.2
        elif self.current_class.name == "Voleur":
            base_damage += self.stats["dexterity"] * 1.3
        
        return int(base_damage)
    
    def check_critical_hit(self):
        """Vérifie si l'attaque est un coup critique"""
        return random.random() < self.stats["critical_chance"]
    
    def use_skill(self, skill_index, target):
        """Utilise une compétence"""
        if skill_index >= len(self.skills):
            return 0, False
        
        skill = self.skills[skill_index]
        
        # Vérifier le cooldown
        if skill.name in self.skill_cooldowns:
            return 0, False
        
        # Vérifier le coût en MP
        if self.mp < skill.mp_cost:
            return 0, False
        
        # Utiliser la compétence
        self.mp -= skill.mp_cost
        damage, is_critical = skill.use(self, target)
        
        # Appliquer le cooldown
        self.skill_cooldowns[skill.name] = skill.cooldown
        
        return damage, is_critical
    
    def take_damage(self, damage):
        """Reçoit des dégâts"""
        # Réduction des dégâts par la défense
        defense = self.stats["defense"]
        if self.equipment["armor"]:
            defense += self.equipment["armor"].defense
        
        actual_damage = max(1, damage - defense)
        self.hp -= actual_damage
        
        return actual_damage
    
    def heal(self, amount):
        """Soigne le joueur"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def restore_mp(self, amount):
        """Restaure du MP"""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def gain_xp(self, amount):
        """Gagne de l'expérience"""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Monte de niveau"""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        
        # Amélioration des stats selon la classe
        self.max_hp += self.current_class.hp_growth
        self.max_mp += self.current_class.mp_growth
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Amélioration des stats secondaires
        self.improve_stats()
        
        # Apprentissage de nouvelles compétences
        self.learn_new_skills()
        
        return True
    
    def improve_stats(self):
        """Améliore les stats secondaires au level up"""
        stat_improvements = self.current_class.get_stat_improvements()
        for stat, value in stat_improvements.items():
            self.stats[stat] += value
    
    def learn_new_skills(self):
        """Apprend de nouvelles compétences au level up"""
        new_skills = self.current_class.get_skills_for_level(self.level)
        for skill in new_skills:
            if skill not in self.skills:
                self.skills.append(skill)
    
    def change_class(self, new_class_name):
        """Change de classe"""
        if new_class_name in self.classes:
            self.current_class = self.classes[new_class_name]
            # Met à jour les compétences disponibles
            self.skills = self.current_class.get_skills_for_level(self.level)
            return True
        return False
    
    def add_item(self, item):
        """Ajoute un objet à l'inventaire"""
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Retire un objet de l'inventaire"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def equip(self, item):
        """Équipe un objet"""
        if item in self.inventory and item.equip_slot in self.equipment:
            # Déséquiper l'objet actuel
            if self.equipment[item.equip_slot]:
                self.unequip(item.equip_slot)
            
            # Équiper le nouvel objet
            self.equipment[item.equip_slot] = item
            self.inventory.remove(item)
            
            # Appliquer les bonus de l'équipement
            self.apply_equipment_bonuses()
            
            return True
        return False
    
    def unequip(self, slot):
        """Déséquipe un objet"""
        if self.equipment[slot]:
            self.inventory.append(self.equipment[slot])
            
            # Retirer les bonus de l'équipement
            self.remove_equipment_bonuses(self.equipment[slot])
            
            self.equipment[slot] = None
            return True
        return False
    
    def apply_equipment_bonuses(self):
        """Applique les bonus de tout l'équipement"""
        # Cette méthode serait appelée après chaque changement d'équipement
        pass
    
    def remove_equipment_bonuses(self, item):
        """Retire les bonus d'un équipement spécifique"""
        # Cette méthode serait appelée quand on déséquipe un objet
        pass

# Classes de base
class CharacterClass:
    def __init__(self, name, hp_growth, mp_growth):
        self.name = name
        self.hp_growth = hp_growth
        self.mp_growth = mp_growth
        self.skill_tree = {}
    
    def get_skills_for_level(self, level):
        """Retourne les compétences disponibles pour un niveau donné"""
        skills = []
        for lvl, skill_list in self.skill_tree.items():
            if lvl <= level:
                skills.extend(skill_list)
        return skills
    
    def get_stat_improvements(self):
        """Retourne les améliorations de stats pour un level up"""
        return {}  # À implémenter dans les sous-classes

class Warrior(CharacterClass):
    def __init__(self):
        super().__init__("Guerrier", 20, 5)
        self.skill_tree = {
            1: [Skill("Coup d'épée", 0, 10, 1)],
            3: [Skill("Coup puissant", 10, 25, 3)],
            5: [Skill("Cri de guerre", 15, 0, 4)]
        }
    
    def get_stat_improvements(self):
        return {"strength": 2, "defense": 1}

class Archer(CharacterClass):
    def __init__(self):
        super().__init__("Archer", 10, 10)
        self.skill_tree = {
            1: [Skill("Tir rapide", 5, 8, 1)],
            3: [Skill("Tir multiple", 15, 6, 3)],
            5: [Skill("Flèche empoisonnée", 20, 10, 4)]
        }
    
    def get_stat_improvements(self):
        return {"dexterity": 3, "critical_chance": 0.02}

class Mage(CharacterClass):
    def __init__(self):
        super().__init__("Mage", 5, 20)
        self.skill_tree = {
            1: [Skill("Boule de feu", 10, 15, 1)],
            3: [Skill("Éclair", 15, 20, 3)],
            5: [Skill("Barrière magique", 20, 0, 4)]
        }
    
    def get_stat_improvements(self):
        return {"intelligence": 3, "mp": 5}

class Thief(CharacterClass):
    def __init__(self):
        super().__init__("Voleur", 8, 12)
        self.skill_tree = {
            1: [Skill("Coup furtif", 5, 12, 1)],
            3: [Skill("Attaque surprise", 10, 18, 3)],
            5: [Skill("Vol à la tire", 0, 5, 4)]
        }
    
    def get_stat_improvements(self):
        return {"dexterity": 2, "critical_chance": 0.03, "critical_multiplier": 0.1}

class Skill:
    def __init__(self, name, mp_cost, base_damage, cooldown):
        self.name = name
        self.mp_cost = mp_cost
        self.base_damage = base_damage
        self.cooldown = cooldown  # en secondes
    
    def use(self, user, target):
        damage = self.base_damage + (user.level * 2)
        actual_damage = target.take_damage(damage)
        
        # Effets spéciaux selon le nom de la compétence
        if "empoisonnée" in self.name.lower():
            # Appliquer un poison
            pass
        elif "cri" in self.name.lower():
            # Appliquer un buff
            pass
        
        return actual_damage, False
