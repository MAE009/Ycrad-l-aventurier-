# main.py - Point d'entrée principal du jeu avec tous les systèmes
import pygame
import sys
import random
from player import Player
from environment import Environment
from quests import QuestManager
from inventory import Inventory
from ui import UI
from monsters import Slime, Rat, Korvash
from dialogue import DialogueSystem, NPC
from audio import AudioManager
from save_system import SaveSystem
from animation import AnimationManager
from menu import MainMenu
from config import Config

class Game:
    def __init__(self):
        pygame.init()
        
        # Configuration
        self.config = Config()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ycrad l'Aventurier")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # menu, playing, combat, dialogue, inventory, game_over
        
        # Initialisation des systèmes
        self.audio_manager = AudioManager()
        self.save_system = SaveSystem()
        self.animation_manager = AnimationManager()
        self.dialogue_system = DialogueSystem()
        
        # Chargement des assets
        self.load_assets()
        
        # Menu principal
        self.main_menu = MainMenu(self)
        
        # Initialisation différée des systèmes de jeu
        self.player = None
        self.environment = None
        self.quest_manager = None
        self.inventory = None
        self.ui = None
        self.npcs = []
        
        # États de jeu
        self.current_zone = "village"
        self.combat_monster = None
        self.combat_turn = "player"
        self.combat_timer = 0
        self.interacting_npc = None
        
        # Appliquer la configuration
        self.apply_config()
        
    def load_assets(self):
        # Charger les sprites et images (à compléter avec vos assets)
        self.assets = {
            "player": pygame.Surface((16, 16)),
            "monsters": {
                "slime": pygame.Surface((16, 16)),
                "rat": pygame.Surface((16, 16)),
            },
            "environments": {
                "village": pygame.Surface((800, 600)),
                "forest": pygame.Surface((800, 600)),
                "marsh": pygame.Surface((800, 600)),
            },
            "npcs": {
                "merchant": pygame.Surface((16, 16)),
                "blacksmith": pygame.Surface((16, 16)),
            }
        }
        
        # Remplir avec des couleurs temporaires
        self.assets["player"].fill((0, 0, 255))  # Bleu pour le joueur
        self.assets["monsters"]["slime"].fill((0, 255, 0))  # Vert pour le slime
        self.assets["monsters"]["rat"].fill((139, 69, 19))  # Marron pour le rat
        self.assets["environments"]["village"].fill((200, 200, 100))  # Jaune sable
        self.assets["environments"]["forest"].fill((0, 100, 0))  # Vert forêt
        self.assets["environments"]["marsh"].fill((70, 50, 30))  # Marron marais
        self.assets["npcs"]["merchant"].fill((255, 0, 0))  # Rouge marchand
        self.assets["npcs"]["blacksmith"].fill((100, 100, 100))  # Gris forgeron
    
    def apply_config(self):
        # Appliquer les paramètres audio
        self.audio_manager.set_music_volume(self.config.get("audio", "music_volume"))
        self.audio_manager.set_sound_volume(self.config.get("audio", "sound_volume"))
        
        # Appliquer les paramètres graphiques
        if self.config.get("graphics", "fullscreen"):
            self.screen = pygame.display.set_mode(
                self.config.get("graphics", "resolution"), 
                pygame.FULLSCREEN
            )
    
    def initialize_game(self):
        """Initialise tous les systèmes pour une nouvelle partie"""
        self.player = Player("Ycrad", "warrior")
        self.environment = Environment()
        self.quest_manager = QuestManager()
        self.inventory = Inventory()
        self.ui = UI(self.player, self.inventory, self.quest_manager)
        
        # Créer les PNJs
        self.npcs = [
            NPC("marchand", "merchant", [200, 200], self.dialogue_system),
            NPC("forgeron", "blacksmith", [300, 250], self.dialogue_system)
        ]
        
        # Générer les monstres initiaux
        self.environment.generate_monsters()
        
        # Jouer la musique du village
        self.audio_manager.play_music("village")
        
        self.game_state = "playing"
    
    def load_game(self, slot=0):
        """Charge une partie sauvegardée"""
        save_data = self.save_system.load_game(slot)
        if save_data:
            # Reconstruire l'état du jeu à partir des données sauvegardées
            self.player = Player(save_data["player"]["name"], save_data["player"]["current_class"])
            self.player.__dict__.update(save_data["player"])
            
            self.environment = Environment()
            self.environment.current_zone = save_data["environment"]["current_zone"]
            
            self.quest_manager = QuestManager()
            # Reconstruire les quêtes...
            
            self.inventory = Inventory()
            # Reconstruire l'inventaire...
            
            self.ui = UI(self.player, self.inventory, self.quest_manager)
            
            self.game_state = "playing"
            self.audio_manager.play_music(self.environment.current_zone)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Gestion des événements selon l'état du jeu
            if self.game_state == "menu":
                self.main_menu.handle_input(event)
            
            elif self.game_state == "playing":
                self.handle_playing_events(event)
            
            elif self.game_state == "combat":
                self.handle_combat_events(event)
            
            elif self.game_state == "dialogue":
                self.handle_dialogue_events(event)
            
            # Gestion des clics pour l'UI
            if self.ui:
                self.ui.handle_event(event, self)
    
    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # Tentative d'interaction avec un PNJ
                for npc in self.npcs:
                    if npc.can_interact(self.player.position):
                        self.interacting_npc = npc
                        self.game_state = "dialogue"
                        npc.interact(self.dialogue_system)
                        break
                else:
                    # Si aucun PNJ, ouvrir l'inventaire
                    self.inventory.toggle()
            
            elif event.key == pygame.K_q:
                self.quest_manager.show_quests = not self.quest_manager.show_quests
            
            elif event.key == pygame.K_SPACE:
                self.attempt_attack()
            
            elif event.key == pygame.K_s:
                # Sauvegarder la partie
                self.save_system.save_game(
                    self.player, self.environment, self.quest_manager
                )
                self.ui.messages.append("Partie sauvegardée!")
    
    def handle_combat_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Attaque normale
                damage = self.player.attack(self.combat_monster)
                self.ui.combat_messages.append(f"Ycrad inflige {damage} dégâts!")
                self.combat_turn = "monster"
                self.combat_timer = pygame.time.get_ticks()
            
            elif event.key == pygame.K_2 and len(self.player.skills) > 1:  # Compétence 1
                damage = self.player.use_skill(1, self.combat_monster)
                self.ui.combat_messages.append(
                    f"Ycrad utilise {self.player.skills[1].name} et inflige {damage} dégâts!"
                )
                self.combat_turn = "monster"
                self.combat_timer = pygame.time.get_ticks()
            
            elif event.key == pygame.K_3:  # Fuir
                if random.random() < 0.5:  # 50% de chance de fuite
                    self.ui.combat_messages.append("Vous avez fui le combat!")
                    self.game_state = "playing"
                else:
                    self.ui.combat_messages.append("Fuite échouée!")
                    self.combat_turn = "monster"
                    self.combat_timer = pygame.time.get_ticks()
    
    def handle_dialogue_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                next_line = self.dialogue_system.next_line()
                if not next_line:
                    self.game_state = "playing"
                    self.interacting_npc = None
            
            elif event.key == pygame.K_ESCAPE:
                self.dialogue_system.end_dialogue()
                self.game_state = "playing"
                self.interacting_npc = None
    
    def attempt_attack(self):
        # Vérifier s'il y a un monstre à proximité pour combattre
        for monster in self.environment.get_monsters_in_current_zone(self.current_zone):
            distance = self.calculate_distance(self.player.position, monster.position)
            if distance < 50:
                self.start_combat(monster)
                self.audio_manager.play_sound("combat_start")
                break
    
    def start_combat(self, monster):
        self.game_state = "combat"
        self.combat_monster = monster
        self.combat_turn = "player"
        self.combat_timer = pygame.time.get_ticks()
        self.audio_manager.play_music("combat")
    
    def resolve_combat_turn(self):
        current_time = pygame.time.get_ticks()
        
        if self.combat_turn == "player" and current_time - self.combat_timer > 2000:
            # Tour du joueur timeout, attaque automatique
            damage = self.player.attack(self.combat_monster)
            self.ui.combat_messages.append(f"Ycrad inflige {damage} dégâts!")
            self.combat_turn = "monster"
            self.combat_timer = current_time
        
        elif self.combat_turn == "monster" and current_time - self.combat_timer > 2000:
            # Tour du monstre
            damage = self.combat_monster.attack(self.player)
            self.ui.combat_messages.append(f"Le {self.combat_monster.name} inflige {damage} dégâts!")
            self.combat_turn = "player"
            self.combat_timer = current_time
            
            # Vérifier la victoire/défaite
            if self.player.hp <= 0:
                self.ui.combat_messages.append("Vous avez été vaincu!")
                self.game_state = "game_over"
                self.audio_manager.play_sound("game_over")
                return
        
        # Vérifier si le monstre est vaincu
        if self.combat_monster.hp <= 0:
            self.ui.combat_messages.append(f"Vous avez vaincu le {self.combat_monster.name}!")
            xp_gained = self.combat_monster.xp_reward
            gold_gained = self.combat_monster.gold_reward
            self.player.gain_xp(xp_gained)
            self.player.gold += gold_gained
            
            loot = self.combat_monster.generate_loot()
            for item in loot:
                self.inventory.add_item(item)
            
            self.ui.messages.append(
                f"Victoire! +{xp_gained} XP, +{gold_gained} or, butin: {', '.join([i.name for i in loot])}"
            )
            
            self.game_state = "playing"
            self.audio_manager.play_music(self.current_zone)
            self.audio_manager.play_sound("victory")
            
            # Mettre à jour les quêtes
            self.quest_manager.on_monster_killed(self.combat_monster.type)
    
    def calculate_distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def update(self):
        # Mettre à jour selon l'état du jeu
        if self.game_state == "menu":
            self.main_menu.update()
        
        elif self.game_state == "playing":
            self.update_playing_state()
        
        elif self.game_state == "combat":
            self.update_combat_state()
        
        # Mettre à jour les animations
        self.animation_manager.update(self.clock.get_time())
    
    def update_playing_state(self):
        # Mettre à jour la position du joueur
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 1
        
        if dx != 0 or dy != 0:
            self.player.move(dx, dy)
            
            # Vérifier les collisions avec l'environnement
            if self.environment.check_collision(self.player.position):
                self.player.move(-dx, -dy)
            
            # Vérifier les collisions avec les PNJs
            for npc in self.npcs:
                if self.calculate_distance(self.player.position, npc.position) < 20:
                    self.player.move(-dx, -dy)
                    break
            
            # Mettre à jour l'animation de marche
            self.animation_manager.play_animation("player", "walk")
        else:
            # Animation idle si pas de mouvement
            self.animation_manager.play_animation("player", "idle")
        
        # Vérifier les déclencheurs de quêtes
        self.quest_manager.check_triggers(self.player.position)
        
        # Vérifier le changement de zone
        new_zone = self.environment.get_zone_at_position(self.player.position)
        if new_zone != self.current_zone:
            self.current_zone = new_zone
            self.ui.messages.append(f"Vous entrez dans {new_zone}")
            self.audio_manager.play_music(new_zone)
    
    def update_combat_state(self):
        self.resolve_combat_turn()
    
    def render(self):
        # Effacer l'écran
        self.screen.fill((0, 0, 0))
        
        # Rendu selon l'état du jeu
        if self.game_state == "menu":
            self.main_menu.draw(self.screen)
        
        elif self.game_state == "playing":
            self.render_playing_state()
        
        elif self.game_state == "combat":
            self.render_combat_state()
        
        elif self.game_state == "dialogue":
            self.render_dialogue_state()
        
        elif self.game_state == "game_over":
            self.render_game_over()
        
        # Mettre à jour l'affichage
        pygame.display.flip()
    
    def render_playing_state(self):
        # Dessiner l'environnement
        self.screen.blit(self.assets["environments"][self.current_zone], (0, 0))
        
        # Dessiner les PNJs
        for npc in self.npcs:
            self.screen.blit(self.assets["npcs"][npc.type], npc.position)
        
        # Dessiner les monstres
        for monster in self.environment.get_monsters_in_current_zone(self.current_zone):
            self.screen.blit(self.assets["monsters"][monster.type], monster.position)
        
        # Dessiner le joueur avec animation
        player_frame = self.animation_manager.get_current_frame()
        if player_frame:
            self.screen.blit(player_frame, self.player.position)
        else:
            self.screen.blit(self.assets["player"], self.player.position)
        
        # Dessiner l'UI
        self.ui.draw(self.screen, self.game_state)
    
    def render_combat_state(self):
        # Fond de combat
        self.screen.fill((30, 0, 0))  Fond rouge sombre
        
        # Dessiner le joueur et le monstre
        self.screen.blit(self.assets["player"], (200, 300))
        self.screen.blit(self.assets["monsters"][self.combat_monster.type], (500, 300))
        
        # Dessiner l'UI de combat
        self.ui.draw(self.screen, self.game_state)
    
    def render_dialogue_state(self):
        # Dessiner l'environnement en arrière-plan
        self.screen.blit(self.assets["environments"][self.current_zone], (0, 0))
        
        # Boîte de dialogue
        dialogue_box = pygame.Surface((700, 150), pygame.SRCALPHA)
        dialogue_box.fill((0, 0, 0, 200))
        self.screen.blit(dialogue_box, (50, 400))
        
        # Texte de dialogue
        current_line = self.dialogue_system.get_current_line()
        if current_line:
            font = pygame.font.SysFont("Arial", 20)
            text = font.render(current_line, True, (255, 255, 255))
            self.screen.blit(text, (70, 420))
            
            # Indicateur de continuation
            continue_text = font.render("Appuyez sur ENTREE pour continuer...", True, (200, 200, 200))
            self.screen.blit(continue_text, (70, 470))
    
    def render_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text, (400 - text.get_width() // 2, 250))
        
        font = pygame.font.SysFont("Arial", 24)
        restart_text = font.render("Appuyez sur R pour recommencer", True, (255, 255, 255))
        self.screen.blit(restart_text, (400 - restart_text.get_width() // 2, 320))
    
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