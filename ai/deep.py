# -*- coding: utf-8 -*-
from typing import Dict, Any
from numbers import Real

from common.game import MancalaGame, Result
from ai.base import AIBase, OneEvalFuncAIBase


class ChoiceMixin:

    choice_typ = 'best'

    @staticmethod
    def best_choice(candidates: Dict[Any, Real]) -> (Real, Any):
        from random import choice

        best = float('-inf')
        ret = []
        for k, v in candidates.items():
            if v > best:
                best = v
                ret = [k]
            elif v == best:
                ret.append(k)
        return best, choice(ret)

    @staticmethod
    def weight_choice(candidates: Dict[Any, Real]) -> (Real, Any):
        from random import random, choice

        m = -min(candidates.values())
        if m < 0.0:
            m = 0.0
        p = (sum(candidates.values()) + m * len(candidates)) * random()
        s = 0.0
        for k, v in candidates.items():
            s += v + m
            if s >= p:
                return v, k
        k = choice(list(candidates))
        return candidates[k], k

    def choice(self, candidates: Dict[Any, Real]) -> (Real, Any):
        return getattr(self, self.choice_typ + '_choice')(candidates)


class SimpleMCMCAI(AIBase, ChoiceMixin):

    def __init__(self, side, num: int, choice_typ: str):
        super().__init__(side)
        self.num = num
        self.choice_typ = choice_typ
        self._offset = {
            Result.WIN_PRE: 1 if side == 0 else 2,
            Result.WIN_EPI: 2 if side == 0 else 1,
            Result.DRAW: 3,
        }

    @staticmethod
    def _random(g: MancalaGame) -> Result:
        from random import choice

        while g.state is Result.IN_BATTLE:
            g.move(choice(g.pos_candidates()))
        return g.state

    def think(self, g: MancalaGame) -> int:
        can = []
        for pos in g.pos_candidates():
            gg = g.copy()
            gg.move(pos)
            can.append([pos, 0, 0, 0])
            for _ in range(self.num):
                res = self._random(gg.copy())
                can[-1][self._offset[res]] += 1
        return self.choice({c[0]: (c[1] - c[2]) / self.num + 1.0 for c in can})[1]


class DepthSearchAI(OneEvalFuncAIBase, ChoiceMixin):

    def __init__(self, side, eval_func, depth: int, choice_typ: str):
        super().__init__(side, eval_func)
        self.depth = depth
        self.choice_typ = choice_typ

    def _search(self, side: int, g: MancalaGame, depth: int):
        ret = []
        stack = [[g, []]]
        while stack:
            g, pos_list = stack.pop()
            for pos in g.pos_candidates():
                gg = g.copy()
                pp = pos_list + [pos]
                nex = gg.move(pos)
                if gg.state is Result.IN_BATTLE:
                    if nex == side:
                        stack.append([gg, pp])
                        continue
                    elif depth > 0:
                        point, _ = self._search(1 - side, gg, depth - 1)
                        ret.append([point * -1, pp])
                        continue
                point = self.eval_func(side, gg)
                ret.append([point, pp])
        return self.choice({tuple(pp): p for p, pp in ret})

    def think(self, g: MancalaGame):
        return self._search(self.side, g, self.depth)[1][0]
