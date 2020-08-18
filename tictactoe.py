"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return "X"
    
    count_X = 0
    count_O = 0
    for row in board:
        for col in row:
            if col == "X":
                count_X += 1
            elif col == "O":
                count_O += 1
    
    if count_X > count_O:
        return "O"
    else:
        return "X"
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return "X"
    poss = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                poss.append((row, col))
    
    return poss

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    cop = copy.deepcopy(board)
    if action not in actions(cop):
        raise Exception("Invalid move")
    else:
        if player(cop) == "X":
            add = "X"
        else:
            add = "O"
    
    cop[action[0]][action[1]] = add
    return cop

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #rows:
    if (board[0][0] == board[0][1] == board[0][2]) and not board[0][0] == EMPTY:
        return board[0][0]
    if (board[1][0] == board[1][1] == board[1][2]) and not board[1][0] == EMPTY:
        return board[1][0]
    if (board[2][0] == board[2][1] == board[2][2]) and not board[2][0] == EMPTY:
        return board[2][0]

    #columns
    if (board[0][0] == board[1][0] == board[2][0]) and not board[0][0] == EMPTY:
        return board[0][0]
    if (board[0][1] == board[1][1] == board[2][1]) and not board[0][1] == EMPTY:
        return board[0][1]
    if (board[0][2] == board[1][2] == board[2][2]) and not board[0][2] == EMPTY:
        return board[0][2]

    #diagonals
    if (board[0][0] == board[1][1] == board[2][2]) and not board[0][0] == EMPTY:
        return board[0][0]
    if (board[0][2] == board[1][1] == board[2][0]) and not board[0][2] == EMPTY:
        return board[0][2]
    
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X" or winner(board) == "O":
        return True
    else:
        if any(EMPTY in subl for subl in board):
            return False
        else:
            return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -10000000000000
    for act in actions(board):
        v = max(v, min_value(result(board, act)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = 10000000000000
    for act in actions(board):
        v = min(v, max_value(result(board, act)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    acts = actions(board)
    print(acts)
    if player(board) == "X":
        vals = []
        for a in acts:
            vals.append(min_value(result(board, a)))
        print(vals)
        return acts[vals.index(max(vals))]
    elif player(board) == "O":
        vals = []
        for a in acts:
            vals.append(max_value(result(board, a)))
        print(vals)
        return acts[vals.index(min(vals))]

    
    raise NotImplementedError
