# config.py - Système de configuration
import json

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = {
            "graphics": {
                "resolution": [800, 600],
                "fullscreen": False,
                "vsync": True,
                "framerate": 60
            },
            "audio": {
                "music_volume": 0.5,
                "sound_volume": 0.7,
                "mute": False
            },
            "gameplay": {
                "difficulty": "normal",
                "autosave": True,
                "autosave_interval": 300  # 5 minutes
            },
            "controls": {
                "move_up": pygame.K_UP,
                "move_down": pygame.K_DOWN,
                "move_left": pygame.K_LEFT,
                "move_right": pygame.K_RIGHT,
                "interact": pygame.K_e,
                "inventory": pygame.K_i,
                "skills": pygame.K_s
            }
        }
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            # S'assurer que toutes les clés existent
            for category, settings in self.default_config.items():
                if category not in self.config:
                    self.config[category] = settings
                else:
                    for key, value in settings.items():
                        if key not in self.config[category]:
                            self.config[category][key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = self.default_config
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, category, key):
        return self.config.get(category, {}).get(key, None)
    
    def set(self, category, key, value):
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value
        self.save_config()
    
    def apply_graphics_settings(self, screen):
        if self.get("graphics", "fullscreen"):
            screen = pygame.display.set_mode(
                self.get("graphics", "resolution"), 
                pygame.FULLSCREEN
            )
        else:
            screen = pygame.display.set_mode(
                self.get("graphics", "resolution")
            )
        return screen
