from config import H, W, GAMEPAD_1_A, GAMEPAD_1_B, GAMEPAD_1_UP, GAMEPAD_1_LEFT, GAMEPAD_1_DOWN, GAMEPAD_1_RIGHT,\
    GAMEPAD_1_L, GAMEPAD_1_R, GAMEPAD_1_L2, GAMEPAD_1_R2

from weapon import Bomb
import pyxel
import random


class Player:

    def __init__(self, game):
        self.x = W / 2
        self.y = H / 3
        self.max_x = W - 50
        self.name = "Chris"
        self.game = game
        self.ground = game.ground
        self.score = game.score
        self.magazine = self.magazine_size = 3
        self.reload_timer = 120
        self.reload_counter = 0
        self.collision = False

    def reset(self):
        self.x = W / 2
        self.y = H / 3
        self.reload_timer = 120
        self.reload_counter = 0
        self.collision = False
        self.magazine = self.magazine_size
        self.reload_counter = self.reload_timer

    def draw(self):
        # Display player
        pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 0)

    def update(self):
        self.move()
        self.collision, _ = self.ground.collision(self.x, self.y)
        if self.collision:
            # update player hit count
            self.score.player_hit()
            pyxel.play(0, 1)
            self.reset()

        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(GAMEPAD_1_A) or pyxel.btn(GAMEPAD_1_B)) and self.magazine > 0:
            self.game.bombs.insert(Bomb(self.game, self.x, self.y))
            self.magazine -= 1

        self.reload_counter -= 1
        if self.reload_counter < 1:
            self.magazine = self.magazine_size
            self.reload_counter = self.reload_timer

    def move(self):
        if self.game.joys:
            self.x += self.game.joy_x
            self.y += self.game.joy_y

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(GAMEPAD_1_UP) or pyxel.btn(GAMEPAD_1_R2):
            self.y -= 2

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(GAMEPAD_1_DOWN) or pyxel.btn(GAMEPAD_1_L2):
            self.y += 2

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(GAMEPAD_1_LEFT) or pyxel.btn(GAMEPAD_1_L):
            self.x -= 2

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(GAMEPAD_1_RIGHT) or pyxel.btn(GAMEPAD_1_R):
            self.x += 2

        self.y = max(self.y, 15)
        # always hits ground or below before reaching max y
        self.x = min(self.x, self.max_x)
        self.x = max(self.x, 50)

    def name_generator(self):
        color = ["Red", "Blue", "Black", "White"]
        tool = ["Hammer", "Drill", "Cutter", "Knife"]
        searching = True
        while searching:
            random_number1 = random.randrange(0, len(color))
            random_number2 = random.randrange(0, len(tool))
            self.name = color[random_number1] + " " + tool[random_number2]
            if self.name not in self.score.ordered_names:
                searching = False


