import pygame

class Info:

    def __init__(self, ti_game):
        self.settings = ti_game.settings
        self.screen = ti_game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 30)

        info_str = "To toggle sound press : CTRL + w"
        self.info_image = self.font.render(info_str, True, self.text_color,
         self.settings.sb_background)
        
        self.info_rect = self.info_image.get_rect()
        self.info_rect.centerx = self.screen_rect.centerx
        self.info_rect.top = self.screen_rect.top + 200

        # it's the background of the image
        self.rect = pygame.Rect(0,0, 500, 60)
        self.rect.centery = self.info_rect.centery
        self.rect.centerx = self.info_rect.centerx

    def show_info(self):
        self.screen.fill(self.settings.sb_background, self.rect)
        self.screen.blit(self.info_image, self.info_rect)