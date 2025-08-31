# ui.py - Interface utilisateur
class UI:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.font = pygame.font.SysFont("Arial", 16)
        self.messages = []
        self.combat_messages = []
    
    def draw(self, screen, game_state):
        # Dessiner la barre de vie
        self.draw_bar(screen, 10, 10, 200, 20, self.player.hp / self.player.max_hp, (255, 0, 0))
        
        # Dessiner la barre de mana
        self.draw_bar(screen, 10, 40, 200, 20, self.player.mp / self.player.max_mp, (0, 0, 255))
        
        # Afficher le niveau et l'XP
        level_text = self.font.render(f"Niveau: {self.player.level} XP: {self.player.xp}/{self.player.xp_to_next_level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 70))
        
        # Afficher la classe actuelle
        class_text = self.font.render(f"Classe: {self.player.current_class.name}", True, (255, 255, 255))
        screen.blit(class_text, (10, 90))
        
        # Afficher l'or
        gold_text = self.font.render(f"Or: {self.player.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (10, 110))
        
        # Afficher les messages récents
        for i, message in enumerate(self.messages[-3:]):
            msg_text = self.font.render(message, True, (255, 255, 255))
            screen.blit(msg_text, (10, 140 + i * 20))
        
        # Interface spécifique selon l'état du jeu
        if game_state == "combat":
            self.draw_combat_ui(screen)
        elif self.inventory.is_open:
            self.draw_inventory(screen)
        elif self.player.quest_manager.show_quests:
            self.draw_quests(screen)
    
    def draw_bar(self, screen, x, y, width, height, ratio, color):
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(screen, color, (x, y, width * ratio, height))
        pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)
    
    def draw_combat_ui(self, screen):
        # Fond semi-transparent pour l'interface de combat
        s = pygame.Surface((800, 200), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 400))
        
        # Afficher les messages de combat
        for i, message in enumerate(self.combat_messages[-5:]):
            msg_text = self.font.render(message, True, (255, 255, 255))
            screen.blit(msg_text, (20, 410 + i * 20))
        
        # Afficher les actions de combat
        actions = ["Attaquer", "Compétence", "Objet", "Fuir"]
        for i, action in enumerate(actions):
            action_text = self.font.render(f"{i+1}. {action}", True, (255, 255, 255))
            screen.blit(action_text, (600, 410 + i * 30))
    
    def draw_inventory(self, screen):
        # Fond de l'inventaire
        s = pygame.Surface((600, 400), pygame.SRCALPHA)
        s.fill((0, 0, 0, 220))
        screen.blit(s, (100, 100))
        
        # Titre
        title = self.font.render("INVENTAIRE", True, (255, 255, 255))
        screen.blit(title, (350, 110))
        
        # Équipement actuel
        equip_title = self.font.render("ÉQUIPÉ:", True, (255, 255, 255))
        screen.blit(equip_title, (120, 140))
        
        y_pos = 160
        for slot, item in self.player.equipment.items():
            slot_text = self.font.render(f"{slot.capitalize()}: {item.name if item else 'Aucun'}", True, (255, 255, 255))
            screen.blit(slot_text, (120, y_pos))
            y_pos += 25
        
        # Liste des objets
        items_title = self.font.render("OBJETS:", True, (255, 255, 255))
        screen.blit(items_title, (350, 140))
        
        for i, item in enumerate(self.inventory.items[:10]):  # Afficher les 10 premiers
            item_text = self.font.render(f"{i+1}. {item.name}", True, (255, 255, 255))
            screen.blit(item_text, (350, 160 + i * 20))
    
    def draw_quests(self, screen):
        # Similaire à draw_inventory mais pour les quêtes
        pass
    
    def handle_event(self, event):
        # Gérer les interactions avec l'UI
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            # Vérifier les clics sur les éléments d'interface
            pass
