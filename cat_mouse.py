#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cat_mouse.py
@Time    :   2021/01/07 17:12:23
@Author  :   lzh 
@Version :   1.0
@Contact :   robinlin163@163.com
@Desc    :   cat mouse catch example and corresponding env and agent.
'''
import random
import numpy as np
from utils import (
    move_on_board,
    index2pos,
    pos2index,
    Label
)


class CatAgent(object):
    """Cat Agent for example.

    Attributes:
        Q (np.ndarray): [n_states, n_states, 4], state is position's index.
        state (int): indicate state agent face.
    """

    def __init__(self, Q, state,):
        self.Q = Q
        self.state = state

    def recv(self, state):
        self.state = state

    def action(self):
        return np.argmax(self.Q[self.state])


class Mouse(object):
    """Mouse object, move in a MDP manner.

    Attributes:
        pos (tuple (x, y)): mouse location.
        move: move method for mouse.
    """

    def __init__(self, pos, board, ):
        self.pos = pos
        self.board = board

    def move(self):
        """random move.
        """
        action = random.randint(0, 3)
        pos = move_on_board(self.pos, action, self.board.shape)
        if self.board[pos] != Label.block:
            self.pos = pos
        return self.pos


class BoardEnv(object):
    """Cat Catch Mouse Env.

    Attributes:
        state (tuple (int, int)): cat and mouse position.
        board (np.ndarray): board map, 0 means empty, 1 means block.
        recv: recieve action and return updated state and reward.
    """

    def __init__(self, state, board):
        self.state = state
        self.board = board
        self.mouse = Mouse(index2pos(state[1]), self.board.shape)

    def recv(self, action):
        """
        Args:
            action (int): [0--3].
        """
        cat_pos = index2pos(self.state[0], self.board.shape)
        cat_pos = move_on_board(cat_pos, action, self.board.shape)
        mouse_pos = self.mouse.move()
        self.state = (
            pos2index(cat_pos, self.board.shape),
            pos2index(mouse_pos, self.board.shape)
        )

    def is_terminate(self):
        catch = self.state[0] == self.state[1]
        block = self.board[pos2index[self.state[0]]] == Label.block
        return catch or block

    def reward(self):
        if self.state[0] == self.state[1]:
            return 10
        elif self.board[pos2index[self.state[0]]] == Label.block:
            return -10
        else:
            return -1