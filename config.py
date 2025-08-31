# config.py - Système de configuration complet
import json
import pygame
import os

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.default_config = self.get_default_config()
        self.config = {}
        self.load_config()
    
    def get_default_config(self):
        """Retourne la configuration par défaut"""
        return {
            "graphics": {
                "resolution": [800, 600],
                "fullscreen": False,
                "vsync": True,
                "framerate": 60,
                "render_scale": 1.0,
                "particles_quality": "medium",
                "shadow_quality": "low"
            },
            "audio": {
                "master_volume": 1.0,
                "music_volume": 0.7,
                "sound_volume": 0.8,
                "mute": False,
                "enable_ambience": True
            },
            "gameplay": {
                "difficulty": "normal",
                "autosave": True,
                "autosave_interval": 300,
                "tooltips": True,
                "minimap": True,
                "quest_markers": True,
                "auto_pickup": False
            },
            "controls": {
                "keyboard_enabled": True,
                "touch_enabled": True,
                "keyboard": {
                    "move_up": [pygame.K_UP, pygame.K_w],
                    "move_down": [pygame.K_DOWN, pygame.K_s],
                    "move_left": [pygame.K_LEFT, pygame.K_a],
                    "move_right": [pygame.K_RIGHT, pygame.K_d],
                    "interact": [pygame.K_e],
                    "attack": [pygame.K_SPACE],
                    "inventory": [pygame.K_i],
                    "skills": [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4],
                    "pause": [pygame.K_ESCAPE]
                },
                "touch": {
                    "opacity": 150,
                    "size": 80,
                    "position": "bottom",
                    "vibration": True,
                    "deadzone": 0.2
                },
                "gamepad": {
                    "enabled": False,
                    "deadzone": 0.15,
                    "vibration": True
                }
            },
            "interface": {
                "language": "french",
                "font_size": 16,
                "font_style": "default",
                "ui_scale": 1.0,
                "show_fps": False,
                "show_coordinates": False,
                "health_bar_style": "modern",
                "chat_opacity": 200
            },
            "accessibility": {
                "high_contrast": False,
                "colorblind_mode": "none",
                "text_to_speech": False,
                "font_dyslexia": False,
                "button_size": "normal",
                "subtitles": True,
                "subtitle_size": "medium"
            }
        }
    
    def load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                # S'assurer que toutes les sections existent
                for category, settings in self.default_config.items():
                    if category not in self.config:
                        self.config[category] = settings
                    else:
                        for key, value in settings.items():
                            if key not in self.config[category]:
                                self.config[category][key] = value
            else:
                self.config = self.default_config
                self.save_config()
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur de chargement de la config: {e}")
            self.config = self.default_config
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                
        except IOError as e:
            print(f"Erreur de sauvegarde de la config: {e}")
    
    def get(self, category, key, default=None):
        """Récupère une valeur de configuration"""
        try:
            return self.config.get(category, {}).get(key, self.default_config[category][key])
        except KeyError:
            return default
    
    def set(self, category, key, value):
        """Définit une valeur de configuration"""
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value
        self.save_config()
    
    def apply_graphics_settings(self, screen):
        """Applique les paramètres graphiques"""
        resolution = self.get("graphics", "resolution")
        fullscreen = self.get("graphics", "fullscreen")
        vsync = self.get("graphics", "vsync")
        
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        if vsync:
            flags |= pygame.HWSURFACE | pygame.DOUBLEBUF
        
        try:
            new_screen = pygame.display.set_mode(resolution, flags)
            pygame.display.set_caption("Ycrad l'Aventurier")
            return new_screen
        except pygame.error as e:
            print(f"Erreur graphique: {e}")
            return screen
    
    def apply_audio_settings(self, audio_manager):
        """Applique les paramètres audio"""
        if audio_manager:
            audio_manager.set_master_volume(self.get("audio", "master_volume"))
            audio_manager.set_music_volume(self.get("audio", "music_volume"))
            audio_manager.set_sound_volume(self.get("audio", "sound_volume"))
            audio_manager.set_mute(self.get("audio", "mute"))
    
    def get_key_bindings(self):
        """Retourne les bindings de touches"""
        return self.get("controls", "keyboard")
    
    def is_touch_enabled(self):
        """Vérifie si les contrôles tactiles sont activés"""
        return self.get("controls", "touch_enabled")
    
    def get_touch_settings(self):
        """Retourne les paramètres tactiles"""
        return self.get("controls", "touch")
    
    def reset_to_defaults(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        self.config = self.default_config
        self.save_config()
    
    def get_difficulty_multiplier(self):
        """Retourne le multiplicateur de difficulté"""
        difficulty = self.get("gameplay", "difficulty")
        multipliers = {
            "easy": 0.7,
            "normal": 1.0,
            "hard": 1.3,
            "expert": 1.7
        }
        return multipliers.get(difficulty, 1.0)
