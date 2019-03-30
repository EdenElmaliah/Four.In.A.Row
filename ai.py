##############################################################################
# FILE: ai.py
# WRITERS: Shahar Jacob, shahar.jacob, 305255176
# Eden Elmaliah ,eden.e236, 204625206
# EXERCISE: ex12
# DESCRIPTION: in this file there is a class of artificial intelligence (AI).
# an AI object will make moves on the game board using the "find_legal_move" function.
##############################################################################

import random


class AI:
    """
    In this class there is only one function, which checks where the
    computer can put a disc on the board, and place it. An explanation on
    our algorithm is in special comments.
    """
    FIRST_COL = 0
    LAST_COL = 6
    NUM_OF_COLUMNS = 7
    EXCEPTION = 'No possible AI moves'

    def find_legal_move(self, g, func, timeout=None):
        """
        gets a Game() object and a function from game.py and determines in
        what column computer should play.
        :param g: a Game object (the dictionary board of the game)
        :param func: a given function that is making a move on the game board (func = g.make_move)
        :param timeout: None (we didn't use this parameter for our algorithm)
        :return: the chosen column for the move
        """
        col = g.ai_move()  # the ai improved algorithm
        if col is not None and g.legal_assignment(col):
            func(col)  # if the column is valid, make a move on the board
            return col

        already_chosen = set()
        col = random.randint(self.FIRST_COL, self.LAST_COL)  # choose a random
        # column
        already_chosen.update(str(col))
        while not g.legal_assignment(col):
            already_chosen.update(str(col))
            col = random.randint(self.FIRST_COL, self.LAST_COL)
            if len(already_chosen) == self.NUM_OF_COLUMNS:  # if all columns
                # are occupied
                raise Exception(self.EXCEPTION)
        func(col)  # if the column is valid, make a move on the board
        return col
