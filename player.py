from config import W, H
from weapon import Bomb
import pyxel
import random


class Player:

    def __init__(self, game):
        self.x = W / 2
        self.y = H / 3
        self.max_x = H - 50
        self.name = "Chris"
        self.game = game
        self.ground = game.ground
        self.score = game.score
        self.collision = False

    def reset(self):
        self.x = W / 2
        self.y = H / 3
        self.collision = False

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

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game.bombs.insert(Bomb(self.game, self.x, self.y))

    def move(self):

        if pyxel.btn(pyxel.KEY_UP) and self.y > 20:
            self.y -= 2

        if pyxel.btn(pyxel.KEY_DOWN):      # always hits ground or below before reaching H
            self.y += 2

        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 50:
            self.x -= 2

        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < self.max_x:
            self.x += 2

    def name_generator(self):
        color = ["Red", "Blue", "Black", "White"]
        tool = ["Hammer", "Drill", "Cutter", "Knife"]
        random_number1 = random.randrange(0, len(color))
        random_number2 = random.randrange(0, len(tool))
        self.name = color[random_number1] + " " + tool[random_number2]
