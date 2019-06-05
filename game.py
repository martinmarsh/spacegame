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
            self.score.list_order()
            name = False
            if pyxel.btnp(pyxel.KEY_N):
                self.player.name_generator()
                self.STATE = "PLAY"
            else:
                try:
                    if pyxel.btnp(pyxel.KEY_1):
                        name = self.score.ordered_names[0]
                    elif pyxel.btnp(pyxel.KEY_2):
                        name = self.score.ordered_names[1]
                    elif pyxel.btnp(pyxel.KEY_3):
                        name = self.score.ordered_names[2]
                    elif pyxel.btnp(pyxel.KEY_4):
                        name = self.score.ordered_names[3]
                    elif pyxel.btnp(pyxel.KEY_5):
                        name = self.score.ordered_names[4]
                    elif pyxel.btnp(pyxel.KEY_6):
                        name = self.score.ordered_names[5]
                    elif pyxel.btnp(pyxel.KEY_7):
                        name = self.score.ordered_names[6]
                    elif pyxel.btnp(pyxel.KEY_8):
                        name = self.score.ordered_names[7]
                except IndexError:
                    pass
                if name:
                    self.player.name = name
                    self.STATE = "PLAY"

        elif self.STATE == "PLAY":
            self.ground.update()
            self.player.update()
            self.score.update()
            self.guns.update()
            self.explosions.update()
            self.shells.update()
            self.bombs.update()
        elif self.STATE == "DEAD":
            if pyxel.btn(pyxel.KEY_0):
                name = self.player.name
                self.reset()
                self.player.name = name
                self.STATE = "PLAY"
            elif pyxel.btn(pyxel.KEY_1):
                self.reset()
                self.STATE = "INIT"

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
            pyxel.text((W / 2) - 30, (H / 2) + 60, f"Press 0 to try again as  {self.player.name}", 8)
            pyxel.text((W / 2) - 30, (H / 2) + 70, f"Press 1 for list of players", 8)

    def initialise(self):
        self.score.list_order()
        x = W/2 - 80
        y = 30
        count = 1
        for name in self.score.ordered_names:
            pyxel.text(x, y, str(count), 8)
            pyxel.text(x + 20, y, name, 8)
            pyxel.text(x + 80, y, str(self.score.results[name]), 8)
            count += 1
            y += 10
        pyxel.text((W/2) - 80, (H/2) + 30, "Select the number next to your alias to replay or", 8)
        pyxel.text((W / 2) - 80, (H / 2) + 40, "To play as new user, hit letter 'N", 8)


if __name__ == '__main__':
    Game().run()
