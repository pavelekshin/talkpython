import csv
from enum import Enum

from models.roll import Roll

_winner_lookup = {}


class Decision(Enum):
    tie = 1
    win = 2
    lose = 3


def decide(roll1: Roll, roll2: Roll) -> Decision:
    _build_decisions()

    if roll1.name == roll2.name:
        return Decision.tie

    roll1_wins = roll2.name in _winner_lookup[roll1.name]

    if roll1_wins:
        return Decision.win
    else:
        return Decision.lose


def _build_decisions():
    if _winner_lookup:
        return

    with open("battle-table.csv") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            _build_roll(row)


def _build_roll(row: dict):
    row = dict(row)
    name = row["Attacker"]

    del row["Attacker"]
    del row[name]

    _winner_lookup[name] = set()
    for k in row.keys():
        can_defeat = row[k].strip().lower() == "win"
        if can_defeat:
            _winner_lookup[name].add(k)
