# audio.py - Système de son et musique
import pygame
import os

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.current_music = None
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.load_audio()
    
    def load_audio(self):
        # Charger les effets sonores
        sound_files = {
            "swing": "sounds/sword_swing.wav",
            "arrow": "sounds/arrow_shot.wav",
            "spell": "sounds/spell_cast.wav",
            "hit": "sounds/hit.wav",
            "level_up": "sounds/level_up.wav",
            "item_pickup": "sounds/item_pickup.wav"
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
        
        # Charger les musiques
        music_files = {
            "village": "music/village_theme.ogg",
            "forest": "music/forest_theme.ogg",
            "marsh": "music/marsh_theme.ogg",
            "combat": "music/combat_theme.ogg",
            "boss": "music/boss_theme.ogg"
        }
        
        for name, path in music_files.items():
            if os.path.exists(path):
                self.music[name] = path
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sound_volume)
            self.sounds[sound_name].play()
    
    def play_music(self, music_name, loops=-1):
        if music_name in self.music and self.current_music != music_name:
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
            self.current_music = music_name
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
    
    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        self.sound_volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
