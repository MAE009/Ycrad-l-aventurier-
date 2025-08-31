# environment.py - Gestion de l'environnement et des zones
class Environment:
    def __init__(self):
        self.zones = {
            "village": {
                "monsters": [],
                "npcs": ["marchand", "forgeron", "aubergiste"],
                "background": "village_bg",
                "music": "village_theme"
            },
            "foret": {
                "monsters": [("slime", 1), ("rat", 1), ("slime", 2)],
                "npcs": ["chasseur"],
                "background": "forest_bg",
                "music": "forest_theme"
            },
            "marais": {
                "monsters": [("slime", 3), ("rat", 4), ("slime", 5)],
                "npcs": ["ermite"],
                "background": "marsh_bg",
                "music": "marsh_theme",
                "boss": "Korvash"
            }
        }
        
        self.zone_boundaries = {
            "village": {"x": (0, 400), "y": (0, 300)},
            "foret": {"x": (400, 800), "y": (0, 300)},
            "marais": {"x": (0, 400), "y": (300, 600)}
        }
        
        # Générer les monstres initiaux
        self.generate_monsters()
    
    def generate_monsters(self):
        from monsters import Slime, Rat
        monster_classes = {"slime": Slime, "rat": Rat}
        
        for zone_name, zone_data in self.zones.items():
            zone_data["monster_instances"] = []
            for monster_type, level in zone_data["monsters"]:
                # Position aléatoire dans la zone
                x_min, x_max = self.zone_boundaries[zone_name]["x"]
                y_min, y_max = self.zone_boundaries[zone_name]["y"]
                x = random.randint(x_min, x_max)
                y = random.randint(y_min, y_max)
                
                monster = monster_classes[monster_type](level, [x, y])
                zone_data["monster_instances"].append(monster)
    
    def get_monsters_in_current_zone(self, zone_name):
        return self.zones[zone_name]["monster_instances"]
    
    def check_collision(self, position):
        # Vérifier les collisions avec les obstacles
        # À adapter selon votre carte
        return False
    
    def get_zone_at_position(self, position):
        x, y = position
        for zone_name, boundaries in self.zone_boundaries.items():
            x_min, x_max = boundaries["x"]
            y_min, y_max = boundaries["y"]
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return zone_name
        return "village"  # Zone par défaut
