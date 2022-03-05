import pygame
from pygame.sprite import Sprite

class Talib(Sprite):

    def __init__(self, ti_game):
        super().__init__()
        self.screen = ti_game.screen
        self.settings = ti_game.settings

        self.image = pygame.image.load('talib.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    # the function runs on every loop and update the horizontal position of the talib
    def update(self):
        self.x += (self.settings.talib_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    '''
    check if any talibs rect position got higher than the right of the screen or the left, which means
    if hits the edges of the screen return true
    '''
    def check_edges(self):
        screen_rect = self.screen.get_rect()

        if(self.rect.right >= screen_rect.right or self.rect.left <= 0):
            return True