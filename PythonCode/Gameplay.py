__version__ = '0.1.0'

import numpy as np
from time import sleep

class Move(object):
    def __init__(self, score = None, xindex = None, yindex = None):
        self.x = xindex
        self.y = yindex
        self.score = score

    def update(self, newmove):
        self.x = newmove.x
        self.y = newmove.y
        self.score = newmove.score


class TacBoard(object):
    def __init__(self):
        self.board = np.zeros((3,3))  # 0 is no move, 1 is bot, -1 is user

    def get_free_space_vector(self):
        ret_vec = []
        for row in self.board:
            ret_vec += [True if v == 0 else False for v in row]
        return ret_vec

    def user_move(self, xindex, yindex):
        self.board[xindex, yindex] = -1

    def bot_move(self, xindex, yindex):
        self.board[xindex, yindex] = 1

    def get_best_move(self):
        return self._calc_move(self.board, 1)

    def get_worst_move(self):
        # For the memes....
        return self._calc_move(self.board, 1, worst=True)

    def _calc_move(self, board_array, player, worst=False):
        # Worst move for AI does minmin instead of minmax search
        if worst == True or player == -1:
            best_move = Move(np.inf)
        else:
            best_move = Move(-np.inf)

        moves = self.possible_moves(board_array)

        # Check if game is over
        score = self.win_check(board_array)
        if len(moves) == 0 or not score == 0:
            best_move.score = score
            return best_move

        # Otherwise do minmax search
        for move in moves:
            board_copy = board_array.copy()
            board_copy[move.x][move.y] = player
            test_move = self._calc_move(board_copy, -1 * player, worst=worst)
            test_move.x = move.x
            test_move.y = move.y

            if (worst == True and test_move.score < best_move.score) or \
                    (worst == False and player == 1 and test_move.score > best_move.score) or \
                    (worst == False and player == -1 and test_move.score < best_move.score):
                best_move.update(test_move)

        return best_move

    def possible_moves(self, board_array=None):
        if board_array is None:
            board_array = self.board

        return [Move(None, r, c) for r in range(3) for c in range(3) if board_array[r,c] == 0]

    @staticmethod
    def win_check(board_array):
        """ Return 0 if no win, 1 if bot win, -1 if user win """
        def check_set(oneset):
            if sum(oneset) == -3:
                return -1
            elif sum(oneset) == 3:
                return 1
            return 0

        for row in range(3):
            setresult = check_set(board_array[row])
            if setresult is not 0:
                return setresult

        for col in range(3):
            setresult = check_set(board_array[:,col])
            if setresult is not 0:
                return setresult

        diag1 = [board_array[0,0], board_array[1,1], board_array[2,2]]
        diag2 = [board_array[0,2], board_array[1,1], board_array[2,0]]

        for diagset in [diag1, diag2]:
            setresult = check_set(diagset)
            if setresult is not 0:
                return setresult
        
        return 0


# Standalone mode for testing
if __name__=='__main__':
    tacgame = TacBoard()
    tacgame.user_move(0,0)
    tacgame.bot_move(1,1)
    tacgame.user_move(1,0)
    nextmove = tacgame.get_best_move()
    # nextmove = tacgame.get_worst_move()
    print(nextmove.x, nextmove.y, nextmove.score)
    print(tacgame.get_free_space_vector())


"""
    bot=x

    o . .
    o x .
    . . .
"""