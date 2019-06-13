from random import randint as rand, random as randf, randrange
from object_helpers import PyxelObjectPool, Particle
import math
import pyxel


class Asteroid:

    def __init__(self, game, x, y, x_inc=-0.5, y_inc=-1):
        self.x = x
        self.y = y
        self.game = game
        self.player = game.player
        self.exploded = False
        self.die = False
        self.x_increment = x_inc
        self.y_increment = y_inc

    def update(self):
        self.x += self.x_increment
        self.y += self.y_increment

        if self.player.x <= self.x <= self.player.x + 16 and self.player.y <= self.y <= self.player.y + 10:
            # take one life
            pyxel.play(0, 1)
            self.game.explosions.insert(AsteroidHitExplosion(self.x, self.y))
            self.game.shells.reset()
            self.die = True
            self.player.score.player_hit()

        if self.y < 1 or self.x < 0:
            self.die = True

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 16, 16, 16, 0)


class AsteroidHitExplosion:

    def __init__(self, x, y):
        self.particles = PyxelObjectPool()
        self.x = x
        self.y = y
        self.die = False
        self.time_to_live = 20

    def update(self):
        # Update existing particles.
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
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    rand(10, 30),

                )
            )

    def draw(self):
        self.particles.draw()
