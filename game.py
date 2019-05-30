import pyxel
from background import Ground
from config import W, H


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        self.ground = Ground()
        self.reset()

    def reset(self):
        """
        Set up game here
        """
        self.ground = self.ground.reset()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ground.update()

    def draw(self):
        pyxel.cls(0)
        self.ground.draw()


if __name__ == '__main__':
    Game().run()
