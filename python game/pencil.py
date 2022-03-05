import pygame
from pygame.sprite import Sprite

class Pencil(Sprite):

    def __init__(self, ti_game):
        super().__init__()

        self.settings = ti_game.settings
        self.screen = ti_game.screen
        self.screen_rect = ti_game.screen.get_rect()

        self.image = pygame.image.load('pencil.png')
        self.image = pygame.transform.scale(self.image, (40,50))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x)
    
    def center_pencil(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        '''
        we add to x until moving_right variable is true and also check if it 
        reached the right corner of the screen then we stop adding to it
        Same for left
        '''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.pencil_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.pencil_speed
        self.rect.x = self.x
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)