import pyxel


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

    def reset(self):
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
        try:
            self.objects[i].alive = False
        except IndexError:                   # Need exception here as Objects may have been destroyed by reset
            pass


class PyxelObjectPool(ObjectPool):
    """ This class makes it easier to use Pools of objects in Pyxel. Simply insert an object
      into an instantiated Pool and let objects update and draw methods do the positioning, collision, rendering and to
      end its life by setting die.
      There is no need to refer to the Pool or iterate over objects in the Pool. Simply call the pools
      update and draw methods from the highest level object you need the pool to exist for.

      This class extends base object pool by having methods to process draw and update
        Classes inserted into a pool instantiated from this case must have:
            1) a property "self.die" set to true (false to commit suicide and be removed from the pool)
            2) Draw and Update methods

    """

    def __init__(self):
        super().__init__()

    def update(self):
        for i, item in self.each():
            item.update()
            if item.die:
                self.kill(i)

    def draw(self):
        for _, item in self.each():
            item.draw()


class Particle:
    """
    Simple dynamic object with position and velocity.
    Life is how long (in frames) the particle should live for.
    Age is how old (in frames) the particle is.
    """
    def __init__(self, x, y, vx, vy, life, x_vel=0.99, y_vel=0.2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.life = life
        self.age = 0

    def update(self):
        """
        This function defines the dynamics of the particle.
        In here you could simulate gravity, or reverse it for a fire or smoke effect.
        """
        self.x += self.vx  # Move based on velocity.
        self.y += self.vy
        self.vx *= self.x_vel  # X velocity slowly goes to zero over time.
        self.vy += self.y_vel  # Increase Y velocity to simulate gravity.

        if self.age < self.life:
            self.age += 1

    def draw(self):
        """
        You can draw anything in here. I'm using circles, but particles can be sprites, text, et cetera.
        """
        colour = 7 - int(3 * self.age / self.life)  # Pick white/grey/dark-grey based on age.
        pyxel.circ(self.x, self.y, 1, colour)
