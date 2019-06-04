from config import W, H
from weapon import Bomb
import pyxel
import random


class Player:

    def __init__(self, game):
        self.player_x = W/2
        self.player_y = H/3
        self.name = "Chris"
        self.game = game
        self.ground = game.ground
        self.score = game.score
        self.player_collision = False

    def reset(self):
        self.player_x = W/2
        self.player_y = H/3
        self.player_collision = False

    def draw(self):
        # Display player
        pyxel.blt(self.player_x, self.player_y, 0, 32, 0, 16, 16, 0)

    def update(self):
        self.player_move()
        self.player_collision, _ = self.ground.collision(self.player_x, self.player_y)
        if self.player_collision:
            # update player hit count
            self.score.player_hit()
            pyxel.play(0, 1)
            self.reset()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game.bombs.insert(Bomb(self.game, self.player_x, self.player_y))

    def player_move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= 2

        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += 2

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2

    def name_generator(self):
        color = ["Red", "Blue", "Black", "White"]
        tool = ["Hammer", "Drill", "Cutter", "Knife"]
        random_number1 = random.randrange(0, len(color))
        random_number2 = random.randrange(0, len(tool))
        self.name = color[random_number1] + " " + tool[random_number2]
