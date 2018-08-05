# -*- coding: utf-8 -*-
from typing import Callable

from common.game import MancalaGame


class AIBase:

    def __init__(self, side: int):
        self.side = side

    def think(self, g: MancalaGame) -> int:
        raise NotImplemented


class OneEvalFuncAIBase(AIBase):

    def __init__(self, side, eval_func: Callable[[int, MancalaGame], int]):
        super().__init__(side)
        self.eval_func = eval_func
