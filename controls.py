# controls.py - Système de contrôle clavier ET tactile
import pygame

class ControlSystem:
    def __init__(self):
        # États de contrôle
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.interact = False
        self.attack = False
        self.inventory = False
        
        # Contrôles tactiles
        self.touch_controls = []
        self.create_touch_controls()
        
        # Configuration des touches
        self.key_bindings = {
            "move_up": [pygame.K_UP, pygame.K_w],
            "move_down": [pygame.K_DOWN, pygame.K_s],
            "move_left": [pygame.K_LEFT, pygame.K_a],
            "move_right": [pygame.K_RIGHT, pygame.K_d],
            "interact": [pygame.K_e],
            "attack": [pygame.K_SPACE],
            "inventory": [pygame.K_i]
        }
    
    def create_touch_controls(self):
        """Crée les boutons de contrôle tactiles"""
        # Zone de déplacement (joystick virtuel)
        self.touch_controls.append({
            "type": "joystick",
            "rect": pygame.Rect(50, 450, 150, 150),
            "active": False,
            "direction": (0, 0)
        })
        
        # Boutons d'action
        self.touch_controls.append({
            "type": "button",
            "action": "interact",
            "rect": pygame.Rect(700, 450, 80, 80),
            "icon": "E"
        })
        
        self.touch_controls.append({
            "type": "button",
            "action": "attack",
            "rect": pygame.Rect(600, 450, 80, 80),
            "icon": "⚔️"
        })
        
        self.touch_controls.append({
            "type": "button",
            "action": "inventory",
            "rect": pygame.Rect(500, 450, 80, 80),
            "icon": "🎒"
        })
    
    def handle_event(self, event):
        """Gère les événements d'entrée"""
        # Réinitialiser les états
        self.interact = False
        self.attack = False
        self.inventory = False
        
        # Contrôles clavier
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_bindings["move_up"]:
                self.move_up = True
            elif event.key in self.key_bindings["move_down"]:
                self.move_down = True
            elif event.key in self.key_bindings["move_left"]:
                self.move_left = True
            elif event.key in self.key_bindings["move_right"]:
                self.move_right = True
            elif event.key in self.key_bindings["interact"]:
                self.interact = True
            elif event.key in self.key_bindings["attack"]:
                self.attack = True
            elif event.key in self.key_bindings["inventory"]:
                self.inventory = True
        
        elif event.type == pygame.KEYUP:
            if event.key in self.key_bindings["move_up"]:
                self.move_up = False
            elif event.key in self.key_bindings["move_down"]:
                self.move_down = False
            elif event.key in self.key_bindings["move_left"]:
                self.move_left = False
            elif event.key in self.key_bindings["move_right"]:
                self.move_right = False
        
        # Contrôles tactiles
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_touch_event(event.pos, True)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_touch_event(event.pos, False)
        
        elif event.type == pygame.MOUSEMOTION:
            self.handle_touch_drag(event.pos)
    
    def handle_touch_event(self, pos, is_pressed):
        """Gère les événements tactiles"""
        for control in self.touch_controls:
            if control["rect"].collidepoint(pos):
                if control["type"] == "joystick" and is_pressed:
                    control["active"] = True
                    self.update_joystick_direction(pos, control)
                elif control["type"] == "button" and is_pressed:
                    setattr(self, control["action"], True)
                elif control["type"] == "joystick" and not is_pressed:
                    control["active"] = False
                    control["direction"] = (0, 0)
                    self.move_up = self.move_down = self.move_left = self.move_right = False
    
    def handle_touch_drag(self, pos):
        """Gère le glissement sur le joystick virtuel"""
        for control in self.touch_controls:
            if control["type"] == "joystick" and control["active"]:
                self.update_joystick_direction(pos, control)
    
    def update_joystick_direction(self, pos, joystick):
        """Met à jour la direction du joystick virtuel"""
        center_x = joystick["rect"].centerx
        center_y = joystick["rect"].centery
        
        dx = pos[0] - center_x
        dy = pos[1] - center_y
        
        # Normaliser la direction
        distance = max(1, (dx**2 + dy**2)**0.5)
        norm_dx = dx / distance
        norm_dy = dy / distance
        
        # Seuils pour activer les directions
        self.move_up = norm_dy < -0.3
        self.move_down = norm_dy > 0.3
        self.move_left = norm_dx < -0.3
        self.move_right = norm_dx > 0.3
        
        joystick["direction"] = (norm_dx, norm_dy)
    
    def get_movement_vector(self):
        """Retourne le vecteur de mouvement normalisé"""
        dx, dy = 0, 0
        
        if self.move_up: dy -= 1
        if self.move_down: dy += 1
        if self.move_left: dx -= 1
        if self.move_right: dx += 1
        
        # Normaliser le vecteur pour les déplacements diagonaux
        if dx != 0 and dy != 0:
            magnitude = (dx**2 + dy**2)**0.5
            dx /= magnitude
            dy /= magnitude
        
        return dx, dy
    
    def draw_touch_controls(self, screen):
        """Dessine les contrôles tactiles à l'écran"""
        for control in self.touch_controls:
            if control["type"] == "joystick":
                self.draw_joystick(screen, control)
            elif control["type"] == "button":
                self.draw_button(screen, control)
    
    def draw_joystick(self, screen, joystick):
        """Dessine le joystick virtuel"""
        # Cercle de fond (semi-transparent)
        s = pygame.Surface((joystick["rect"].width, joystick["rect"].height), pygame.SRCALPHA)
        pygame.draw.circle(s, (100, 100, 100, 150), 
                          (joystick["rect"].width//2, joystick["rect"].height//2),
                          joystick["rect"].width//2)
        screen.blit(s, joystick["rect"])
        
        # Stick du joystick
        if joystick["active"]:
            stick_pos = (
                joystick["rect"].centerx + joystick["direction"][0] * 30,
                joystick["rect"].centery + joystick["direction"][1] * 30
            )
            pygame.draw.circle(screen, (200, 200, 200, 200), stick_pos, 20)
    
    def draw_button(self, screen, button):
        """Dessine un bouton tactile"""
        # Fond du bouton (semi-transparent)
        s = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
        pygame.draw.circle(s, (100, 100, 100, 150), 
                          (button["rect"].width//2, button["rect"].height//2),
                          button["rect"].width//2)
        screen.blit(s, button["rect"])
        
        # Icône du bouton
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(button["icon"], True, (255, 255, 255))
        screen.blit(text, button["rect"].center)
