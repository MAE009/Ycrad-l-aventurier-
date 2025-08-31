# dialogue.py - Système de dialogues avec les PNJ
class DialogueSystem:
    def __init__(self):
        self.dialogues = self.load_dialogues()
        self.current_dialogue = None
        self.current_line = 0
        self.active = False
    
    def load_dialogues(self):
        return {
            "marchand": {
                "greeting": [
                    "Bienvenue dans ma boutique, aventurier !",
                    "J'ai des armes et armures de qualité.",
                    "Que puis-je pour vous aujourd'hui ?"
                ],
                "quest": [
                    "J'ai entendu dire que des slimes attaquent les fermes.",
                    "Si vous en éliminez quelques-uns, je vous récompenserai."
                ],
                "trade": [
                    "Voici ce que j'ai à vendre...",
                    "*Ouvre son inventaire*"
                ]
            },
            "forgeron": {
                "greeting": [
                    "Hé ho ! Du fer et du feu, c'est ce qui fait un bon forgeron !",
                    "Besoin d'aiguiser votre lame ?"
                ],
                "quest": [
                    "J'ai besoin de minerai rare des montagnes.",
                    "Apportez-moi 5 morceaux et je vous forgerai une arme spéciale."
                ]
            }
        }
    
    def start_dialogue(self, npc_name, dialogue_type="greeting"):
        if npc_name in self.dialogues and dialogue_type in self.dialogues[npc_name]:
            self.current_dialogue = self.dialogues[npc_name][dialogue_type]
            self.current_line = 0
            self.active = True
            return self.get_current_line()
        return None
    
    def get_current_line(self):
        if self.current_dialogue and self.current_line < len(self.current_dialogue):
            return self.current_dialogue[self.current_line]
        return None
    
    def next_line(self):
        if self.current_dialogue and self.current_line < len(self.current_dialogue) - 1:
            self.current_line += 1
            return self.get_current_line()
        else:
            self.end_dialogue()
            return None
    
    def end_dialogue(self):
        self.active = False
        self.current_dialogue = None
        self.current_line = 0

class NPC:
    def __init__(self, name, npc_type, position, dialogues):
        self.name = name
        self.type = npc_type  # merchant, quest_giver, etc.
        self.position = position
        self.dialogues = dialogues
        self.interaction_range = 50
    
    def can_interact(self, player_position):
        distance = ((self.position[0] - player_position[0])**2 + 
                   (self.position[1] - player_position[1])**2)**0.5
        return distance <= self.interaction_range
    
    def interact(self, dialogue_system):
        return dialogue_system.start_dialogue(self.name, "greeting")
