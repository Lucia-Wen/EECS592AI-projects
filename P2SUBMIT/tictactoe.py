"""tictactoe

This minimax algothim to formulate a never lose tictactoe game.
$ python tictactoe.py s
s is a integer
output: tictactoe.txt
"""

import random
import sys
from copy import deepcopy

class State(object):
    """ State class including board(current game board),
    actions(actions left), terminal(if the state is complete ) ,
     insertion(current insertion 'x' or 'o')
    """
    def __init__(self, board, actions, insertion, terminal=False):
        self.board = board
        self.actions = actions
        self.terminal = terminal
        self.insertion = insertion

    def terminal_test(self):
        """return whether this state is true
        """
        if self.terminal:
            return True
        return False

def convert(num):
    """convert integer to 2d axis

    """
    a_axis = 2 - num//3
    b_axis = num%3
    return a_axis, b_axis
def insert_board(board, action):
    """insert current operation to board location

    """
    board[action[0]][action[1]] = action[2]

def termination(board, a_axis, b_axis, rem_t, sy_t):
    """check if current board is terminated

    """
    if not rem_t:
        return True
    if board[0][0] == board[1][1] == board[2][2] == sy_t or board[2][0] == board[0][2] == board[1][1] == sy_t:
        return True
    if board[a_axis][0] == board[a_axis][1] == board[a_axis][2] == sy_t or board[0][b_axis] == board[1][b_axis] == board[2][b_axis] == sy_t:
        return True
    return False
    #def __init__(self, board, actions, insertion, parent = None, terminal = False):
def result(state, a_r):
    """return next state after action a

    """
    rem_result = deepcopy(state.actions)
    board = []
    for bitem in state.board:
        board.append(deepcopy(bitem))
    rem_result.remove(a_r)
    a_axis, b_axis = convert(a_r)
    insertion = [a_axis, b_axis, '']
    if state.insertion[2] == 'O':
        insertion[2] = 'X'
    else:
        insertion[2] = 'O'
    insert_board(board, [a_axis, b_axis, insertion[2]])
    terminal = termination(board, a_axis, b_axis, rem_result, insertion[2])
    return State(board, rem_result, insertion, terminal)

def utility(state):
    """return final utility value

    """
    a_axis, b_axis = state.insertion[0], state.insertion[1]
    board = state.board
    if state.actions:
        if state.insertion[2] == 'O':
            return 1
        return -1
    else:
        if board[0][0] == board[1][1] == board[2][2] or board[2][0] == board[0][2] == board[1][1]:
            if board[a_axis][b_axis] == 'O':
                return 1
            return -1
        if board[a_axis][0] == board[a_axis][1] == board[a_axis][2] or board[0][b_axis] == board[1][b_axis] == board[2][b_axis]:
            if board[a_axis][b_axis] == 'O':
                return 1
            return -1
    return 0

def maxvalue(state):
    """recursive max

    """
    if state.terminal:
        u_max = utility(state)
        return u_max
    v_max = float('-inf')
    for action in state.actions:
        v_max = max(v_max, minvalue(result(state, action)))
    return v_max

def minvalue(state):
    """recursive min

    """
    if state.terminal:
        u_min = utility(state)
        return u_min
    v_min = float('inf')
    for action in state.actions:
        v_min = min(v_min, maxvalue(result(state, action)))
    return v_min

def minimaxdecision(state):
    """minimax algorithm implementation

    """
    actionlst = []
    vlst = []
    for action in state.actions:
        actionlst.append(action)
        c_v = minvalue(result(state, action))
        vlst.append(c_v)
    mv_mini, idx_mini = max((vlst[i], i) for i in range(len(vlst)))
    return actionlst[idx_mini]

if __name__ == '__main__':
    S = int(sys.argv[1])
    print("Seed = "+str(S))
    random.seed(S)
    REM = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    CURRENT_BOARD = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    PREV = []
    while REM:
        CHOICE = random.choice(REM)
        REM.remove(CHOICE)
        A, B = convert(CHOICE)
        insert_board(CURRENT_BOARD, [A, B, 'X'])
        PREV.append(deepcopy(CURRENT_BOARD))
        if termination(CURRENT_BOARD, B, A, REM, 'X'):
            break
        CURRENT_STATE = State(CURRENT_BOARD, REM, [A, B, 'X'], terminal=False)
        CHOICE = minimaxdecision(CURRENT_STATE)
        REM.remove(CHOICE)
        A, B = convert(CHOICE)
        insert_board(CURRENT_BOARD, [A, B, 'O'])
        PREV.append(deepcopy(CURRENT_BOARD))
        if termination(CURRENT_BOARD, A, B, REM, 'O'):
            break
    with open('tictactoe.txt', 'w') as f:
        for item in PREV:
            for line in item:
                f.write(',' .join(line)+'\n')
            f.write('\n')
