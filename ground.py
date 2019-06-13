from config import W, H, TANK, GUN, LAND
from object_helpers import PyxelObjectFixedList
from random import randrange
from shells import Shell
from asteroids import Asteroid
import pyxel
import math


class BaseObject:

    def __init__(self, x, y, game, colour, high_colour):
        self.ground = game.ground
        self.player = game.player
        self.game = game
        self.x = x
        self.y = y - 16
        self.ys = None
        caps = int(H / 1.7)
        self.ys_caps = [caps]
        for i in range(0, 16):
            self.ys_caps.append(caps - randrange(0, 4))
        self.colour = colour
        self.high_colour = high_colour
        self.burning = False

    def get_last_y(self):
        return self.y + 16

    def update(self):
        self.x -= 1

    def draw(self):
        s = self.x
        for i in range(0, 17):
            s2 = s + 1
            if self.ys is not None:
                y = self.ys[i]
            else:
                y = self.y + 17
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
            if self.ys is not None:
                y_ground = self.ys[xd]
            else:
                y_ground = self.y
            if y >= y_ground:
                return True
            else:
                return False
        except IndexError:
            print("indxex error", xd)
            return False

    def burn(self):
        self.burning = True


class Tanks(BaseObject):

    def __init__(self, x, y, game, colour, high_colour):
        super().__init__(x, y, game, colour, high_colour)
        self.name = TANK

    def draw(self):
        if self.burning:
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16)
        super().draw()


class Gun(BaseObject):

    def __init__(self, x, y, game, colour, high_colour):
        super().__init__(x, y, game, colour, high_colour)
        self.name = GUN
        self.fire_period = randrange(90, 240)
        self.time_to_fire = 10

    def draw(self):
        if self.burning:
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16)
        super().draw()

    def update(self):
        super().update()

        self.time_to_fire -= 1
        x_inc = -1

        if self.time_to_fire == 0 and not self.burning:
            y_inc = 0
            if self.player.x + 20 > self.x > 80:
                time_to_hit = abs(self.player.y - self.y)
                x_inc = (self.player.x - self.x) / time_to_hit
                y_inc = -1
            elif self.player.x < self.x:
                y_inc = -1

            if y_inc != 0:
                self.game.shells.insert(Shell(self.game, self.x, self.y, x_inc, y_inc))
            self.time_to_fire = self.fire_period


class Land(BaseObject):

    def __init__(self, x, y1, y2, game, colour, high_colour):
        super().__init__(x, y1, game, colour, high_colour)
        self.name = LAND
        self.ys = [y1]
        for i in range(0, 16):
            y = self.ys[i]
            y_step = (y2 - y) // (16 - i)
            y_vary = abs(y_step)//8
            if y_vary > 0:
                self.ys.append(y + y_step + randrange(-y_vary, y_vary))
            else:
                self.ys.append(y + y_step)
        self.ys.append(y2)

    def get_last_y(self):
        return self.ys[17]


class Ground:

    def __init__(self, game):
        self.y_base = H * 2 // 3
        self.lead_in = 32
        self.ground_objs = None
        self.game = game
        self.ground_colour = 5
        self.high_colour = 7
        self.count = 0
        self.gradient = 0
        self.jitter = 0

    def reset(self):
        x = 0
        y = H
        self.ground_objs = PyxelObjectFixedList(W, self.lead_in, self.add)

        for i, obj in self.ground_objs.all():
            y2 = y - 2
            self.ground_objs.substitute(i, Land(x, self.y_base, self.y_base, self.game,
                                                self.ground_colour, self.high_colour))
            y = y2
            x += 16
        self.count = 0

    def add(self):
        i = self.ground_objs.length
        prev_obj = self.ground_objs.get(i-1)
        y_start = prev_obj.get_last_y()

        if randrange(1, 7) == 5:
            if randrange(1, 3) == 2:
                self.ground_objs.substitute(i, Tanks(W + 32, y_start, self.game, self.ground_colour, self.high_colour))
            else:
                self.ground_objs.substitute(i, Gun(W + 32, y_start, self.game, self.ground_colour, self.high_colour))
            if randrange(1, 4) == 2:
                aster_y_max = H/2 - 20
                aster_y = randrange(10, aster_y_max)
                aster_y_speed = (aster_y_max - aster_y) * (randrange(0, 100)/32000)
                self.game.asteroids.insert(Asteroid(self.game, W+32, aster_y, randrange(-30, -5)/10, aster_y_speed))
        else:
            if self.ground_objs.origin == 0:
                self.jitter = randrange(-5, 6)
            offset = math.cos(pyxel.frame_count/100 - self.jitter * 3) * 20
            offset += math.sin(pyxel.frame_count/20 + self.jitter) * 20
            y_end = self.y_base + randrange(-10, 11) + offset
            if y_end < H//2:
                self.gradient += randrange(-5, 10)
            elif y_end > H - 25:
                self.gradient += randrange(-10, 5)
            y_end += self.gradient
            self.ground_objs.substitute(i, Land(W + 32, y_start, y_end, self.game,
                                                self.ground_colour, self.high_colour))

    def update(self):
        self.ground_objs.update()

    def draw(self):
        self.ground_objs.draw()

    def collision(self, x, y):
        # find ground object with same x position
        x = x - 1
        obj_id = (x + self.ground_objs.pixel_shift) // 16
        obj = self.ground_objs.get(obj_id)
        x_rel = x - obj.x

        if x_rel > 17:
            obj = self.ground_objs.get(obj_id + 1)
            print('greater')
        elif x_rel < 0:
            print('lesser', x_rel)
            obj = self.ground_objs.get(obj_id - 1)

        collision = obj.collision(x, y)
        return collision, obj
