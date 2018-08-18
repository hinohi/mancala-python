# -*- coding: utf-8 -*-
from common.game import MancalaGame, Result
from learn_eval_func.db import session, Board, add_board, add_move


class Node:
    def __init__(self, g: MancalaGame):
        self.g = g
        self.vec = g.to_str()
        self.side = g.side
        self.children = []
        p0, p1 = self.g.get_points()
        n = self.g.pit_num * self.g.stone_num * 2
        self.raw_score = (p0 - p1) / n
        if g.state is Result.IN_BATTLE:
            self.searched = False
        else:
            self.searched = True

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
        elif not self.searched:
            for gg in self.g.iter_nex():
                self.children.append(Node(gg))
            self.searched = True
        self.g = None

    def collect_board(self):
        s = {self.vec: (self.score, self.searched)}
        for c in self.children:
            ss = c.collect_board()
            for vec in ss:
                if ss[vec][1] or vec not in s:
                    s[vec] = ss[vec]
        return s

    def collect_move(self):
        s = {(self.vec, c.vec) for c in self.children}
        for c in self.children:
            s = s.union(c.collect_move())
        return s


class GenData:

    def __init__(self, pit, stone, score_depth):
        self.pit = pit
        self.stone = stone
        self.score_depth = score_depth
        self.num = pit

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
        q = session.query(Board.searched)
        for g in self.iter_g():
            vec = g.to_str()
            searched = q.filter(Board.vec == vec).first()
            if searched:
                continue
            node = Node(g)
            for _ in range(self.score_depth):
                node.grow()
            boards = node.collect_board()
            add_board(boards)
            session.commit()
            moves = node.collect_move()
            add_move(moves)
            session.commit()
            i += 1
            if i >= n:
                break


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('--pit', '-p', type=int, default=6)
    p.add_argument('--stone', '-s', type=int, default=4)
    p.add_argument('--depth', '-d', type=int, default=3)
    p.add_argument('--num', '-n', type=int, default=1000)

    args = p.parse_args()

    gen = GenData(args.pit, args.stone, args.depth)
    gen.make(args.num)


if __name__ == '__main__':
    main()
