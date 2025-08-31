# save_system.py - Système de sauvegarde et chargement
import json
import os

class SaveSystem:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, player, environment, quest_manager, slot=0):
        save_data = {
            "player": {
                "name": player.name,
                "level": player.level,
                "xp": player.xp,
                "xp_to_next_level": player.xp_to_next_level,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "mp": player.mp,
                "max_mp": player.max_mp,
                "current_class": player.current_class.name,
                "position": player.position,
                "gold": player.gold,
                "inventory": [item.__dict__ for item in player.inventory],
                "equipment": {
                    slot: item.__dict__ if item else None 
                    for slot, item in player.equipment.items()
                }
            },
            "quests": {
                "active": [quest.__dict__ for quest in quest_manager.quests["active"]],
                "completed": [quest.__dict__ for quest in quest_manager.quests["completed"]],
                "available": [quest.__dict__ for quest in quest_manager.available_quests]
            },
            "environment": {
                "current_zone": environment.current_zone,
                "monsters": self.serialize_monsters(environment)
            },
            "timestamp": pygame.time.get_ticks()
        }
        
        save_path = os.path.join(self.save_dir, f"save_{slot}.json")
        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return True
    
    def load_game(self, slot=0):
        save_path = os.path.join(self.save_dir, f"save_{slot}.json")
        if not os.path.exists(save_path):
            return None
        
        with open(save_path, 'r') as f:
            save_data = json.load(f)
        
        return save_data
    
    def serialize_monsters(self, environment):
        serialized = {}
        for zone_name, zone_data in environment.zones.items():
            serialized[zone_name] = []
            for monster in zone_data.get("monster_instances", []):
                serialized[zone_name].append({
                    "type": monster.type,
                    "level": monster.level,
                    "position": monster.position,
                    "hp": monster.hp
                })
        return serialized
    
    def get_save_slots(self):
        slots = []
        for i in range(3):  # 3 slots de sauvegarde
            if os.path.exists(os.path.join(self.save_dir, f"save_{i}.json")):
                with open(os.path.join(self.save_dir, f"save_{i}.json"), 'r') as f:
                    data = json.load(f)
                    slots.append({
                        "slot": i,
                        "exists": True,
                        "player_name": data["player"]["name"],
                        "player_level": data["player"]["level"],
                        "timestamp": data["timestamp"]
                    })
            else:
                slots.append({"slot": i, "exists": False})
        return slots
