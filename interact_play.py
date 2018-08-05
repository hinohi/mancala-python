# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result, MancalaGameError


def interact():

    def input_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                pass

    pit = input_int('pit: ')
    stone = input_int('stone: ')
    g = MancalaGame(pit, stone)
    while g.state is Result.IN_BATTLE:
        print(g.purity_dumps())
        print(f'next: {g.side}')
        while True:
            pos = input_int('pos: ')
            try:
                g.move(pos)
                break
            except MancalaGameError as e:
                print(e)
        print()
    print(g.state)


def main():
    interact()


if __name__ == '__main__':
    main()
