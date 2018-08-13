# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result


class Node:
    def __init__(self, g: MancalaGame):
        self.g = g
        self.side = g.side
        self.children = []
        if g.state is Result.IN_BATTLE:
            p0, p1 = self.g.get_points()
            n = self.g.pit_num * self.g.stone_num * 2
            self.raw_score = (p0 - p1) / n
        elif g.state is Result.WIN_PRE:
            self.raw_score = 1.0
        elif g.state is Result.WIN_EPI:
            self.raw_score = -1.0
        else:
            self.raw_score = 0.0

    @staticmethod
    def iter_nex(g: MancalaGame):
        ini_side = g.side
        stack = [g]
        while stack:
            g = stack.pop()
            for pos in g.pos_candidates():
                gg = g.copy()
                nex = gg.move(pos)
                if gg.state is Result.IN_BATTLE:
                    if nex == ini_side:
                        stack.append(gg)
                        continue
                yield gg

    @property
    def score(self):
        if self.children:
            c_score = [c.score for c in self.children]
            if self.side == 0:
                return max(c_score)
            else:
                return min(c_score)
        return self.raw_score

    @property
    def depth(self):
        return 1 + max(c.depth for c in self.children)

    @property
    def num_node(self):
        return 1 + sum(c.num_node for c in self.children)

    def grow(self):
        if self.children:
            for c in self.children:
                c.grow()
        elif self.g.state is Result.IN_BATTLE:
            for gg in self.iter_nex(self.g):
                self.children.append(Node(gg))


class GenData:

    def __init__(self, pit, stone, score_depth):
        self.pit = pit
        self.stone = stone
        self.score_depth = score_depth
        self.num = pit
        self.mem = {}

    def dump(self):
        return {
            'pit': self.pit,
            'stone': self.stone,
            'score_depth': self.score_depth,
            'data': [
                {
                    'v': vec,
                    's': score,
                } for vec, score in self.mem.items()
            ]
        }

    @classmethod
    def load(cls, data):
        new = cls(data['pit'], data['stone'], data['score_depth'])
        for d in data['data']:
            new.mem[tuple(d['v'])] = d['s']
        return new

    def iter_g(self):
        from random import choice

        while True:
            g = MancalaGame(self.pit, self.stone)
            while g.state is Result.IN_BATTLE:
                yield g
                pos = choice(g.pos_candidates())
                g.move(pos)

    def make(self, n):
        i = 0
        for g in self.iter_g():
            vec = g.to_vec()
            if vec in self.mem:
                continue
            i += 1
            node = Node(g)
            score = [node.score]
            for j in range(self.score_depth):
                node.grow()
                score.append(node.score)
            self.mem[vec] = score
            if i >= n:
                break


def main():
    import json
    import argparse
    from pathlib import Path

    p = argparse.ArgumentParser()
    p.add_argument('--pit', '-p', type=int, default=6)
    p.add_argument('--stone', '-s', type=int, default=5)
    p.add_argument('--depth', '-d', type=int, default=3)
    p.add_argument('--num', '-n', type=int, default=1000)
    p.add_argument('--output', '-o', required=True)
    p.add_argument('--input', '-i')

    args = p.parse_args()

    data = None
    if args.input:
        inp = Path(args.input)
        if inp.exists():
            with inp.open() as f:
                data = json.load(f)
    if data:
        gen = GenData.load(data)
    else:
        gen = GenData(args.pit, args.stone, args.depth)

    gen.make(args.num)
    with Path(args.output).open('w') as f:
        json.dump(gen.dump(), f, separators=(',', ':'))


if __name__ == '__main__':
    main()
