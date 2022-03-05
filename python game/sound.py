import pygame

class Sound:

    def __init__(self, ti):
        self.settings = ti.settings
        self.bullet_sound = pygame.mixer.Sound("bullet_sound.mp3")
        self.talib_hit_sound = pygame.mixer.Sound("hit.mp3")
        self.talib_hit_sound.set_volume(0.1)

    def bullet(self):
        if self.settings.sound_active:
            pygame.mixer.Sound.play(self.bullet_sound)
            pygame.mixer.music.stop()  

    def talib_hit(self):
        if self.settings.sound_active:
            pygame.mixer.Sound.play(self.talib_hit_sound)
            pygame.mixer.music.stop() 

