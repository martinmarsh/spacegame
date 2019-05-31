import pyxel
import os
from background import Ground
from score import Score
from shells import Shells
from player import Player
from config import W, H

ASSET_PATH = f"{os.getcwd()}/assets.pyxel"


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        pyxel.load(ASSET_PATH)
        self.ground = Ground(self)
        self.shells = Shells(self)
        self.score = Score(self)
        self.player = Player(self)
        self.STATE = "PLAY"
        self.reset()

    def reset(self):
        """
        Set up game here
        """
        self.ground.reset()
        self.score.reset()
        self.shells.reset()
        self.STATE = "PLAY"

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.STATE == "PLAY":
            self.ground.update()
            self.player.update()
            self.score.update()
            self.shells.update()

    def draw(self):
        pyxel.cls(0)
        if self.STATE == "PLAY":
            self.ground.draw()
            self.player.draw()
            self.score.draw()
            self.shells.draw()
        elif self.STATE == "DEAD":
            pyxel.blt(40, H/2 - 50, 1, 0, 0, 255, 86)
            pyxel.text((W/2) - 30, (H/2) + 30, f"Total Score: {self.score.total}", 8)


if __name__ == '__main__':
    Game().run()
