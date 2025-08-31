# mobile_adapter.py - Adaptations pour appareils tactiles
import pygame
import os

class MobileAdapter:
    def __init__(self):
        self.is_mobile = self.detect_mobile()
        self.scale_factor = 1.0
        
        if self.is_mobile:
            self.adapt_for_mobile()
    
    def detect_mobile(self):
        """Détecte si l'application tourne sur mobile"""
        try:
            # Méthodes de détection pour différentes plateformes
            if os.environ.get('ANDROID_ARGUMENT') or os.environ.get('KIVY_BUILD'):
                return True
            # Ajouter d'autres méthodes de détection au besoin
        except:
            pass
        return False
    
    def adapt_for_mobile(self):
        """Adapte le jeu pour les appareils mobiles"""
        # Ajuster la résolution
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        
        # Calculer le facteur d'échelle
        self.scale_factor = min(screen_width / 800, screen_height / 600)
        
        # Configurer pour le tactile
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        
        # Ajuster la taille de police
        pygame.font.init()
        
    def scale_value(self, value):
        """Met à l'échelle une valeur selon l'écran"""
        return int(value * self.scale_factor)
    
    def get_touch_position(self, pos):
        """Convertit la position du touch en coordonnées jeu"""
        if self.is_mobile:
            return (pos[0] / self.scale_factor, pos[1] / self.scale_factor)
        return pos

# Utilisation dans main.py
class Game:
    def __init__(self):
        # ...
        self.mobile_adapter = MobileAdapter()
        # Ajuster la configuration en fonction de la plateforme
        if self.mobile_adapter.is_mobile:
            self.config.set("controls", "keyboard_enabled", False)
            self.config.set("controls", "touch_enabled", True)
