import pyxel

TANKS_HIT = 400
GUNS_HIT = 200


class Score:

    def __init__(self, game):
        self.total = 0
        self.player_count = 3
        self.guns_hit = 0
        self.tanks_hit = 0
        self.lives_position = 100
        self.game = game

    def reset(self):
        self.total = 0
        self.player_count = 3
        self.guns_hit = 0
        self.tanks_hit = 0

    def update(self):
        pass

    def draw(self):
        total_score = f"Score: {self.total}"
        pyxel.text(3, 3, total_score, 7)
        pyxel.text(70, 3, "Lives:", 7)
        for count in range(self.player_count):
            pyxel.circ(self.lives_position + (count * 10), 5, 2, 8)

        if self.player_count == 0:
            pyxel.text(100, 3, "Game over", 8)
            self.game.STATE = "DEAD";

    def player_hit(self):
        self.player_count = self.player_count - 1

    def guns_hit(self):
        self.total = self.total + GUNS_HIT

    def tanks_hit(self):
        self.total = self.total + TANKS_HIT
