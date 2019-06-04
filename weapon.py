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
        self.y = self.y + 3
        self.impact, obj = self.ground.collision(self.x + 12, self.y + 8)

        if self.impact:
            # obj 10 = tank, 11 = gun
            if obj == 11:
                self.score.tanks_hit()
            elif obj == 10:
                self.score.guns_hit()
                self.game.guns.reset()
            self.die = True
            pyxel.play(0, 1)
