from config import W, H
from random import randrange
import pyxel


class Ground:

    def __init__(self):
        self.lead_in = self.object_list = self.object_mask = self.ground_line = None
        self.sprite_lock_out = self.rate = None
        self.yx = self.yo = None
        self.y_max = self.y_min = self.y_range = self.y_base = None
        self.ground_colour = None

    def reset(self):
        self.ground_line = []
        self.object_mask = []
        self.object_list = []
        self.ground_colour = 9
        self.rate = 1
        self.y_base = H * 2//3
        self.y_range = H // 6
        self.lead_in = 32         # extra bit of buffer for adding sprites and allowing clean exit
        self.sprite_lock_out = 0
        self.y_max = self.y_base + self.y_range
        self.y_min = self.y_base - self.y_range
        self.yo = self.yx = self.y_base
        for yd in range(1, W + self.lead_in * 2):
            self.ground_add()

    def draw(self):
        x = 0
        y = self.yo
        end = W + self.lead_in
        pos = self.lead_in
        y = self.ground_line[pos]
        while pos < end:
            x = pos - self.lead_in
            if self.object_list[pos] != 0:
                obj = self.object_list[pos]
                # Draw object
                y = self.object_mask[pos]+1
                x2 = x
                while self.object_list[pos] != 0:
                    pos += 1
                    x2 += 1
                ybase = y + 17
                pyxel.line(x, ybase, x2, ybase, self.ground_colour)
                if obj == 2:
                    pyxel.blt(x, y, 0, 0, 16, 16, 16)
                else:
                    pyxel.blt(x, y, 0, 48, 0, 16, 16)
                y = ybase

            else:
                # Draw ground
                pos += 1
                y2 = self.ground_line[pos]
                pyxel.line(x, y, x+1, y2, self.ground_colour)
                y = y2

    def collision(self, x, y):
        collision = False
        obj = None
        pos = x + self.lead_in
        obj_y = max(self.object_mask[pos], self.ground_line[pos])
        if y >= obj_y:
            collision = True
            obj = self.object_list[pos]
            pyxel.blt(x, y, 0, 16, 0, 16, 16)

        return collision, obj

    def update(self):
        self.ground_line.pop(0)
        self.object_mask.pop(0)
        self.object_list.pop(0)
        self.ground_add()
        self.sprite_add()

    def sprite_add(self):
        # randomly add an object to the object mask
        if self.sprite_lock_out == 0 and randrange(1, 70) == 10:
            sprite_type = randrange(1, 3)
            print(sprite_type)
            sprite_len = 16
            sprite_height = 16
            start = W + self.lead_in
            sprite_top = self.ground_line[start] - sprite_height
            for pos in range(start, start + sprite_len):
                self.object_mask[pos] = sprite_top
                self.object_list[pos] = sprite_type
            self.sprite_lock_out += sprite_len
        elif self.sprite_lock_out > 0:
            self.sprite_lock_out -= 1

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
        self.ground_line.append(self.yx)

        self.object_mask.append(0)
        self.object_list.append(0)

