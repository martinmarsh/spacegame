from config import W, H
from weapon import Bomb
import pyxel


class Player():

    def __init__(self, game):
        self.player_x = W/2
        self.player_y = H/3
        self.bomb = None
        self.bomb_dropped = False
        self.ground = game.ground
        self.score = game.score
        self.bomb_collision = self.player_collision = False

    def reset(self):
        self.player_x = W/2
        self.player_y = H/3

    def draw(self):
        if self.player_collision:
            # Display explosion
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16)
            # update player hit count
            self.score.player_hit()
            self.reset()
        else:
            # Display player
            pyxel.blt(self.player_x, self.player_y, 0, 32, 0, 16, 16)
        if self.bomb:
            self.bomb.draw()

    def update(self):
        self.player_move()
        self.player_collision, obj = self.ground.collision(self.player_x, self.player_y)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bomb = Bomb(self.player_x, self.player_y)
            self.bomb_dropped = True

        if self.bomb_dropped:
            self.bomb.update()
            self.bomb_collision, obj = self.ground.collision(self.bomb.bomb_x, self.bomb.bomb_y)
            if self.bomb_collision:
                self.bomb.explode_bomb()

    def player_move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = self.player_y - 2

        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = self.player_y + 2
