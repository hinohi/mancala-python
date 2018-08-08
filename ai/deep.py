# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result
from ai.base import OneEvalFuncAIBase, ChoiceMixin


class DepthSearchAI(OneEvalFuncAIBase, ChoiceMixin):

    def __init__(self, side, eval_func, depth: int):
        super().__init__(side, eval_func)
        self.depth = depth

    def _search(self, side: int, g: MancalaGame, depth: int):
        ret = {}
        for gg, pp in self.iter_pos(g):
            if depth > 0 and gg.state is Result.IN_BATTLE:
                point, _ = self._search(1 - side, gg, depth - 1)
                ret[pp] = point * -1
            else:
                point = self.eval_func(side, gg)
                ret[pp] = point
        return self.choice(ret)

    def think(self, g: MancalaGame):
        return self._search(self.side, g, self.depth)[1]


class KDepthSearchAI(OneEvalFuncAIBase, ChoiceMixin):

    def __init__(self, side, eval_func, depth: int, width: int):
        super().__init__(side, eval_func)
        self.depth = depth
        self.width = width

    def _search(self, side: int, g: MancalaGame, depth: int):
        from random import shuffle

        can = [[self.eval_func(side, gg), pp, gg] for gg, pp in self.iter_pos(g)]
        if depth > 0:
            shuffle(can)
            can.sort(key=lambda x: x[0], reverse=True)
            can = can[:self.width]
            for c in can:
                if c[2].state is Result.IN_BATTLE:
                    point, _ = self._search(1 - side, c[2], depth - 1)
                    c[0] = point * -1
        return self.choice({pp: point for point, pp, _ in can})

    def think(self, g: MancalaGame):
        return self._search(self.side, g, self.depth)[1]
