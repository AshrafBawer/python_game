import sys
from time import sleep

import pygame

from settings import Settings
from pencil import Pencil
from bullet import Bullet
from talib import Talib
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound
from info import Info

class TalibInvasion:
    def __init__(self):
        pygame.init() 
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
         self.settings.screen_width
        ,self.settings.screen_height))
        pygame.display.set_caption("Taliban Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound(self)
        self.info = Info(self)

        self.pencil = Pencil(self)
        # we create a bullets group to store all bullets fired into it
        self.bullets = pygame.sprite.Group()
        self.talibs = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")
    
    # This is the main function that will be run when the file is called
    def run_game(self):
        '''
        while the game is open, check all the events and make changes
        acordingly and update screen right after those changes
        '''
        while True:
            self._check_events()
            
            # show the game is active then update pencil, talibs, and bullets
            if self.stats.game_active:
                self.pencil.update()
                self._update_bullets()
                self._update_talibs()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # for continue movment we need to set a variable to true and do something until it's true
            self.pencil.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.pencil.moving_left = True
        elif event.key == pygame.K_SPACE:
            # only create bullets if the game is active
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_w:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL:
                if self.settings.sound_active:
                    self.settings.sound_active = False
                else:
                    self.settings.sound_active = True            

    def _check_keyup_events(self, event):
        '''
        if the right or left key is no longer pressed then set
        the moving_right and left to false so the pencil stop moving in that direction
        '''
        if event.key == pygame.K_RIGHT:
            self.pencil.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.pencil.moving_left = False      

    def _check_play_button(self, mouse_pos):
        # check if the position that the mouse clicked is within the play button rectangular
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        '''
        if the play button is clicked and the game was in not active mode then start the game
        because the button will be clicked even if it's not visible to the user.
        all we do here is define our values then the update_screen will be run after this that
        will use these values to draw on the screen
        '''
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True  
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_pencils()

            pygame.mouse.set_visible(False)

            self.talibs.empty()
            self.bullets.empty()

            self._create_fleet()
            self.pencil.center_pencil()

            self.settings.initialize_dynamic_settings()

    def _fire_bullet(self):
        self.sound.bullet()
        # a certain amount of bullets can be allowed at one time on the screen
        if len(self.bullets) < self.settings.bullets_allowed:
            # everytime space button is clicked, we create a bullet and add it to bullets group
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    '''
    Here we update the position of each bullet on every loop and if the position is off
    the screen then we remove it from the list and we also check if any bullet is colided with 
    any talibs
    '''
    def _update_bullets(self):
        # update method will be run for all the bullets that are inside the bullets group
        self.bullets.update()

        '''
        we can't remove an element from a list that is being iterated, so we iterate over a copy 
        and remove elements from the original one
        '''
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_talib_collisions()

    '''
    firstly check if any talib hit the edge of the screen, then run the update function for every 
    talib in the talibs group, then check if any talib collided with the pencil, if yes then call
    pencil_hit function then check if any talib hit the bottom of the screen
    '''
    def _update_talibs(self):
        self._check_fleet_edges()
        self.talibs.update()

        if pygame.sprite.spritecollideany(self.pencil, self.talibs):
            self._pencil_hit()

        self._check_talibs_bottom()

    '''
    now after all values are updated, it's time to draw them on the screen
    '''
    def _update_screen(self):
        # give the background a color
        self.screen.fill(self.settings.bg_color)
        # draw the pencil on the screen
        self.pencil.blitme()
        # run draw function for every bullet in the bullets group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw every talib on the screen because talibs are just images, we only need to call
        # draw function fo each of them and pygame do the rest
        self.talibs.draw(self.screen)

        # draw all the scores on the screen
        self.sb.show_score()

        # if the game is not active then draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.info.show_info()

        '''
        this function makes the most recently drawn elements visible and remove the old one on every 
        loop iteration
        '''
        pygame.display.flip()

    def _create_fleet(self):
        talib = Talib(self)
        talib_width, talib_height = talib.rect.size
        available_space_x = self.settings.screen_width - (2* talib_width)
        number_talibs_x = available_space_x // (2*talib_width)

        pencil_height = self.pencil.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * talib_height) - pencil_height)
        number_rows = available_space_y // (2 * talib_height)

        for row_number in range(number_rows):
            for talib_number in range(number_talibs_x):
                self._create_talib(talib_number, row_number)
        

    def _create_talib(self, talib_number, row_number):
        talib = Talib(self)
        talib_width, talib_height = talib.rect.size
        talib.x = talib_width + 2 * talib_width * talib_number
        talib.rect.x = talib.x
        talib.rect.y = talib.rect.height + 2 * talib.rect.height * row_number
        self.talibs.add(talib)

    def _check_fleet_edges(self):
        '''
        check if any talibs in the talibs group hit the edge of the screen, if yes then 
        change direction of the fleet
        '''
        for talib in self.talibs.sprites():
            if talib.check_edges():
                self._change_fleet_direction()
                break

    '''
    for any talibs in the talibs group frop the fleet and then make the fleet direction oposite
    '''
    def _change_fleet_direction(self):
        for talib in self.talibs.sprites():
            # it means drop it by for example 10 points
            talib.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1
    
    def _check_bullet_talib_collisions(self):
        # check if and bullet is collided with any talibs, if yes then remove both of them (True, True)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.talibs, True, True
        )

 
        if collisions:
            self.sound.talib_hit()
            # if one bullet hit one or more than one talib then score it appropriatly
            for talibs in collisions.values():
                self.stats.score += self.settings.talib_points * len(talibs)
            # create new images of score and check the high score and update it properly
            self.sb.prep_score()
            self.sb.check_high_score()

        # if there no talibs left in the talibs group, then go to next level
        if not self.talibs:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
    
    '''
    check if I have any pencils left, if yes then subtract one from it and start again
    if not set the game active mode to false
    '''
    def _pencil_hit(self):

        if self.stats.pencils_left > 0:
            self.stats.pencils_left -= 1
            self.sb.prep_pencils()

            self.talibs.empty()
            self.bullets.empty()

            self._create_fleet()
            self.pencil.center_pencil()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    '''
    check if any talibs in the talibs group reached the bottom of the screen, if yes run the pencil hit
    '''
    def _check_talibs_bottom(self):
        screen_rect = self.screen.get_rect()
        for talib in self.talibs.sprites():
            if talib.rect.bottom >= screen_rect.bottom:
                self._pencil_hit()
                break

# only run the run_game if this file is called directly
if __name__ == '__main__':
    ti = TalibInvasion()
    ti.run_game()