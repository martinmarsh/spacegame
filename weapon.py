from config import W, H
import pyxel


class Bomb:

    def __init__(self):
        self.player_x = W/2
        self.player_y = H/3
        self.bomb_x = self.player_x
        self.bomb_width = self.bomb_x + 3
        self.bomb_height = 6
        self.bomb_y = self.player_y
        self.bomb_count = 0
        self.ground_level = 160
        self.colour = 3
        self.bomb_exploded = False

    def reset(self):
        self.player_x = W/2
        self.player_y = H/3
        self.bomb_x = self.player_x
        self.bomb_width = self.bomb_x + 3
        self.bomb_height = 6
        self.bomb_y = self.player_y
        self.bomb_count = 0
        self.bomb_exploded = False

    def draw(self):
        pyxel.circ(self.player_x, self.player_y, 10, 8)
        if self.bomb_exploded:
            pyxel.blt(self.bomb_x, self.bomb_y, 0, 16, 0, 16, 16)
            self.bomb_exploded = False
        else:
            pyxel.blt(self.bomb_x, self.bomb_y, 0, 8, 0, 8, 8)

    def update(self):
        self.player_move()
        self.drop_bomb()

    def player_move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = self.player_y - 2

        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = self.player_y + 2

    def drop_bomb(self):
        self.bomb_y = self.bomb_y + 4

        if self.bomb_y > self.ground_level:
            self.explode_bomb()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bomb_y = self.player_y
            self.colour = 3
            self.bomb_count = 1

    def explode_bomb(self):
        self.bomb_count = 0
        self.bomb_exploded = True
