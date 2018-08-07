# -*- coding: utf-8 -*-
from typing import Callable, List, Dict, Any
from numbers import Real

from common.game import MancalaGame, Result


__all__ = [
    'AIBase',
    'OneEvalFuncAIBase',
    'ChoiceMixin',
]


class AIBase:

    def __init__(self, side: int):
        self.side = side

    @staticmethod
    def iter_pos(g: MancalaGame):
        ini_side = g.side
        stack = [[g, []]]
        while stack:
            g, pos_list = stack.pop()
            for pos in g.pos_candidates():
                gg = g.copy()
                pp = pos_list + [pos]
                nex = gg.move(pos)
                if gg.state is Result.IN_BATTLE:
                    if nex == ini_side:
                        stack.append([gg, pp])
                        continue
                yield gg, tuple(pp)

    def think(self, g: MancalaGame) -> List[int]:
        raise NotImplemented


class OneEvalFuncAIBase(AIBase):

    def __init__(self, side, eval_func: Callable[[int, MancalaGame], int]):
        super().__init__(side)
        self.eval_func = eval_func


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
