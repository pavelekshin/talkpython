from actors import Player, Rolls, game_objects
import random


GAME_OBJECTS = game_objects()


def print_header():
    print("This is game")


def get_players_name():
    return input("Enter your name: ")


def build_the_rolls(go):
    return [Rolls(name) for name in go.keys()]


def main():
    print_header()

    rolls = build_the_rolls(GAME_OBJECTS)

    name = get_players_name()

    player1 = Player(name)
    player2 = Player("computer")

    game_loop(player1, player2, rolls)


def game_loop(player1, player2, rolls):
    count = 0
    while count < 3:
        p2_roll = random.choice(rolls)

        cmd = input("Choice a roll from a list {} : ".format(list(GAME_OBJECTS.keys())))
        if cmd:
            p1_roll = Rolls(cmd)

        if p1_roll.can_defeat(p2_roll) is True:
            print("{} has beat the {}!".format(p1_roll.name, p2_roll.name))
            print("{} has won this round!".format(player1.name))
            player1.score += 1
        elif p1_roll.can_defeat(p2_roll) is False:
            print("{} has defeat the {}!".format(p1_roll.name, p2_roll.name))
            print("{} has won this round!".format(player2.name))
            player2.score += 1
        elif p1_roll.can_defeat(p2_roll) is None:
            print("{} has same as {}, tie!".format(p1_roll.name, p2_roll.name))
        # display winner for this round
        count += 1

    # Compute who won
    if player1.score > player2.score:
        print("{} has won this game with {} score!".format(player1.name, player1.score))
    elif player2.score > player1.score:
        print("{} has won this game with {} score!".format(player2.name, player2.score))
    else:
        print("Tie!")


if __name__ == "__main__":
    main()
