import random
import csv
from collections import defaultdict


def read_rolls_csv():
    battle_list = []
    with open("battle-table.csv") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            battle_list.append(row)
    return read_rolls(battle_list)


def read_rolls(rows: list):
    d = defaultdict(dict)
    for row in rows:
        name = row["Attacker"]
        del row["Attacker"]
        del row[name]

        for k in row.keys():
            can_defeat = row[k].strip().lower()
            if can_defeat == "win":
                d[name].setdefault("win", []).append(k)
            elif can_defeat == "lose":
                d[name].setdefault("lose", []).append(k)
    return d


def game_objects():
    return read_rolls_csv()


GAME_OBJECTS = game_objects()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class Rolls:
    def __init__(self, name):
        _game_objects = GAME_OBJECTS
        if name in _game_objects.keys():
            self.name = name
            self.defeated = self._defeated(self, _game_objects)
            self.defeat = self._defeat(self, _game_objects)
        else:
            raise ValueError("name is not game object")

    def _defeated(self, name, game):
        if self.name in game.keys():
            return game[self.name]["win"]

    def _defeat(self, name, game):
        if self.name in game.keys():
            return game[self.name]["lose"]

    def can_defeat(self, rolls):
        if self.name in rolls.defeat:
            return True
        elif self.name in rolls.defeated:
            return False
        elif self.name == rolls.name:
            return None
