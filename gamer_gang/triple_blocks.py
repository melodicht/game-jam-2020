import os
from pathlib import Path
import sys
sys.path.insert(0, Path(__file__).parent)
from mechanics.menuCrap import *
from mechanics.baseLevelAndPhysics import *
from dumbConstants import *


class ActualGame(arcade.Window):  # TODO: relative imports and crap
    def __init__(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def setup(self):
        self.menuView = MenuView()
        self.gameOver = GameOverView()
        self.levels = {1: BaseLevel()}
        self.current_view = self.menuView
        self.game_over = False
        self.show_view(self.current_view)

def main():
    game = ActualGame()
    game.setup()
    arcade.run()

main()
