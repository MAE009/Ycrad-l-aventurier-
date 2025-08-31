# main.py - Point d'entrée principal du jeu
import pygame
import sys
from player import Player
from environment import Environment
from quests import QuestManager
from inventory import Inventory
from ui import UI
from monsters import Monster, Boss

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ycrad l'Aventurier")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # menu, playing, combat, dialogue
        
        # Chargement des assets
        self.load_assets()
        
        # Initialisation des systèmes
        self.player = Player("Ycrad", "warrior")
        self.environment = Environment()
        self.quest_manager = QuestManager()
        self.inventory = Inventory()
        self.ui = UI(self.player, self.inventory)
        
        # Zone actuelle
        self.current_zone = "village"
        
    def load_assets(self):
        # Charger les sprites et images (à compléter avec vos assets)
        self.assets = {
            "player": pygame.Surface((16, 16)),
            "monsters": {
                "slime": pygame.Surface((16, 16)),
                "rat": pygame.Surface((16, 16)),
                # Ajouter d'autres monstres...
            },
            "environments": {
                "village": pygame.Surface((800, 600)),
                "forest": pygame.Surface((800, 600)),
                # Ajouter d'autres environnements...
            }
        }
        # Remplir avec des couleurs temporaires
        self.assets["player"].fill((0, 0, 255))  # Bleu pour le joueur
        self.assets["monsters"]["slime"].fill((0, 255, 0))  # Vert pour le slime
        self.assets["monsters"]["rat"].fill((139, 69, 19))  # Marron pour le rat
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        self.game_state = "playing"
                elif self.game_state == "playing":
                    if event.key == pygame.K_e:
                        self.inventory.toggle()
                    elif event.key == pygame.K_q:
                        self.quest_manager.show_quests = not self.quest_manager.show_quests
                    elif event.key == pygame.K_SPACE:
                        self.attempt_attack()
            
            # Gestion des clics pour l'UI
            self.ui.handle_event(event)
    
    def attempt_attack(self):
        # Vérifier s'il y a un monstre à proximité pour combattre
        for monster in self.environment.get_monsters_in_current_zone(self.current_zone):
            if self.calculate_distance(self.player.position, monster.position) < 50:
                self.start_combat(monster)
                break
    
    def start_combat(self, monster):
        self.game_state = "combat"
        self.combat_monster = monster
        self.combat_turn = "player"  # player ou monster
    
    def resolve_combat_turn(self):
        if self.combat_turn == "player":
            damage = self.player.attack(self.combat_monster)
            self.ui.combat_messages.append(f"Ycrad inflige {damage} dégâts!")
            
            if self.combat_monster.hp <= 0:
                self.ui.combat_messages.append(f"Vous avez vaincu le {self.combat_monster.name}!")
                self.player.gain_xp(self.combat_monster.xp_reward)
                self.game_state = "playing"
                return
                
            self.combat_turn = "monster"
        else:
            damage = self.combat_monster.attack(self.player)
            self.ui.combat_messages.append(f"Le {self.combat_monster.name} inflige {damage} dégâts!")
            
            if self.player.hp <= 0:
                self.ui.combat_messages.append("Vous avez été vaincu!")
                self.game_state = "game_over"
                return
                
            self.combat_turn = "player"
    
    def calculate_distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def update(self):
        if self.game_state == "playing":
            # Mettre à jour la position du joueur en fonction des inputs
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]: dx = -1
            if keys[pygame.K_RIGHT]: dx = 1
            if keys[pygame.K_UP]: dy = -1
            if keys[pygame.K_DOWN]: dy = 1
            
            self.player.move(dx, dy)
            
            # Vérifier les collisions avec l'environnement
            if self.environment.check_collision(self.player.position):
                self.player.move(-dx, -dy)  # Annuler le mouvement en cas de collision
            
            # Vérifier les déclencheurs de quêtes
            self.quest_manager.check_triggers(self.player.position)
            
            # Vérifier si le joueur change de zone
            new_zone = self.environment.get_zone_at_position(self.player.position)
            if new_zone != self.current_zone:
                self.current_zone = new_zone
                self.ui.messages.append(f"Vous entrez dans {new_zone}")
        
        elif self.game_state == "combat":
            # Gérer le tour par tour du combat
            if pygame.time.get_ticks() % 2000 < 20:  # Toutes les 2 secondes
                self.resolve_combat_turn()
    
    def render(self):
        # Dessiner l'environnement
        self.screen.blit(self.assets["environments"][self.current_zone], (0, 0))
        
        # Dessiner le joueur
        self.screen.blit(self.assets["player"], self.player.position)
        
        # Dessiner les monstres dans la zone actuelle
        for monster in self.environment.get_monsters_in_current_zone(self.current_zone):
            self.screen.blit(self.assets["monsters"][monster.type], monster.position)
        
        # Dessiner l'UI
        self.ui.draw(self.screen, self.game_state)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
