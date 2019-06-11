from object_helpers import PyxelObjectPool, Particle
from random import randint as rand, random as randf
import math
import pyxel


class Bomb:

    def __init__(self, game, x, y):
        self.game = game
        self.ground = game.ground
        self.score = game.score
        self.die = False
        self.x = x
        self.width = self.x + 3
        self.height = 6
        self.y = y
        self.colour = 3
        self.impact = None
        pyxel.play(0, 0)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8)

    def update(self):
        self.y += 3
        self.impact, obj = self.ground.collision(self.x-4, self.y-4)

        if self.impact:
            # obj 10 = tank, 11 = gun
            if obj == 11:
                self.score.tanks_hit()
            elif obj == 10:
                self.score.guns_hit()
                self.game.guns.reset()
            self.die = True
            self.game.explosions.insert(BombExplosion(self.x-4, self.y-4))
            pyxel.play(0, 1)


class BombExplosion:

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
