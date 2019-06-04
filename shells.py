from random import randint as rand, random as randf, randrange
from object_pool import ObjectPool
import math
import pyxel


class Guns:

    def __init__(self, game):
        self.game = game
        self.ground = game.ground
        self.guns = None

    def reset(self):
        self.guns = ObjectPool()

    def create_gun(self, pos, x):
        self.guns.insert(Gun(self.game, pos+1, x))

    def update(self):
        for i, gun in self.guns.each():
            gun.update()
            if gun.off_screen:
                self.guns.kill(i)

    def draw(self):
        for _, gun in self.guns.each():
            gun.draw()


class Gun:
    def __init__(self, game, pos, x):
        self.x = x
        self.ground = game.ground
        self.player = game.player
        self.game = game
        self.pos = pos
        self.off_screen = False
        self.fire_period = randrange(90, 240)
        self.time_to_fire = 10
        self.gun_shells = ObjectPool()

    def update(self):
        self.pos -= 1
        self.x -= 1
        self.time_to_fire -= 1
        x_inc = -1

        if self.pos < 8:
            self.off_screen = True
        elif self.time_to_fire == 0:
            y = self.ground.object_mask[self.pos]
            y_inc = 0
            if self.player.player_x + 20 > self.x > 80:
                time_to_hit = abs(self.player.player_y - y)
                x_inc = (self.player.player_x - self.x)/time_to_hit
                y_inc = -1
            elif self.player.player_x < self.x:
                y_inc = -1

            if y_inc != 0:
                self.game.shells.insert(Shell(self.game, self.x, y, x_inc, y_inc))
            self.time_to_fire = self.fire_period

    def draw(self):
        pass


class Shell:

    def __init__(self, game, x, y, x_inc=-0.5, y_inc=-1):
        self.x = x
        self.y = y
        self.game = game
        self.player = game.player
        self.guns = game.guns
        self.exploded = False
        self.die = False
        self.x_increment = x_inc
        self.y_increment = y_inc

    def update(self):
        self.x += self.x_increment
        self.y += self.y_increment

        if self.player.player_x <= self.x <= self.player.player_x + 16 and \
                self.player.player_y <= self.y <= self.player.player_y + 10:
            # take one life
            self.game.explosions.insert(ShellHitExplosion(self.x, self.y))
            self.guns.reset()
            self.die = True
            self.player.score.player_hit()

        if self.y < 1 or self.x < 0:
            self.die = True

    def draw(self):
        pyxel.rect(self.x-1, self.y-2, self.x+1, self.y+2, 8)


class ShellHitExplosion:

    def __init__(self, x, y):
        self.particles = ObjectPool()
        self.x = x
        self.y = y
        self.die = False
        self.time_to_live = 15

    def update(self):
        # Update existing particles.
        self.time_to_live -= 1
        if self.time_to_live < 0:
            self.die = True
        for i, particle in self.particles.each():
            particle.update()
            if particle.age >= particle.life:
                self.particles.kill(i)

        # Create new particles.
        for _ in range(3):
            angle = randf() * math.tau
            speed = randf() * 3
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
        for _, particle in self.particles.each():
            particle.draw()


class Particle:
    """
    Simple dynamic object with position and velocity.
    Life is how long (in frames) the particle should live for.
    Age is how old (in frames) the particle is.
    """
    def __init__(self, x, y, vx, vy, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.age = 0

    def update(self):
        """
        This function defines the dynamics of the particle.
        In here you could simulate gravity, or reverse it for a fire or smoke effect.
        """
        self.x += self.vx  # Move based on velocity.
        self.y += self.vy
        self.vx *= 0.99  # X velocity slowly goes to zero over time.
        self.vy += 0.2  # Increase Y velocity to simulate gravity.

        if self.age < self.life:
            self.age += 1

    def draw(self):
        """
        You can draw anything in here. I'm using circles, but particles can be sprites, text, et cetera.
        """
        colour = 7 - int(3 * self.age / self.life)  # Pick white/grey/dark-grey based on age.
        pyxel.circ(self.x, self.y, 1, colour)


class ParticleExample:
    def __init__(self):
        pyxel.init(128, 128)

        self.particles = ObjectPool()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        # Update existing particles.
        for i, particle in self.particles.each():
            particle.update()
            if particle.age >= particle.life:
                self.particles.kill(i)

        # Create new particles.
        for _ in range(3):
            angle = randf() * math.tau
            speed = randf() * 3
            self.particles.insert(
                Particle(
                    64,
                    32,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    rand(10, 30),
                )
            )

    def draw(self):
        pyxel.cls(0)
        for _, particle in self.particles.each():
            particle.draw()
