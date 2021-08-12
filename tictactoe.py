import numpy as np
import os
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x = 0
    o = 0
    for ele in board:
        for pos in ele:
            if pos == 'X':
                x += 1
            if pos == 'O':
                o += 1
    if x == o:
        return X
    if o < x:
        return O


def actions(board):
    possible_actions = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == None:
                possible_actions.append((row, col))
    return possible_actions


def reverse(original_board, new_board):
    for row in range(3):
        for col in range(3):
            if original_board[row][col] != new_board[row][col]:
                return (row, col)


def result(board, action):
    turn = player(board)
    (row, _) = action
    (_, col) = action
    board[row][col] = turn
    return board


def emptyCount(board):
    emp_count = 0
    for row in board:
        for col in row:
            if col == EMPTY:
                emp_count += 1
    return (emp_count)


def winner(board):
    lett = [X, O]
    for let in lett:
        for pos in range(3):
            if board[pos][0] == let and board[pos][1] == let and board[pos][2] == let:
                return let
            elif board[0][pos] == let and board[1][pos] == let and board[2][pos] == let:
                return let
        if board[0][0] == let and board[1][1] == let and board[2][2] == let:
            return let
        if board[2][0] == let and board[1][1] == let and board[0][2] == let:
            return let
    else:
        return None


def terminal(board):
    if emptyCount(board) == 0:
        return True
    if winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        if emptyCount(board) == 0 and winner(board) is None:
            return 0
    else:
        return None


def minimax(board):
    moves = [[]] * (emptyCount(board) + 1)
    node = [board, None, []]
    moves[0] = [node]

    for movepos in range(0, len(moves)-1):
        for oldnode in range(0, len(moves[movepos])):
            if utility(moves[movepos][oldnode][0]) is None:
                possible_actions = actions(moves[movepos][oldnode][0])
                for action in possible_actions:
                    board = copy.deepcopy(moves[movepos][oldnode][0])
                    new_board = result(board, action)
                    value = utility(new_board)
                    if value is None:
                        value = []
                    if movepos == 0:
                        node = [new_board, oldnode, value, action]
                    else:
                        node = [new_board, oldnode, value]
                    if moves[movepos + 1] == []:
                        moves[movepos + 1] = [node]
                    else:
                        moves[movepos + 1].append(node)
        print('One Set Modelled')

    print('Possibilites Modeled')
    for pos in range(len(moves)-1, 1, -1):
        for node in moves[pos]:
            moves[pos-1][node[1]][2].append(node[2])

        for older_node2 in moves[pos-1]:
            if isinstance(older_node2[2], int):
                older_node2[2] = [older_node2[2]]
            if player(older_node2[0]) == X:
                older_node2[2] = max(older_node2[2])
            if player(older_node2[0]) == O:
                older_node2[2] = min(older_node2[2])
    print('Values Transferred')

    values = []
    for node in moves[1]:
        values.append(node[2])

    if player(moves[0][0][0]) == X:
        index = values.index(max(values))
    if player(moves[0][0][0]) == O:
        index = values.index(min(values))
    move = moves[1][index][3]
    return move