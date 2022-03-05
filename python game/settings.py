
class Settings:

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        self.sb_background = (220,220,220)
        self.sound_active = True

        # bullets settings
        self.bullet_speed = 1.5
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 100

        #talibs Settings
        self.talib_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #pencil Settings
        self.pencil_speed = 1.5
        self.pencil_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.pencil_speed = 1.5
        self.bullet_speed = 3.0
        self.talib_speed = 1.0
        self.talib_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        self.pencil_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.talib_speed *= self.speedup_scale

        self.talib_points = int(self.talib_points * self.score_scale)

    
    