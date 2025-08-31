# skills.py - Système de compétences avancées
class AdvancedSkill(Skill):
    def __init__(self, name, mp_cost, base_damage, skill_type, cooldown, effects=None):
        super().__init__(name, mp_cost, base_damage)
        self.skill_type = skill_type  # attack, buff, debuff, heal
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.effects = effects or {}
    
    def use(self, user, target):
        if self.current_cooldown > 0:
            return 0  # Compétence en recharge
        
        result = super().use(user, target)
        
        # Appliquer les effets supplémentaires
        if "buff" in self.effects:
            for attr, value in self.effects["buff"].items():
                if hasattr(user, attr):
                    setattr(user, attr, getattr(user, attr) + value)
        
        if "debuff" in self.effects:
            for attr, value in self.effects["debuff"].items():
                if hasattr(target, attr):
                    setattr(target, attr, max(1, getattr(target, attr) - value))
        
        self.current_cooldown = self.cooldown
        return result
    
    def update_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

# Compétences spéciales pour chaque classe
class WarriorSkills:
    @staticmethod
    def power_strike():
        return AdvancedSkill(
            "Coup Puissant", 15, 30, "attack", 3,
            effects={"debuff": {"damage": 5}}  # Réduit les dégâts de l'ennemi
        )
    
    @staticmethod
    def war_cry():
        return AdvancedSkill(
            "Cri de Guerre", 20, 0, "buff", 4,
            effects={"buff": {"damage": 10, "max_hp": 20}}  Augmente les dégâts et PV max
        )

class MageSkills:
    @staticmethod
    def fireball():
        return AdvancedSkill(
            "Boule de Feu", 25, 40, "attack", 3,
            effects={"debuff": {"hp": 5}}  # Dégâts sur le temps
        )
    
    @staticmethod
    def magic_shield():
        return AdvancedSkill(
            "Bouclier Magique", 30, 0, "buff", 5,
            effects={"buff": {"defense": 15}}  # Augmente la défense
        )

# Ajouter ces compétences aux classes
Warrior.skill_levels = {
    3: WarriorSkills.power_strike(),
    5: WarriorSkills.war_cry(),
    8: AdvancedSkill("Fracasseur", 40, 60, "attack", 5)
}

Mage.skill_levels = {
    3: MageSkills.fireball(),
    5: MageSkills.magic_shield(),
    8: AdvancedSkill("Tempête de Glace", 50, 70, "attack", 6)
}
