# menu.py - Système de menu principal
class MainMenu:
    def __init__(self, game):
        self.game = game
        self.options = ["Nouvelle Partie", "Charger Partie", "Options", "Quitter"]
        self.selected_option = 0
        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        # Animation de fond
        self.background = self.create_animated_background()
    
    def create_animated_background(self):
        # Créer un fond animé avec des particules
        background = pygame.Surface((800, 600))
        background.fill((0, 0, 0))
        return background
    
    def update(self):
        # Mettre à jour l'animation de fond
        pass
    
    def draw(self, screen):
        # Dessiner le fond
        screen.blit(self.background, (0, 0))
        
        # Dessiner le titre
        title = self.title_font.render("YCRAD L'AVENTURIER", True, (255, 215, 0))
        screen.blit(title, (400 - title.get_width() // 2, 100))
        
        # Dessiner les options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            screen.blit(text, (400 - text.get_width() // 2, 250 + i * 50))
        
        # Dessiner les informations de copyright
        copyright_text = self.font.render("© 2024 VotreStudio", True, (100, 100, 100))
        screen.blit(copyright_text, (400 - copyright_text.get_width() // 2, 550))
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()
    
    def select_option(self):
        if self.selected_option == 0:  # Nouvelle Partie
            self.game.start_new_game()
        elif self.selected_option == 1:  # Charger Partie
            self.game.show_load_menu()
        elif self.selected_option == 2:  # Options
            self.game.show_options_menu()
        elif self.selected_option == 3:  # Quitter
            self.game.running = False
