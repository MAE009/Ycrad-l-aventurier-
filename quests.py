# quests.py - Système de quêtes
class Quest:
    def __init__(self, title, description, objectives, rewards):
        self.title = title
        self.description = description
        self.objectives = objectives  # Liste de tuples (type, cible, quantité)
        self.rewards = rewards  # XP, or, objets
        self.completed = False
        self.progress = {obj[1]: 0 for obj in objectives}
    
    def update_progress(self, objective_type, target, amount=1):
        if not self.completed and (objective_type, target) in self.objectives:
            self.progress[target] += amount
            # Vérifier si tous les objectifs sont complétés
            if all(self.progress[obj[1]] >= obj[2] for obj in self.objectives):
                self.completed = True
                return True
        return False

class QuestManager:
    def __init__(self):
        self.quests = {
            "active": [],
            "completed": []
        }
        self.available_quests = self.generate_starting_quests()
        self.show_quests = False
    
    def generate_starting_quests(self):
        return [
            Quest(
                "Chasse aux slimes",
                "Les slimes attaquent les récoltes. Tuez 5 slimes.",
                [("kill", "slime", 5)],
                {"xp": 100, "gold": 50, "items": ["Petite épée"]}
            ),
            Quest(
                "Rat problem",
                "Les rats volent notre nourriture. Éliminez 3 rats.",
                [("kill", "rat", 3)],
                {"xp": 50, "gold": 25, "items": ["Potion de santé"]}
            )
        ]
    
    def accept_quest(self, quest_index):
        if 0 <= quest_index < len(self.available_quests):
            quest = self.available_quests.pop(quest_index)
            self.quests["active"].append(quest)
    
    def complete_quest(self, quest):
        if quest in self.quests["active"] and quest.completed:
            self.quests["active"].remove(quest)
            self.quests["completed"].append(quest)
            return quest.rewards
        return None
    
    def check_triggers(self, player_position):
        # Vérifier les déclencheurs de quêtes (NPCs, zones, etc.)
        pass
    
    def on_monster_killed(self, monster_type):
        for quest in self.quests["active"]:
            quest.update_progress("kill", monster_type)
