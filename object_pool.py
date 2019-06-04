

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

    def update(self):
        for i, item in self.each():
            item.update()
            if item.die:
                self.kill(i)

    def draw(self):
        for _, item in self.each():
            item.draw()


