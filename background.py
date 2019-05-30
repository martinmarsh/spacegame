from config import W, H
from random import randrange
import pyxel


class Ground:

    def __init__(self):
        self.baseline = None
        self.rate = None
        self.yx = self.yo = None
        self.y_max = self.y_min = self.y_range = self.y_base = None

    def reset(self):
        self.baseline = []
        self.rate = 1
        self.y_base = H * 2//3
        self.y_range = H // 6
        self.y_max = self.y_base + self.y_range
        self.y_min = self.y_base - self.y_range

        self.yo = self.yx = self.y_base
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
        if self.yx > self.y_max:
            self.yx -= self.y_range
        elif self.yx < self.y_min:
            self.yx += self.y_range
        self.baseline.append(self.yx)
