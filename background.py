from config import W, H
from object_helpers import PyxelObjectPool, Particle
from random import randrange, randint as rand, random as randf
import math
import pyxel


class Ground:

    def __init__(self, game):
        self.lead_in = self.object_list = self.object_mask = self.ground_line = None
        self.sprite_lock_out = self.rate = None
        self.yx = self.yo = None
        self.y_max = self.y_min = self.y_range = self.y_base = None
        self.ground_colour = None
        self.gun_create_standoff = None
        self.game = game

    def reset(self):
        self.ground_line = []
        self.object_mask = []
        self.object_list = []
        self.gun_create_standoff = 0
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
        end = W + self.lead_in
        pos = 0
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
                if obj == 1:
                    pyxel.blt(x, y, 0, 16, 0, 16, 16)
                elif obj == 10:
                    pyxel.blt(x, y, 0, 0, 16, 16, 16)
                elif obj == 11:
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
        x = int(x)
        pos = x + self.lead_in
        obj_y = int(max(self.object_mask[pos], self.ground_line[pos]))
        y = int(y)

        if y >= obj_y - 8:
            collision = True
            obj = self.object_list[pos]
            self.game.explosions.insert(GroundExplosion(x, y))
            if obj > 9:
                # find start of object to replace with explosion
                while self.object_list[pos-1] == obj:
                    pos -= 1
                for pos in range(pos, pos + 16):
                    self.object_list[pos] = 1   # type 1 = explosion

        return collision, obj

    def update(self):
        self.ground_line.pop(0)
        self.object_mask.pop(0)
        self.object_list.pop(0)
        self.ground_add()
        self.sprite_add()
        pos = W + self.lead_in
        if self.object_list[pos] == 10 and self.gun_create_standoff <= 0:
            self.game.guns.create_gun(pos, W + 4)
            self.game.guns.create_gun(pos, W + 14)
            self.gun_create_standoff = 17
        else:
            self.gun_create_standoff -= 1

    def sprite_add(self):
        # randomly add an object to the object mask
        if self.sprite_lock_out == 0 and randrange(1, 70) == 10:
            # reserve 0 to 9,  10 = tanks, 11 = guns
            sprite_type = randrange(10, 12)
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


class GroundExplosion:

    def __init__(self, x, y):
        self.particles = PyxelObjectPool()
        self.x = x
        self.y = y
        self.die = False
        self.time_to_live = 30

    def update(self):
        # Update existing particles.
        self.x -= 1
        self.time_to_live -= 1
        if self.time_to_live < 0:
            self.die = True
        self.particles.update()

        # Create new particles.
        for _ in range(3):
            angle = randf() * math.tau
            speed = randf() * 4
            self.particles.insert(
                Particle(
                    self.x,
                    self.y,
                    math.cos(angle) * speed - 1,
                    math.sin(angle) * speed,
                    rand(5, 20),
                    y_vel=-0.2,
                    x_vel=0.99

                )
            )

    def draw(self):
        self.particles.draw()
