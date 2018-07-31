# -*- coding: utf-8 -*-
import json
import argparse
from typing import List
from pathlib import Path
from collections import namedtuple

from game import MancalaGame, Result


SearchResult = namedtuple('SearchResult', ['result', 'record', 'score'])


def _dfs(g: MancalaGame, record: List[List[int]]) -> (Result, int, List[List[int]]):
    if g.state is not Result.IN_BATTLE:
        return g.state, g.score, record
    win = Result.WIN_PRE if g.side == 0 else Result.WIN_EPI
    lose = Result.WIN_EPI if g.side == 0 else Result.WIN_PRE
    best = None
    for pos in g.pos_candidates():
        gg = g.copy()
        gg.move(pos)
        res = _dfs(gg, record + [[g.side, pos]])
        if best is None:
            best = res
        if res[0] is win:
            if best[0] is not win:
                best = res
            elif best[1] < res[1]:
                # スコアが良い
                best = res
            elif best[1] == res[1] and len(best[2]) > len(res[2]):
                # スコアが同じならできるだけ早く勝つ
                best = res
        elif res[0] is Result.DRAW:
            if best[0] is lose:
                best = res
            elif len(best[2]) < len(res[2]):
                # 引き分けならばできるだけ試合を引っ張る
                best = res
        elif best[0] is lose:
            if best[1] > res[1]:
                # 負け具合を緩和
                best = res
            elif len(best[2]) < len(res[2]):
                # できるだけ試合を引っ張る
                best = res
    return best


def dfs(pit, stone) -> SearchResult:
    g = MancalaGame(pit, stone)
    result, score, record = _dfs(g, [])
    return SearchResult(result, record, score)


def _dfs_result_only(g: MancalaGame, record: List[List[int]]) -> (Result, List[List[int]]):
    if g.state is not Result.IN_BATTLE:
        return g.state, record
    win = Result.WIN_PRE if g.side == 0 else Result.WIN_EPI
    lose = Result.WIN_EPI if g.side == 0 else Result.WIN_PRE
    best = None
    for pos in g.pos_candidates():
        gg = g.copy()
        gg.move(pos)
        res = _dfs_result_only(gg, record + [[g.side, pos]])
        if best is None:
            best = res
        if res[0] is win:
            best = res
            break
        elif res[0] is Result.DRAW:
            if best[0] is lose:
                best = res
            elif len(best[1]) < len(res[1]):
                # 引き分けならばできるだけ試合を引っ張る
                best = res
        elif best[0] is lose:
            if len(best[1]) < len(res[1]):
                # できるだけ試合を引っ張る
                best = res
    return best


def dfs_result_only(pit, stone) -> SearchResult:
    g = MancalaGame(pit, stone)
    result, record = _dfs_result_only(g, [])
    return SearchResult(result, record, None)


def main():
    tasks = {
        'dfs': dfs,
        'dfs_result_only': dfs_result_only,
    }
    p = argparse.ArgumentParser()
    p.add_argument('task', choices=list(tasks))
    p.add_argument('--pit', '-p', type=int, default=4)
    p.add_argument('--stone', '-s', type=int, default=4)
    p.add_argument('--no-debug', action='store_true')
    p.add_argument('--output', '-o')
    args = p.parse_args()

    result = tasks[args.task](args.pit, args.stone)
    g = MancalaGame(args.pit, args.stone)
    data = {
        'pit': args.pit,
        'stone': args.stone,
        'board': [],
    }
    print(f'pit={args.pit}')
    print(f'stone={args.stone}')
    if not args.no_debug:
        print(g.purity_dumps())
    for side, pos in result.record:
        g.move(pos)
        if not args.no_debug:
            print()
            print(f'side={side}')
            print(f'pos={pos}')
            print(g.purity_dumps())
        data['board'].append(g.copy().board)
    print(result.result)
    print(f'score={result.score}')

    if args.output:
        path = Path(args.output)
        with path.open('w') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
