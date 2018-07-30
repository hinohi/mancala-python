# -*- coding: utf-8 -*-
from enum import Enum


__all__ = [
    'Result',
    'MancalaGameError',
    'MancalaGame',
]


class Result(Enum):
    IN_BATTLE = 0
    WIN_PRE = 1
    WIN_EPI = 2
    DRAW = 3


class MancalaGameError(Exception):
    pass


class MancalaGame:

    def __init__(self, pit, stone):
        assert pit > 0
        assert stone > 0
        self.pit_num = pit
        self.stone_num = stone
        self.pits = [
            [self.stone_num] * self.pit_num + [0],
            [self.stone_num] * self.pit_num + [0],
        ]
        self.side = 0
        self.rest_stones = [self.stone_num * self.pit_num] * 2

    def copy(self):
        new = self.__new__(self.__class__)
        new.pit_num = self.pit_num
        new.stone_num = self.stone_num
        new.pits = [self.pits[0][:], self.pits[1][:]]
        new.side = self.side
        new.rest_stones = self.rest_stones[:]
        return new

    def _move_stone(self, side: int, pos: int, num: int) -> (int, int):
        is_self = side == self.side
        if pos + num <= self.pit_num + is_self:
            for i in range(pos, pos + num):
                self.pits[side][i] += 1
            end_pos = pos + num - is_self
            if end_pos == self.pit_num:
                self.rest_stones[side] -= 1
            return side, end_pos
        else:
            for i in range(pos, self.pit_num + is_self):
                self.pits[side][i] += 1
            self.rest_stones[side] -= is_self
            rest = num - (self.pit_num + is_self - pos)
            return self._move_stone(1 - side, 0, rest)

    def move(self, pos):
        side = self.side

        if not (0 <= pos < self.pit_num and self.pits[side][pos] > 0):
            raise MancalaGameError('posが不正です')

        self_stone = self.pits[side][pos]
        self.pits[side][pos] = 0
        end_side, end_pos = self._move_stone(side, pos + 1, self_stone)
        if end_side == side:
            if end_pos == self.pit_num:
                next_side = side
            else:
                next_side = 1 - side
                if self.pits[side][end_pos] == 1:
                    opposite_pos = self.pit_num - 1 - end_pos
                    opposite_num = self.pits[1 - side][opposite_pos]
                    if opposite_num:
                        self.pits[1 - side][opposite_pos] = 0
                        self.pits[side][self.pit_num] += opposite_num
                        self.rest_stones[1 - side] -= opposite_num
        else:
            next_side = 1 - side

        assert sum(self.rest_stones) == sum(self.pits[0][:-1]) + sum(self.pits[1][:-1])

        self.side = next_side
        return next_side

    @property
    def state(self) -> Result:
        if self.rest_stones[0] == 0 or self.rest_stones[1] == 0:
            pre, epi = self.pits[0][-1], self.pits[1][-1]
            if pre > epi:
                return Result.WIN_PRE
            elif pre < epi:
                return Result.WIN_EPI
            else:
                return Result.DRAW
        return Result.IN_BATTLE

    def purity_dumps(self):
        ret = []
        width = len(str(self.pit_num * self.stone_num))
        fmt = '{:%s}' % width
        op_side_stones = [fmt.format(s) for s in self.pits[1][:-1]]
        op_side_stones = [fmt.format('')] + op_side_stones + [fmt.format('')]
        ret.append('|'.join(op_side_stones[::-1]))
        scores = [fmt.format(self.pits[1][-1])]
        scores += [fmt.format('')] * self.pit_num
        scores += [fmt.format(self.pits[0][-1])]
        ret.append('|'.join(scores))
        self_side_stones = [fmt.format(s) for s in self.pits[0][:-1]]
        self_side_stones = [fmt.format('')] + self_side_stones + [fmt.format('')]
        ret.append('|'.join(self_side_stones))
        return '\n'.join(ret)
