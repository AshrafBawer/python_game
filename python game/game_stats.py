
class GameStats:

    def __init__(self,ti_game):
        self.settings = ti_game.settings
        self.reset_stats()

        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        self.pencils_left = self.settings.pencil_limit
        self.score = 0
        self.level = 1
    
