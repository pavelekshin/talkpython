from time import sleep
import itertools
import random

def rd():
    return random.randint(3,7)

def main():
    traffic = random.random()
    lights = "red amber green".split()
    if traffic > 0.5:
        signal = reversed(lights)
    signal = itertools.cycle(lights)
    for i in signal:
        if i == "red":
            print(i)
            sleep(rd())
        if i == "amber":
            print(i)
            sleep(0.5)
        if i == "green":
            print(i)
            sleep(rd())

if __name__ == "__main__":
    main()
