# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result, MancalaGameError
from ai.base import AIBase


class BattleManager:

    def __init__(self, pit: int, stone: int,
                 ai1: AIBase, ai2: AIBase):
        self.pit = pit
        self.stone = stone
        self.ai_list = [ai1, ai2]
        self.game = MancalaGame(self.pit, self.stone)

    def battle(self, debug=False):
        if debug:
            print(self.game.purity_dumps())
        while self.game.state is Result.IN_BATTLE:
            this_side = self.game.side
            assert this_side in [0, 1]
            ai = self.ai_list[this_side]
            pos = ai.think(self.game.copy())
            try:
                self.game.move(pos)
            except MancalaGameError as e:
                print(ai, e)
                if this_side == 0:
                    return Result.WIN_EPI,
                else:
                    return Result.WIN_PRE
            if debug:
                print(f'next: {self.game.side}')
                print(f'pos: {pos}')
                print(self.game.purity_dumps())
        print(self.game.state)
        return self.game.state


def factory(name, side):
    from ai.simple import RandomAI, OneTurnAI
    from ai.human import HumanAI
    from ai.eval_functions import evf_point_diff

    if name == 'human':
        return HumanAI(side)
    if name == 'random':
        return RandomAI(side)
    if name == 'one':
        return OneTurnAI(side, evf_point_diff)
    raise ValueError(f'unknown: {name}')


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('ai1')
    p.add_argument('ai2')
    p.add_argument('--pit', type=int, default=6)
    p.add_argument('--stone', type=int, default=4)
    p.add_argument('--no-debug', action='store_true')
    args = p.parse_args()

    bm = BattleManager(args.pit, args.stone,
                       factory(args.ai1, 0), factory(args.ai2, 1))
    bm.battle(debug=not args.no_debug)


if __name__ == '__main__':
    main()
