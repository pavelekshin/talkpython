import random
import itertools


NAMES = [
    "arnold schwarzenegger",
    "alec baldwin",
    "bob belderbos",
    "julian sequeira",
    "sandra bullock",
    "keanu reeves",
    "julbob pybites",
    "bob belderbos",
    "julian sequeira",
    "al pacino",
    "brad pitt",
    "matt damon",
    "brad pitt",
]


names = [name.title() for name in NAMES]


def gen_pairs(names=names):
    first_names = [name.split()[0] for name in names]
    while True:
        first, second = None, None
        while first == second:
            first, second = random.sample(first_names, 2)
        yield f"{first} pairs with {second}"

pairs = gen_pairs()
#for _ in range(10):
#    print(next(pairs))
first_ten = itertools.islice(pairs,10)
print(list(first_ten))
