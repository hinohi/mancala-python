# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result


_INF = 10**8

_MODEL_CACHE = {}


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


def evf_factory(pit: int, stone: int, name: str):
    import pickle
    from pathlib import Path

    if name == 'simple':
        return evf_point_diff

    key = (pit, stone, name)
    if key not in _MODEL_CACHE:
        model_dir = Path('learn_eval_func/model')
        model = None
        for path in model_dir.glob(f'p{pit}s{stone}*_{name}*.pickle'):
            with path.open('rb') as f:
                model = pickle.load(f)
            break
        if not model:
            raise ValueError('unknown model: %s' % name)
        _MODEL_CACHE[key] = model

    model = _MODEL_CACHE[key]

    def _evf_ml(side: int, g: MancalaGame):
        m = model[g.side]
        vec = g.to_vec()
        score = m.predict([vec])[0]
        if side == 0:
            return score
        else:
            return -score

    return _evf_ml
