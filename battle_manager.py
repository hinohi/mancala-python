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
            pos_list = ai.think(self.game.copy())
            assert isinstance(pos_list, (list, tuple)), pos_list
            assert len(pos_list) >= 1, pos_list
            try:
                for pos in pos_list:
                    assert self.game.side == this_side
                    self.game.move(pos)
                    if debug:
                        print()
                        print(f'next: {self.game.side}')
                        print(f'pos: {pos}')
                        print(self.game.purity_dumps())
            except MancalaGameError as e:
                print(ai, e)
                if this_side == 0:
                    return Result.WIN_EPI,
                else:
                    return Result.WIN_PRE
        p1, p2 = self.game.get_points()
        print(self.game.state, p1, p2)
        return self.game.state


def factory(name, side):
    import re
    from ai.simple import RandomAI, OneTurnGreedyAI, HumanAI
    from ai.deep import SimpleMCMCAI, DepthSearchAI
    from ai.eval_functions import evf_point_diff

    if name == 'human':
        return HumanAI(side)
    if name == 'random':
        return RandomAI(side)
    if name == 'one':
        return OneTurnGreedyAI(side, evf_point_diff)
    m = re.match(r'mcmc(\d)_(.+)', name)
    if m:
        num = int(m.group(1))
        typ = m.group(2)
        return SimpleMCMCAI(side, 10 ** num, typ)
    m = re.match(r'depth(\d)_(.+)', name)
    if m:
        depth = int(m.group(1))
        typ = m.group(2)
        ai = DepthSearchAI(side, evf_point_diff, depth)
        ai.choice_typ = typ
        return ai
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
