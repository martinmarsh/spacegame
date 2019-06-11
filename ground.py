from config import W, H, TANK, GUN, LAND
from object_helpers import PyxelObjectFixedList
from random import randrange
import pyxel


class Bl

class Tanks:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = TANK

    def get_last_y(self):
        return self.y

    def update(self):
        self.x -= 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16)
        pyxel.blt(x, y, 0, 48, 0, 16, 16)

    def collision(self, x, y):
        return False


class Land:

    def __init__(self, x, y1, y2, colour, high_colour):
        self.name = LAND
        self.x = x
        self.ys = [y1]
        caps = int(H/1.7)
        self.ys_caps = [caps]
        for i in range(0, 16):
            y = self.ys[i]
            y_step = (y2 - y) // (16 - i)
            y_vary = abs(y_step)//8
            if y_vary > 0:
                self.ys.append(y + y_step + randrange(-y_vary, y_vary))
            else:
                self.ys.append(y + y_step)

        for i in range(0, 16):
            self.ys_caps.append(caps-randrange(0, 4))

        self.ys.append(y2)
        self.colour = colour
        self.high_colour = high_colour

    def get_last_y(self):
        return self.ys[17]

    def update(self):
        self.x -= 1

    def draw(self):
        s = self.x
        for i in range(0, 17):
            s2 = s + 1
            y = self.ys[i]
            cap = self.ys_caps[i]
            if y < cap:
                pyxel.rect(s, y, s2, cap, self.high_colour)
                pyxel.rect(s, cap, s2, H, self.colour)
            else:
                pyxel.rect(s, y, s2, H, self.colour)
            s = s2

    def collision(self, x, y):
        xd = int(x - self.x)
        try:
            y_ground = self.ys[xd]
            if y >= y_ground:
                return True
            else:
                return False
        except IndexError:
            print("indxex error", xd)
            return False


class Ground:

    def __init__(self, game):
        self.y_base = H * 2 // 3
        self.ground_objs = PyxelObjectFixedList(W, 32, self.add)
        self.game = game
        self.ground_colour = 4
        self.high_colour = 7
        self.count = 0
        self.gradient = 0

    def reset(self):
        x = -32
        y = H
        for i, obj in self.ground_objs.all():
            print(i, x)
            y2 = y - 2
            self.ground_objs.substitute(i, Land(x, self.y_base, self.y_base, self.ground_colour, self.high_colour))
            y = y2
            x += 16
        self.count = 0

    def add(self):
        i = self.ground_objs.length
        prev_obj = self.ground_objs.get(i-1)
        y_start = prev_obj.get_last_y()

        if randrange(1, 10) == 1:
            self.ground_objs.substitute(i, Tanks(W + 32, y_start))

        else:
            y_end = self.y_base + randrange(-30, 31)
            if y_end < H//2:
                self.gradient += randrange(-5, 10)
            elif y_end > H - 25:
                self.gradient += randrange(10, 5)
            y_end += self.gradient
            self.ground_objs.substitute(i, Land(W + 32, y_start, y_end, self.ground_colour, self.high_colour))

    def update(self):
        self.ground_objs.update()

    def draw(self):
        self.ground_objs.draw()

    def collision(self, x, y):
        # find ground object with same x position
        x = x - 4
        obj_id = (x + self.ground_objs.pixel_lead_in) // 16 + 3
        obj = self.ground_objs.get(obj_id)
        x_rel = x - obj.x

        if x_rel > 17:
            obj = self.ground_objs.get(obj_id + 1)
            print('greater')
        elif x_rel < 0:
            obj = self.ground_objs.get(obj_id - 1)

        collision = obj.collision(x, y)
        return collision, obj
