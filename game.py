##############################################################################
# FILE: game.py
# WRITERS: Shahar Jacob, shahar.jacob, 305255176
# Eden Elmaliah ,eden.e236, 204625206
# EXERCISE: ex12
# DESCRIPTION: in this file there is the logic behind the four in a row
# game.
##############################################################################


class Game:
    """
    This class initials a plain game board (a dictionary). it's in charge of
    all the changes in the board dictionary. The functions in this class
    are checking the board and makes changes in it when needed.
    """
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    LEN_BOARD = 6
    WID_BOARD = 7
    EMPTY_CELL = None
    COLORS = 'Coconut', 'Pineapple'
    NUM_OF_SEQ = 4
    TOP_ROW = 0
    EXCEPTION_MESSAGE = 'Illegal move.'

    def __init__(self):
        """
        constructor for the Game class. initials a Game object with a plain
        board
        """
        self.__board = self.create_board()

    def create_board(self):
        """
        function that creates a plain game board as a dictionary
        :return: a dictionary in the form of {(x,y): EMPTY_CELL}
        """
        board = {}
        for row in range(self.LEN_BOARD):
            for col in range(self.WID_BOARD):
                board[(row, col)] = self.EMPTY_CELL

        return board

    def legal_assignment(self, column):
        """
        function that determine if an assignment is legal, return True if
        it is, False otherwise.
        :param column: the column to check (an integer)
        :return: True if assignment is legal, otherwise - False.
        """
        # check if the top cell in this column is occupied
        if self.__board[(self.TOP_ROW, column)]:
            return False

        return True

    def get_comp_row(self, column):
        """
        checks in a given column where was the last disc placed (this would
        be the row the computer just placed a disc in)
        :param column: a given column
        :return: the row that the computer just placed a disc in
        """
        for row in range(self.LEN_BOARD):
            # this runs on rows from the upper part of the board downward
            if self.__board[(row, column)] is not self.EMPTY_CELL:
                return row

    def make_move(self, column):
        """
        receives a column, and checks if the assignment is valid. if it is
        executes the move, otherwise throws an exception.
        :param column: a given column on the board (integer)
        :return: the row that the disc was placed in
        """
        current_player = self.get_current_player()
        if not self.legal_assignment(column):
            raise Exception(self.EXCEPTION_MESSAGE)

        for row in range(self.LEN_BOARD - 1, -1, -1):  # runs on rows from
            # the bottom of the board upward
            if not self.__board[(row, column)]:  # place a disc in the first
                #  vacant row
                self.__board[(row, column)] = self.COLORS[current_player]
                return row

    def right_left(self):
        """
        transform the board to the form of list of strings. in addition,
        creates a list of all the coordinates of every row.
        :return: a list of rows in the form of strings, and a list of lists of
        coordinates
        """
        rows_strings = []
        coords_lst = []
        for row in range(self.LEN_BOARD):
            temp_string = ''
            row_coords = []
            for col in range(self.WID_BOARD):
                temp_string += str(self.__board[(row, col)])
                row_coords.append((row, col))
            rows_strings.append(temp_string)
            coords_lst.append(row_coords)
        return rows_strings, coords_lst

    def up_down(self):
        """
        transform the column of the board to the form of list of strings. in
        addition, creates a list of all the coordinates of every column.
        :return: a list of columns in the form of strings, and a list of
        lists of coordinates
        """
        cols_string = []
        coords_lst = []
        for col in range(self.WID_BOARD):
            temp_string = ''
            col_coords = []
            for row in range(self.LEN_BOARD):
                temp_string += str(self.__board[(row, col)])
                col_coords.append((row, col))
            cols_string.append(temp_string)
            coords_lst.append(col_coords)
        return cols_string, coords_lst

    def leftdown_rightup(self):
        """
        transform the diagonals (from bottom left to upper right) of the
        board to the form of list of strings. in addition, creates a list of
         all the coordinates of every diagonal.
        :return: a list of the diagonals in the form of strings, and a list of
        lists of coordinates
        """
        leftdown_rightup_strings = []
        coords_lst = []
        for diag in range(1 - self.LEN_BOARD, self.WID_BOARD):
            temp_str = ''
            diag_coords = []
            for row_index in range(self.LEN_BOARD):
                for col_index in range(self.WID_BOARD):
                    if col_index - row_index == diag:
                        temp_str += str(self.__board[row_index, col_index])
                        diag_coords.append((row_index, col_index))
            leftdown_rightup_strings.append(temp_str)
            coords_lst.append(diag_coords)
        return leftdown_rightup_strings, coords_lst

    def leftup_rightdown(self):
        """
        transform the diagonals (from upper left to bottom right) of the
        board to the form of list of strings. in addition, creates a list of
         all the coordinates of every diagonal.
        :return: a list of the diagonals in the form of strings, and a list of
        lists of coordinates
        """
        leftup_rightdown_strings = []
        coords_lst = []
        for diag in range(2 - self.LEN_BOARD, self.WID_BOARD + 1):
            temp_str = ''
            coords_line = []
            for row_index in range(self.LEN_BOARD):
                for col_index in range(self.WID_BOARD):
                    if self.WID_BOARD - col_index - row_index == diag:
                        temp_str += str(self.__board[row_index, col_index])
                        coords_line.append((row_index, col_index))
            leftup_rightdown_strings.append(temp_str)
            coords_lst.append(coords_line)
        return leftup_rightdown_strings, coords_lst

    def string_to_lst(self, string):
        """
        takes a string of attached words, and separate it into a list of
        words.for example-'RedNoneGreen' will turn into ['Red','None',
        'Green']. more in special comments.
        :param string: a string of attached words
        :return: a list of words
        """
        colors_lst = []
        word = string[0]
        for i in string[1::]:
            if i.islower():  # will distinguish between words with capital
                # letter
                word += i
            else:
                colors_lst.append(word)
                word = i
        colors_lst.append(word)
        return colors_lst

    def seq_coords(self, string, color, coords_list):
        """
        finds the coordination of a winning sequence
        :param string: the string where the winning sequence is at. can be a
        row/column/diagonal of the board
        :param color: the winning color
        :param coords_list: a list of the string coordination on the board
        :return: the sequence of the winning coordination
        """

        colors_lst = self.string_to_lst(string)
        i = 0
        for j in range(len(colors_lst)):
            if colors_lst[j] == color:
                i += 1
                if i == self.NUM_OF_SEQ:  # if the color appears 4 times in
                    # a row
                    return coords_list[j - 3:j + 1]
            else:
                i = 0

    def get_winner_helper(self, lists):
        """
        function that determines whether there is a draw, or one of the
        participants won, or if the game continues.
        :param lists: lists[0] is a list of strings, and lists[1] is a list of
        coordination.
        :return: the state of the game (draw/the winner/None) and a list of the
        winning coordination (if there is a win. otherwise it returns None)
        """

        for i, row in enumerate(lists[0]):
            # if a color appears 4 times in a row in any direction
            if self.COLORS[self.PLAYER_ONE] * self.NUM_OF_SEQ in row:
                coords = self.seq_coords(row, self.COLORS[self.PLAYER_ONE],
                                         lists[1][i])
                return self.PLAYER_ONE, coords

            elif self.COLORS[self.PLAYER_TWO] * self.NUM_OF_SEQ in row:
                coords = self.seq_coords(row, self.COLORS[self.PLAYER_TWO],
                                         lists[1][i])
                return self.PLAYER_TWO, coords

        for col in range(self.WID_BOARD):
            if not self.__board[(self.TOP_ROW, col)]:
                break  # board is not full, keep checking
        else:  # board is full (happens if we have not reached the condition)
            return self.DRAW, None

        return None  # game continues

    def get_win_seq(self):
        """
        :return: the winning coordination
        """
        if self.get_winner_helper(self.right_left()) is not None:
            return self.get_winner_helper(self.right_left())[1]

        if self.get_winner_helper(self.up_down()) is not None:
            return self.get_winner_helper(self.up_down())[1]

        if self.get_winner_helper(self.leftdown_rightup()) is not None:
            return self.get_winner_helper(self.leftdown_rightup())[1]

        if self.get_winner_helper(self.leftup_rightdown()) is not None:
            return self.get_winner_helper(self.leftup_rightdown())[1]

    def get_winner(self):
        """
        function that uses 'get_winner_helper' to determine if there is a
        draw (board is full), checking all the direction and determine if one
        of the player won, otherwise return None (game continue)
        :return: self.DRAW if there is a draw, self.PLAYER_ONE if player one
        won, self.PLAYER_TWO if player two won, and None if game continues.
        """
        # checking sequence in rows
        if self.get_winner_helper(self.right_left()) is not None:
            return self.get_winner_helper(self.right_left())[0]

        # checking sequence in columns
        if self.get_winner_helper(self.up_down()) is not None:
            return self.get_winner_helper(self.up_down())[0]

        # checking sequence in diagonals (gradient of (+1)).
        if self.get_winner_helper(self.leftdown_rightup()) is not None:
            return self.get_winner_helper(self.leftdown_rightup())[0]

        # checking sequence in diagonals (gradient of (-1)).
        if self.get_winner_helper(self.leftup_rightdown()) is not None:
            return self.get_winner_helper(self.leftup_rightdown())[0]

        return None

    def get_player_at(self, row, col):
        """
        gets row and column and returns the player in this cell.
        :param row: a given row (an integer)
        :param col: a given column (an integer)
        :return: the player in this cell.
        """
        return self.__board[(row, col)]

    def get_current_player(self):
        """
        checks who is the current player in the game
        :return: the current player
        """
        num_of_discs = self.count_discs()
        if num_of_discs % 2 == 0:
            return self.PLAYER_ONE
        return self.PLAYER_TWO

    def count_discs(self):
        """
        :return: the number of discs on the board
        """
        num_of_discs = 0
        for cell in self.__board.values():
            if cell:  # count how many discs are on the board
                num_of_discs += 1
        return num_of_discs

    def ai_strings(self):  # for the bonus
        """
        this function create a list of all the lines in the board (rows,
        columns, and diagonals), and also create a list of the coordination of
        all the cells in every row/col/diagonal.
        :return:
        """
        lst_strings = []
        lst_coords = []
        lst_strings.extend(self.right_left()[0])
        lst_coords.extend(self.right_left()[1])
        lst_strings.extend(self.up_down()[0])
        lst_coords.extend(self.up_down()[1])
        lst_strings.extend(self.leftdown_rightup()[0])
        lst_coords.extend(self.leftdown_rightup()[1])
        lst_strings.extend(self.leftup_rightdown()[0])
        lst_coords.extend(self.leftup_rightdown()[1])

        return lst_strings, lst_coords

    def ai_move(self):  # for the bonus
        """
        function that runs on all the lines in the board (rows, columns,
        and diagonals) and checking if there is a line that has 3 discs
        from the same color, so the next move would be a win, and puts a
        disc in this cell if possible.
        :return: column if possible, None otherwise.
        """
        string_lst, coords_lst = self.ai_strings()
        for row_index, row_string in enumerate(string_lst):
            colors_lst = self.string_to_lst(row_string)
            # winning sequence can be in a row of four or more:
            if len(colors_lst) >= self.NUM_OF_SEQ:
                for j in range(len(colors_lst) - 3):
                    if (colors_lst[j:j + self.NUM_OF_SEQ].count(
                            self.COLORS[0]) == 3 or colors_lst[
                                                    j:j + self.NUM_OF_SEQ].
                            count(
                        self.COLORS[1]) == 3) and str(self.EMPTY_CELL) \
                            in colors_lst[j:j + self.NUM_OF_SEQ]:
                        col = self.quartet_check(j, colors_lst, coords_lst,
                                                 row_index)
                        return col

    def quartet_check(self, outside_index, colors_lst, lst_coords, row_index):
        """  for the bonus !!!
        this function gets sequence of 4 cells and determine if the disc
        can be placed in one of them (if its None, and there is another disc
        under it).
        :param outside_index: an integer number
        :param colors_lst: list of colors
        :param lst_coords: list of the coordination of the colors
        :param row_index: an integer number
        :return: column (integer number), if possible, otherwise return None.
        """
        for index, color in enumerate(
                colors_lst[outside_index:outside_index + self.NUM_OF_SEQ]):
            if color == str(self.EMPTY_CELL):
                col = lst_coords[row_index][index + outside_index][1]
                row = lst_coords[row_index][index + outside_index][0]
                if row == (self.LEN_BOARD - 1):
                    return col
                # Check if the the cell beneath has disc in it, otherwise
                # the disc can't be in it
                elif self.get_player_at(row + 1, col) is not \
                        self.EMPTY_CELL:
                    return col
