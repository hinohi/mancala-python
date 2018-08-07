# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result
from ai.base import AIBase, OneEvalFuncAIBase, ChoiceMixin


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

    def think(self, g: MancalaGame):
        can = []
        for pos in g.pos_candidates():
            gg = g.copy()
            gg.move(pos)
            can.append([pos, 0, 0, 0])
            for _ in range(self.num):
                res = self._random(gg.copy())
                can[-1][self._offset[res]] += 1
        return [self.choice({c[0]: (c[1] - c[2]) / self.num + 1.0 for c in can})[1]]


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
