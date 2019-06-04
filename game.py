import pyxel
import os
from background import Ground
from object_helpers import ObjectPool
from score import Score
from shells import Guns
from player import Player
from config import W, H

ASSET_PATH = f"{os.getcwd()}/assets.pyxel"


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        pyxel.load(ASSET_PATH)
        self.ground = Ground(self)
        self.score = Score(self)
        self.player = Player(self)
        self.STATE = "INIT"
        self.guns = Guns(self)
        self.bombs = self.shells = self.explosions = None
        self.STATE = "PLAY"
        self.reset()

    def reset(self):
        """
        Set up game here
        """
        self.ground.reset()
        self.score.reset()
        self.guns.reset()
        self.STATE = "INIT"
        self.guns.reset()
        self.explosions = ObjectPool()
        self.shells = ObjectPool()
        self.bombs = ObjectPool()
        
    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.STATE == "INIT":
            self.initialise()
        elif self.STATE == "PLAY":
            self.ground.update()
            self.player.update()
            self.score.update()
            self.guns.update()
            self.explosions.update()
            self.shells.update()
            self.bombs.update()

    def draw(self):
        pyxel.cls(0)
        if self.STATE == "INIT":
            self.initialise()
        elif self.STATE == "PLAY":
            self.ground.draw()
            self.player.draw()
            self.score.draw()
            self.guns.draw()
            self.explosions.draw()
            self.shells.draw()
            self.bombs.draw()
        elif self.STATE == "DEAD":
            pyxel.blt(40, H/2 - 50, 1, 0, 0, 255, 86)
            pyxel.text((W/2) - 30, (H/2) + 30, f"Total Score: {self.score.total}", 8)

    def initialise(self):
        pyxel.text((W/2) - 30, (H/2) + 30, "Please choose a name, hit letter 'N", 8)

        if pyxel.btnp(pyxel.KEY_N):
            self.player.name_generator()
            self.STATE = "PLAY"


if __name__ == '__main__':
    Game().run()
