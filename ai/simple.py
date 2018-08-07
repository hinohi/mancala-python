# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result
from ai.base import AIBase, OneEvalFuncAIBase


class RandomAI(AIBase):

    def think(self, g: MancalaGame):
        import random
        return random.choice(g.pos_candidates())


class OneTurnGreedyAI(OneEvalFuncAIBase):

    def __init__(self, side, eval_func):
        super().__init__(side, eval_func)

    def think(self, g: MancalaGame) -> int:
        from random import choice

        best_pos = []
        best_point = float('-inf')
        stack = [[g, []]]
        while stack:
            g, pos_list = stack.pop()
            for pos in g.pos_candidates():
                gg = g.copy()
                pp = pos_list + [pos]
                nex = gg.move(pos)
                if gg.state is Result.IN_BATTLE:
                    if nex == self.side:
                        stack.append([gg, pp])
                        continue
                point = self.eval_func(self.side, gg)
                if point > best_point:
                    best_point = point
                    best_pos = [pp]
                elif point == best_point:
                    best_pos.append(pp)
        return choice(best_pos)[0]
