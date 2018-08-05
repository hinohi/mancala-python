# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result


_INF = 10**8


def _eval_result(side, g):
    res = g.state
    if res is Result.WIN_PRE:
        if side == 0:
            return _INF
        else:
            return -_INF
    elif res is Result.WIN_EPI:
        if side == 1:
            return _INF
        else:
            return -_INF
    elif res is Result.DRAW:
        return 0


def evf_point_diff(side: int, g: MancalaGame) -> int:
    res = _eval_result(side, g)
    if res is not None:
        return res
    pre, epi = g.get_points()
    if side == 0:
        return pre - epi
    else:
        return epi - pre
