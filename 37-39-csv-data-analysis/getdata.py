import os
import csv
import collections
from typing import List

data = []

Record = collections.namedtuple(
    "Record",
    (
        "country",
        "beer_servings",
        "spirit_servings",
        "wine_servings",
        "total_litres_of_pure_alcohol",
    ),
)


def init():
    for row in read_file():
        data.append(parse_row(row))


def read_file():
    if data:
        return
    dir_name = os.path.dirname(__file__)
    filepath = os.path.join(dir_name, "data", "drinks.csv")
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data.clear()
        for row in reader:
            yield row


def parse_row(row):
    row["beer_servings"] = int(row["beer_servings"])
    row["spirit_servings"] = int(row["spirit_servings"])
    row["wine_servings"] = int(row["wine_servings"])
    row["total_litres_of_pure_alcohol"] = float(row["total_litres_of_pure_alcohol"])
    record = Record(**row)
    return record


def beer_servings() -> List[Record]:
    return sorted(data, key=lambda r: -r.beer_servings)


def wine_servings() -> List[Record]:
    return sorted(data, key=lambda r: -r.wine_servings)


def spirit_servings() -> List[Record]:
    return [
        r
        for r in sorted(data, key=lambda r: r.spirit_servings)
        if r.spirit_servings != 0
    ]


def total_litres() -> List[Record]:
    return [
        r
        for r in sorted(data, key=lambda r: r.total_litres_of_pure_alcohol)
        if r.total_litres_of_pure_alcohol != 0
    ]
