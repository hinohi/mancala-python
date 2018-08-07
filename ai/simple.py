# -*- coding: utf-8 -*-
from common.game import MancalaGame, MancalaGameError
from ai.base import AIBase, OneEvalFuncAIBase, ChoiceMixin


class RandomAI(AIBase):

    def think(self, g: MancalaGame):
        from random import choice
        return [choice(g.pos_candidates())]


class ContRandom(AIBase):

    def think(self, g: MancalaGame):
        from random import choice
        return choice(list(self.iter_pos(g)))


class OneTurnGreedyAI(OneEvalFuncAIBase, ChoiceMixin):

    def think(self, g: MancalaGame):
        can = {pp: self.eval_func(self.side, gg)
               for gg, pp in self.iter_pos(g)}
        return self.choice(can)[1]


class HumanAI(AIBase):

    @staticmethod
    def input_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                pass

    def think(self, g: MancalaGame):
        while True:
            pos = self.input_int('pos: ')
            try:
                g.copy().move(pos)
                break
            except MancalaGameError as e:
                print(e)
        return pos
