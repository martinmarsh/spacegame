import pyxel
import os
from ground import Ground
from object_helpers import PyxelObjectPool
from score import Score
from player import Player
from config import W, H, GAMEPAD_1_X, GAMEPAD_1_Y, GAMEPAD_1_UP, GAMEPAD_1_DOWN, GAMEPAD_1_L2, GAMEPAD_1_R2
import glfw

ASSET_PATH = f"{os.getcwd()}/assets.pyxel"


class Game:

    def __init__(self):
        pyxel.init(W - 1, H - 1, caption="", fps=60)
        pyxel.load(ASSET_PATH)
        self.ground = Ground(self)
        self.score = Score(self)
        self.player = Player(self)
        self.STATE = "INIT"
        self.bombs = self.shells = self.explosions = self.asteroids = None
        self.STATE = "PLAY"
        self.reset()
        self.joys = 0
        self.joy_x = 0
        self.joy_y = 0
        self.select_name = 0

    def reset(self):
        """
        Set up game here
        """
        self.ground.reset()
        self.score.reset()
        self.STATE = "INIT"
        self.explosions = PyxelObjectPool()
        self.shells = PyxelObjectPool()
        self.bombs = PyxelObjectPool()
        self.asteroids = PyxelObjectPool()
        
    def run(self):
        self.joys = 0
        for joy in range(glfw.JOYSTICK_1, glfw.JOYSTICK_LAST):
            if glfw.joystick_present(joy):
                self.joys += 1
        print("number of joysticks =", self.joys)
        pyxel.run(self.update, self.draw)

    def update(self):

        if self.joys:
            js, c = glfw.get_joystick_axes(glfw.JOYSTICK_1)
            self.joy_x = js[0] * 2
            self.joy_y = js[1] * 2

        if self.STATE == "INIT":
            self.score.list_order()
            num = len(self.score.ordered_names) + 1
            if pyxel.btnp(pyxel.KEY_X) or pyxel.btn(GAMEPAD_1_X):
                if self.select_name == num:
                    self.player.name_generator()
                else:
                    self.player.name = self.score.ordered_names[self.select_name - 1]
                self.STATE = "PLAY"
            else:

                if self.select_name < num and (pyxel.btnr(pyxel.KEY_DOWN) or pyxel.btnr(GAMEPAD_1_DOWN)
                                               or pyxel.btnr(GAMEPAD_1_L2)):
                    self.select_name += 1

                if self.select_name > 0 and (pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(GAMEPAD_1_UP) or
                                             pyxel.btnr(GAMEPAD_1_R2)):
                    self.select_name -= 1

        elif self.STATE == "PLAY":
            self.ground.update()
            self.player.update()
            self.score.update()
            self.explosions.update()
            self.shells.update()
            self.bombs.update()
            self.asteroids.update()
        elif self.STATE == "DEAD":
            # We use X on gamepad and not A which is for bombs to prevent accidental replay
            if pyxel.btn(pyxel.KEY_X) or pyxel.btn(GAMEPAD_1_X):
                name = self.player.name
                self.reset()
                self.player.name = name
                self.STATE = "PLAY"
            elif pyxel.btn(pyxel.KEY_Y) or pyxel.btn(GAMEPAD_1_Y):
                self.reset()
                self.STATE = "INIT"
                self.select_name = 0

    def draw(self):
        pyxel.cls(0)
        if self.STATE == "INIT":
            self.initialise()
        elif self.STATE == "PLAY":
            self.ground.draw()
            self.player.draw()
            self.score.draw()
            self.explosions.draw()
            self.shells.draw()
            self.bombs.draw()
            self.asteroids.draw()
        elif self.STATE == "DEAD":
            pyxel.blt(40, H/2 - 50, 1, 0, 0, 255, 86)
            pyxel.text((W/2) - 30, (H/2) + 30, f"Total Score: {self.score.total}", 8)
            pyxel.text((W / 2) - 30, (H / 2) + 60, f"Press X to try again as  {self.player.name}", 8)
            pyxel.text((W / 2) - 30, (H / 2) + 70, f"Press Y for list of players", 8)

    def initialise(self):
        self.score.list_order()
        x = W/2 - 80
        y = 60
        count = 1

        pyxel.text(x, 10, "Space Game", 8)

        for name in self.score.ordered_names:
            if count == self.select_name:
                text_colour = 7
            else:
                text_colour = 8
            pyxel.text(x, y, str(count), text_colour)
            pyxel.text(x + 20, y, name, text_colour)
            pyxel.text(x + 80, y, str(self.score.results[name]), text_colour)
            count += 1
            y += 10
        text_colour = 8
        if count == self.select_name:
            text_colour = 7
        pyxel.text(x, y, str(count), text_colour)
        pyxel.text(x + 20, y, "New Player", text_colour)

        pyxel.text((W/2) - 80, (H/2) + 50, "Use up or down keys to select player", 8)
        pyxel.text((W / 2) - 80, (H / 2) + 60, "Press 'X' to select", 8)


if __name__ == '__main__':
    Game().run()
