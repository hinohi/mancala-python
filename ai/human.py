# -*- coding: utf-8 -*-
from common.game import MancalaGameError, MancalaGame
from ai.base import AIBase


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


class HumanAI(AIBase):

    def think(self, g: MancalaGame):
        while True:
            pos = input_int('pos: ')
            try:
                g.copy().move(pos)
                break
            except MancalaGameError as e:
                print(e)
        return pos

