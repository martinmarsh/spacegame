from config import W, H
import pyxel


class Bomb:

    def __init__(self, x, y):
        self.bomb_x = x
        self.bomb_width = self.bomb_x + 3
        self.bomb_height = 6
        self.bomb_y = y
        self.bomb_count = 0
        self.ground_level = 160
        self.colour = 3
        self.bomb_exploded = False

    def reset(self):
        self.bomb_x = 0
        self.bomb_width = self.bomb_x + 3
        self.bomb_height = 6
        self.bomb_y = 0
        self.bomb_count = 0
        self.bomb_exploded = False

    def draw(self):
        if self.bomb_exploded:
            # pyxel.blt(self.bomb_x, self.bomb_y, 0, 16, 0, 16, 16)
            self.bomb_exploded = False
        elif self.bomb_x != 0:
            pyxel.blt(self.bomb_x, self.bomb_y, 0, 8, 0, 8, 8)

    def update(self):
        if self.bomb_x != 0:
            self.drop_bomb()

    def drop_bomb(self):
        self.bomb_y = self.bomb_y + 4
        self.bomb_count = 1

    def explode_bomb(self):
        self.bomb_count = 0
        self.bomb_exploded = True
        self.reset()
