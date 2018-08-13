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
        self.board = [
            [self.stone_num] * self.pit_num + [0],
            [self.stone_num] * self.pit_num + [0],
        ]
        self.side = 0
        self._state = None

    def copy(self) -> 'MancalaGame':
        new = self.__new__(self.__class__)
        new.pit_num = self.pit_num
        new.stone_num = self.stone_num
        new.board = [self.board[0][:], self.board[1][:]]
        new.side = self.side
        new._state = None
        return new

    def to_vec(self):
        v = [self.side]
        v.extend(self.board[0])
        v.extend(self.board[1])
        return tuple(v)

    @classmethod
    def from_vec(cls, v) -> 'MancalaGame':
        new = cls.__new__(cls)
        new.side = v[0]
        new.pit_num = (len(v) - 1) // 2 - 1
        new.stone_num = sum(v[1:]) // (new.pit_num * 2)
        new.board = [
            v[1:2 + new.pit_num],
            v[2 + new.pit_num:],
        ]
        new._state = None
        return new

    def _move_stone(self, side: int, pos: int, num: int) -> (int, int):
        is_self = side == self.side
        if pos + num <= self.pit_num + is_self:
            for i in range(pos, pos + num):
                self.board[side][i] += 1
            end_pos = pos + num - is_self
            return side, end_pos
        else:
            for i in range(pos, self.pit_num + is_self):
                self.board[side][i] += 1
            rest = num - (self.pit_num + is_self - pos)
            return self._move_stone(1 - side, 0, rest)

    def move(self, pos):
        self._state = None
        side = self.side

        if not (0 <= pos < self.pit_num and self.board[side][pos] > 0):
            raise MancalaGameError('posが不正です: pos=%s board=%s' % (pos, self.board))

        self_stone = self.board[side][pos]
        self.board[side][pos] = 0
        end_side, end_pos = self._move_stone(side, pos + 1, self_stone)
        if end_side == side:
            if end_pos == self.pit_num:
                next_side = side
            else:
                next_side = 1 - side
                if self.board[side][end_pos] == 1:
                    opposite_pos = self.pit_num - 1 - end_pos
                    opposite_num = self.board[1 - side][opposite_pos]
                    if opposite_num:
                        self.board[1 - side][opposite_pos] = 0
                        self.board[side][self.pit_num] += opposite_num
        else:
            next_side = 1 - side

        self.side = next_side
        return next_side

    def pos_candidates(self):
        return [i for i, n in enumerate(self.board[self.side][:-1]) if n > 0]

    def get_points(self):
        return self.board[0][-1], self.board[1][-1]

    @property
    def state(self) -> Result:
        if self._state is not None:
            return self._state
        rest_pre = sum(self.board[0][:-1])
        rest_epi = sum(self.board[1][:-1])
        if rest_pre == 0 or rest_epi == 0:
            pre = self.board[0][-1]
            epi = self.board[1][-1]
            if pre > epi:
                self._state = Result.WIN_PRE
                return Result.WIN_PRE
            elif pre < epi:
                self._state = Result.WIN_EPI
                return Result.WIN_EPI
            else:
                self._state = Result.DRAW
                return Result.DRAW
        self._state = Result.IN_BATTLE
        return Result.IN_BATTLE

    @property
    def score(self):
        return abs(self.board[0][-1] - self.board[1][-1])

    def purity_dumps(self):
        ret = []
        width = len(str(self.pit_num * self.stone_num))
        fmt = '{:%s}' % width
        op_side_stones = [fmt.format(s) for s in self.board[1][:-1]]
        op_side_stones = [fmt.format('')] + op_side_stones + [fmt.format('')]
        ret.append('|'.join(op_side_stones[::-1]))
        scores = [fmt.format(self.board[1][-1])]
        scores += [fmt.format('')] * self.pit_num
        scores += [fmt.format(self.board[0][-1])]
        ret.append('|'.join(scores))
        self_side_stones = [fmt.format(s) for s in self.board[0][:-1]]
        self_side_stones = [fmt.format('')] + self_side_stones + [fmt.format('')]
        ret.append('|'.join(self_side_stones))
        return '\n'.join(ret)
