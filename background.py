from config import W
from random import randrange
import pyxel


class Ground:

    def __init__(self):
        self.baseline = None
        self.rate = None
        self.yo = None
        self.yx = self.yo = None

    def reset(self):
        self.baseline = []
        self.rate = 1
        self.yo = 200
        self.yx = self.yo
        for yd in range(1, W):
            self.ground_add()

    def draw(self):
        x = 0
        y = self.yo
        for y2 in self.baseline:
            x2 = x + 1
            pyxel.line(x, y, x2, y2, 11)
            x = x2
            y = y2

    def update(self):
        self.yo = self.baseline.pop(0)
        self.ground_add()

    def ground_add(self):
        if randrange(1, 100) == 7:
            self.yx = 200 + randrange(-30, 31)
        if randrange(-10, 10) == 0:
            self.rate = -self.rate

        self.yx = self.yx + randrange(0, 3) * self.rate
        if self.yx > 230:
            self.yx = 200
        elif self.yx < 150:
            self.yx = 200
        self.baseline.append(self.yx)
