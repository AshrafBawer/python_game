import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    
    def __init__(self,ti_game):

        super().__init__()

        self.screen = ti_game.screen
        self.settings = ti_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ti_game.pencil.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    # this function if called draw one bullet, and it will be called for every bullet in the bullets group
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    