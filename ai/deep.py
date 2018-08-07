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
