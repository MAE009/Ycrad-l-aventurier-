# animation.py - Système d'animation avancé
class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames  # Liste des images/surfaces
        self.frame_duration = frame_duration  # Durée de chaque frame en ms
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.done = False
    
    def update(self, dt):
        if self.done:
            return
        
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.done = True
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.done = False

class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.load_animations()
    
    def load_animations(self):
        # Charger les animations pour chaque entité
        self.animations = {
            "player": {
                "idle": self.create_animation("player/idle", 4, 200),
                "walk": self.create_animation("player/walk", 6, 100),
                "attack": self.create_animation("player/attack", 4, 150, False),
                "cast": self.create_animation("player/cast", 5, 120, False)
            },
            "slime": {
                "idle": self.create_animation("monsters/slime/idle", 2, 300),
                "move": self.create_animation("monsters/slime/move", 4, 150)
            }
        }
    
    def create_animation(self, path, frame_count, duration, loop=True):
        frames = []
        for i in range(frame_count):
            # Charger l'image depuis le dossier correspondant
            frame_path = f"assets/{path}_{i}.png"
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                frames.append(frame)
            else:
                # Fallback: créer des surfaces colorées
                frames.append(pygame.Surface((16, 16), pygame.SRCALPHA))
        return Animation(frames, duration, loop)
    
    def play_animation(self, entity, animation_name):
        if entity in self.animations and animation_name in self.animations[entity]:
            self.current_animation = self.animations[entity][animation_name]
            self.current_animation.reset()
    
    def update(self, dt):
        if self.current_animation:
            self.current_animation.update(dt)
    
    def get_current_frame(self):
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None
