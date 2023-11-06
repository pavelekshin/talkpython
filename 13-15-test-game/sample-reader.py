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
            # can_defeat = row[k].strip().lower() == "win"
            # print(" * {} will defeat {}? {}".format(name, k, can_defeat))
    return d


d = read_rolls_csv()
print(d)
print(d["Rock"])
