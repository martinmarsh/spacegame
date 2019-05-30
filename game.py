import pyxel
from background import Ground
from weapon import Bomb
from config import W, H


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        pyxel.load("assets.pyxel")
        self.ground = Ground()
        self.bomb = Bomb()
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
        self.bomb.update()
        pass

    def draw(self):
        pyxel.cls(0)
        self.ground.draw()
        self.bomb.draw()


if __name__ == '__main__':
    Game().run()
