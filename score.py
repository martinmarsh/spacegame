import os
import csv
import pyxel
from pathlib import Path

TANKS_HIT = 400
GUNS_HIT = 200


class Score:

    def __init__(self, game):
        self.total = 0
        self.player_count = 3
        self.guns_num_hit = 0
        self.tanks_num_hit = 0
        self.lives_position = 100
        self.game = game
        self.results = None
        self.ordered_names = []

    def reset(self):
        self.total = 0
        self.player_count = 3
        self.guns_num_hit = 0
        self.tanks_num_hit = 0
        self.results = None

    def update(self):
        pass

    def draw(self):
        total_score = f"Score: {self.total}"
        pyxel.text(3, 3, total_score, 7)
        pyxel.text(70, 3, "Lives:", 7)
        pyxel.text(200, 3, self.game.player.name, 7)
        for count in range(self.player_count):
            pyxel.circ(self.lives_position + (count * 10), 5, 2, 8)
        if self.player_count <= 0:
            pyxel.text(100, 3, "Game over", 8)
            self.save()
            self.game.STATE = "DEAD";

    def player_hit(self):
        self.player_count = self.player_count - 1

    def guns_hit(self):
        self.total = self.total + GUNS_HIT

    def tanks_hit(self):
        self.total = self.total + TANKS_HIT

    def list_order(self):
        if self.results is None:
            self.read()
        self._make_ordered_names()

    def _make_ordered_names(self):
        self.ordered_names = []
        count = 0
        for key, value in sorted(self.results.items(), reverse=True, key=lambda item: item[1]):
            self.ordered_names.append(key)
            count += 1
            if count > 7:
                break

    def read(self):
        file = "/scores.csv"
        path = os.getcwd() + file
        file_to_open = Path(path)
        print(file_to_open)
        self.results = {}
        if file_to_open.is_file():
            with open(file_to_open) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.results[row[0]] = int(row[1])
        return file_to_open

    def save(self):
        # Write scores to file.
        file_to_open = self.read()

        if self.results.get(self.game.player.name, None) is not None:
            self.results[self.game.player.name] = max(self.total, int(self.results[self.game.player.name]))
        else:
            self.results[self.game.player.name] = self.total
            print(self.results)

        self._make_ordered_names()
        print(self.ordered_names)
        with open(file_to_open, 'w') as csvfile:
            my_writer = csv.writer(csvfile)
            for name in self.ordered_names:
                my_writer.writerow([name, self.results[name]])
