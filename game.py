import pyxel
import os
from background import Ground
from player import Player
from config import W, H

ASSET_PATH = f"{os.getcwd()}/assets.pyxel"


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        pyxel.load(ASSET_PATH)
        self.ground = Ground()
        self.player = Player(self.ground)
        self.reset()

    def reset(self):
        """
        Set up game here
        """
        self.ground.reset()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ground.update()
        self.player.update()
        pass

    def draw(self):
        pyxel.cls(0)
        self.ground.draw()
        self.player.draw()


if __name__ == '__main__':
    Game().run()
