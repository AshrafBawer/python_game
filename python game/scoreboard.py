import pygame.font
from pygame.sprite import Group
from pencil import Pencil

class Scoreboard:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 30)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_pencils()


        self.width, self.height = self.screen.get_rect().width, 50
        self.background_color = (220,220,220)
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.top = self.screen_rect.top
        
    
    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "Score : {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.sb_background)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    '''
    Here we draw images that we create in the prep_* on the screen, in the prep_* methods
    we only define an image and assign it to self.level_image for example and then we can use it 
    anywhere we want.
    '''
    def show_score(self):
        self.screen.fill(self.settings.sb_background, self.rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.pencils.draw(self.screen)
        

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score : {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
         self.settings.sb_background)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        
    '''
    check if the current score is higher than the high score and update
    the high score properly and then create an image of it
    '''
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # prep_level will create an image with the level value at the center of it and define it's position
    def prep_level(self):
        level_str = "Level:" + str(self.stats.level) 
        self.level_image = self.font.render(level_str, True, 
                    self.text_color, self.settings.sb_background)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.left - 100
        self.level_rect.top = self.score_rect.top
    
    def prep_pencils(self):
        self.pencils = Group()
        for pencil_number in range(self.stats.pencils_left):
            pencil = Pencil(self.ai_game)
            pencil.image = pygame.transform.scale(pencil.image, (20,30))
            pencil.rect.x = 10 + pencil_number * pencil.rect.width
            pencil.rect.y = 10
            self.pencils.add(pencil)

