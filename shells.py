from random import randint as rand, random as randf
import math
import pyxel


class Shells:

    def __init__(self, game):
        self.game = game
        self.shells = ObjectPool()

    def reset(self):

        pass

    def update(self):
        pass

    def draw(self):
        pass


class Shell:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= 4

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8)



class ObjectPool:
    """
    ObjectPool is a data structure that grows to fit a set of objects.
    """
    class Object:
        """
        Object is a simple wrapper around a value.
        """
        def __init__(self, value):
            self.value = value
            self.alive = True

    def __init__(self):
        self.objects = []

    def insert(self, value):
        """
        Wrap the given value and find a place for it in the list, append if necessary.
        """
        new = self.Object(value)
        for i, obj in enumerate(self.objects):
            if obj.alive is False:
                self.objects[i] = new
                break
        else:
            self.objects.append(new)

    def each(self):
        """
        Iterate over each object, ignoring inactive ones.
        Yields the object's ID and the object itself.
        """
        for i, obj in enumerate(self.objects):
            if obj.alive:
                yield i, obj.value

    def kill(self, i):
        """
        Deactivate an object with the given ID.
        """
        self.objects[i].alive = False


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


