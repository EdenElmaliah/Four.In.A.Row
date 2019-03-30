##############################################################################
# FILE: four_in_a_row.py
# WRITERS: Shahar Jacob, shahar.jacob, 305255176
# Eden Elmaliah ,eden.e236, 204625206
# EXERCISE: ex12
# DESCRIPTION: in this file there is the execution of the four in a row
# game, including the graphic (gui) methods, communication between 2 players
#  (can be both human or computer), etc.  ENJOY!
##############################################################################

import tkinter as tk
from game import Game
from communicator import Communicator
import socket
from ai import AI
import sys

PARAM_ERROR_MESAGGE = 'Illegal program arguments.'
PLAYER_LOCATION = 1
PORT_LOCATION = 2
IP_LOCATION = 3
MIN_PORT = 1000
MAX_PORT = 65535
MIN_ARGS = 3
MAX_ARGS = 4
COMPUTER = 'ai'
HUMAN = 'human'


class Gui:
    """
    This class is in charge of the graphics of the game, and operating it as
     well. It changes the graphic board according to the changes in the
     Game object (a board dictionary).
    """
    TIE_SCORE = "It's a tie!"
    OPEN_MESSAGE = 'WELCOME!'
    WINNER_MESAGGE = 'YOU WON!'
    LOSER_MESSAGE = 'YOU LOST!'
    COL_0_COORD = 77
    COL_FACTOR = 90
    ROW_0_COORD = 557
    ROW_FACTOR = 67
    INDICATOR = 'column'
    TAG = 'player'
    PLAY = 'Your turn'
    DONT_PLAY = "Oppenent's turn"
    ON = 1
    OFF = 0
    INDICATOR_ROW = -1
    CANVAS_WID = 700
    CANVAS_HIGHT = 600
    ILLEGAL_TAG = 'illegal'
    OUT_OF_BOARD = 50
    TIME_OF_ILLEGAL_MOVE = 250
    WELCOME_FONT_SIZE = 50
    MAIN_TITLE_FONT_SIZE = 50
    SECOND_TITLE_FONT_SIZE = 30
    CENTER_WIDTH = 350
    PINEAPPLE_IMG = 'pineapple.png'
    COCONUT_IMG = 'coconut1.png'
    BACKGROUND_IMG = 'background.png'
    WINNER_IMG = 'like.png'
    ILLEGAL_IMG = 'illegal_move.png'
    COL_START = 31
    FACTOR = 91

    def __init__(self, root, ip, port, server, is_human):
        """
        the game starts with a board (from class Game), creates canvas with
        all the images needed, and starts a communicator object
        :param root: the Tk 'parent' object
        :param ip: servers ip
        :param port: the game port
        :param server: True or False
        """
        self.__board = Game()
        self.__root = root
        self.__is_human = is_human
        self.__coconut_img, self.__pineapple_img, self.__background_img, \
        self.__winner_img, self.__illegal_img = self.create_images()
        self.__col_lst = []  # used for the indicator
        self.__indicator = self.OFF  # a 'switch' for the indicator
        self.__illegal_sign = self.OFF  # counter for illegal move sign
        self.__canvas, self.__title, self.__second_title = self.create_canvas(
            self.__background_img)
        self.__communicator = Communicator(root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)
        self.__is_playing = server
        if self.__is_human == COMPUTER:
            self.__ai = AI()
        self.initialization()

    def initialization(self):
        """
        initials the players. for human player - activates his mouse,
        for ai player - starting to play
        """
        if player_type == COMPUTER and is_server:
            self.play_with_comp()
        if player_type == HUMAN:
            self.__canvas.bind("<Button-1>", self.callback)
            self.__canvas.bind("<Motion>", self.motion)

    def create_images(self):
        """
        creates the images needed for the graphic display
        :return: the images
        """
        coconut_img = tk.PhotoImage(file=self.COCONUT_IMG)
        pineapple_img = tk.PhotoImage(file=self.PINEAPPLE_IMG)
        background_img = tk.PhotoImage(file=self.BACKGROUND_IMG)
        winner_img = tk.PhotoImage(file=self.WINNER_IMG)
        illegal_img = tk.PhotoImage(file=self.ILLEGAL_IMG)
        return coconut_img, pineapple_img, background_img, winner_img, \
               illegal_img

    def create_canvas(self, background_img):
        """
        creates the canvas that will be the graphic game board
        :param background_img: the background image for the canvas
        :return: the canvas, the board title and a secondary title to be
        used later
        """
        canvas = tk.Canvas(self.__root, width=self.CANVAS_WID,
                           height=self.CANVAS_HIGHT, background='white')
        canvas.create_image(self.CENTER_WIDTH, 300, image=background_img,
                            anchor=tk.CENTER)

        if self.__is_human == HUMAN:
            title = canvas.create_text(self.CENTER_WIDTH, 50,
                                       text=self.OPEN_MESSAGE,
                                       font=('', self.WELCOME_FONT_SIZE),
                                       fill='white')
            if is_server:  # server starts the game.his title would be
                # accordingly
                second_title = canvas.create_text(self.CENTER_WIDTH, 100,
                                                  text=self.PLAY, font=(
                        '', self.SECOND_TITLE_FONT_SIZE),
                                                  fill='white')
            else:
                second_title = canvas.create_text(self.CENTER_WIDTH, 150,
                                                  text=self.DONT_PLAY, font=(
                        '', self.SECOND_TITLE_FONT_SIZE),
                                                  fill='white')
            canvas.pack()
            return canvas, title, second_title
        else:
            empty_title = canvas.create_text(350, 100, text='', font=('', 30),
                                             fill='white')
            canvas.pack()
        return canvas, empty_title, empty_title

    def motion(self, event):
        """
        shows the current player what is the column his mouse is pointing on
        :param event: the location of the mouse (x and y coordinates)
        """
        if self.__is_playing:
            self.__col_lst.append(self.get_column(event.x))
            column = self.get_column(event.x)
            if column is None:
                return

            # Checking who is playing:
            player = self.__board.get_current_player()

            if self.__indicator == self.OFF:  # no indicator on screen
                # the screen
                self.put_image_helper(self.INDICATOR_ROW, column,
                                      player, self.INDICATOR)

            self.__indicator = self.ON
            if self.__col_lst[0] == self.__col_lst[-1]:  # first and last
                # item are the same- mouse is still on the same column
                return

            self.delete_img(self.INDICATOR)
            self.__col_lst = []
            self.__indicator = self.OFF

    def delete_img(self, name):
        """
        deleting an image from screen with a given name (tag).
        """
        tag = self.__canvas.find_withtag(name)
        if tag:  # if the image exist on the board at the moment
            self.__canvas.delete(tag)

    def __handle_message(self, column):
        """
        when receiving a message it means that one player had played and
        now it's the second one turn. this function is placing the disc that
        the first player put in his turn on the second's player board. if the
        second player is an ai player- it makes a move.
        :param column: the column the user clicked.
        """
        self.put_image(int(column))

        if self.__is_human == COMPUTER and self.__board.get_winner() is None:
            self.play_with_comp()  # calling to computer to act

    def get_column(self, event_x):
        """
        finds the column that fits the dictionary board coordinates form,
        according to the pixel the user clicked on
        :param event_x: the x-coordinate of the user click
        :return: the column in boards coordinate (int in range(7))
        """

        if event_x in range(self.COL_START, self.COL_START +
                            self.COL_FACTOR):  # range 31,122
            return 0
        elif event_x in range(self.COL_START + self.FACTOR,
                              self.COL_START + 2 * self.FACTOR):
            # range 122,213
            return 1
        elif event_x in range(self.COL_START + 2 * self.FACTOR,
                              self.COL_START + 3 * self.FACTOR):
            # range 213,304
            return 2
        elif event_x in range(self.COL_START + 3 * self.FACTOR,
                              self.COL_START + 4 * self.FACTOR):
            # range 304,395
            return 3
        elif event_x in range(self.COL_START + 4 * self.FACTOR,
                              self.COL_START + 5 * self.FACTOR):
            # range 395,486
            return 4
        elif event_x in range(self.COL_START + 5 * self.FACTOR,
                              self.COL_START + 6 * self.FACTOR):
            # range 486,577
            return 5
        elif event_x in range(self.COL_START + 6 * self.FACTOR,
                              self.COL_START + 7 * self.FACTOR):
            # range 577,668
            return 6
        else:
            return

    def put_image_helper(self, row, column, player, tag):
        """
        puts the user disc in its place according to a given 'row' and
        'column'. gets the current player, to determine which disc should be
        placed there. 'tag' is used for image that we want to remove later on.
        :param row: a given row number
        :param column: a given row number
        :param player: current player
        :param tag: the tag of the image (a string)
        :return:
        """
        if player == Game.PLAYER_ONE:
            self.__canvas.create_image(
                self.COL_0_COORD + column * self.COL_FACTOR,
                self.ROW_0_COORD - (5 - row) * self.ROW_FACTOR,
                image=self.__coconut_img, tag=tag)

        elif player == Game.PLAYER_TWO:
            self.__canvas.create_image(self.COL_0_COORD + column *
                                       self.COL_FACTOR,
                                       self.ROW_0_COORD - (5 - row) *
                                       self.ROW_FACTOR,
                                       image=self.__pineapple_img, tag=tag)

    def put_image(self, column):
        """
        gets the column (integer number in range(7)), and checking if its
        possible to put disc in this column. if it is- it will update
        the Game() object and update the graphic board by calling
        'put_image_helper'. after putting the disc, the is_plying will
        change to True, it means that the other player can play now.
        :param column: the column the user chose.
        :return: True if the disc was added.
        """
        if self.__board.legal_assignment(column):  # if the user move was legal
            player = self.__board.get_current_player()
            row = self.__board.make_move(column)
            self.put_image_helper(row, column, player, self.TAG)
            if self.__is_human == HUMAN:
                self.__canvas.itemconfig(self.__title, text=self.PLAY,
                                         font=('', self.MAIN_TITLE_FONT_SIZE))
                self.__canvas.delete(self.__second_title)

            self.__is_playing = True
            self.get_game_status()  # checks if the game is over or continues
            return True
        else:
            self.__canvas.create_image(self.CENTER_WIDTH, 300,
                                       image=self.__illegal_img,
                                       tag=self.ILLEGAL_TAG)
            self.__canvas.after(self.TIME_OF_ILLEGAL_MOVE, lambda:
                                self.__canvas.delete(self.ILLEGAL_TAG))

    def paint_winner(self):
        """
        checks if there is a winner. if there is- it marks the 4 winning discs
        """
        win_coords = self.__board.get_win_seq()
        for coord in win_coords:
            row = coord[0]
            col = coord[1]
            self.__canvas.create_image(
                self.COL_0_COORD + col * self.COL_FACTOR,
                self.ROW_0_COORD - (5 - row) * self.ROW_FACTOR,
                image=self.__winner_img)

    def callback(self, event):
        """
        when user clicks on the board, the board should update. this
        function will react only if self.__is_playing=True, otherwise,
        clicking on the board will do nothing. its sends a message with the
        column clicked to the other player.
        :param event: x and y coordinates of the user click
        """
        if self.__is_playing:
            # user clicks outside the top border of the board - do nothing
            if event.y < self.OUT_OF_BOARD:
                return
            column = self.get_column(event.x)
            if column is None:
                return

            if self.put_image(column):
                self.delete_img(self.INDICATOR)
                self.__indicator = self.OFF  # no indicator on screen
                self.__canvas.delete(self.__second_title)
                self.__canvas.itemconfig(self.__title, text=self.DONT_PLAY,
                                         font=('', self.MAIN_TITLE_FONT_SIZE))
                # after a player had made a move, disable his mouse
                self.__is_playing = False
                # send message to the other player, so he can play:
                self.__communicator.send_message(column)

            self.get_game_status()  # checks if the game is over or continues

    def get_game_status(self):
        """
        checks if there is a winner, or draw in the game
        """
        if self.__board.get_winner() is not None:  # there is a winner
            self.__canvas.unbind("<Button-1>")  # human can't use their mouse
            self.__canvas.unbind("<Motion>")

            winner = self.__board.get_winner()

            if winner is self.__board.DRAW:
                self.__canvas.itemconfig(self.__title, text=self.TIE_SCORE,
                                         font=('', self.MAIN_TITLE_FONT_SIZE))

            else:
                if (is_server and not winner) or (not is_server and winner):
                    # display to each player if he won or lost the game
                    self.__canvas.itemconfig(self.__title,
                                             text=self.WINNER_MESAGGE,
                                             font=(
                                                 '',
                                                 self.MAIN_TITLE_FONT_SIZE))
                else:
                    self.__canvas.itemconfig(self.__title,
                                             text=self.LOSER_MESSAGE,
                                             font=(
                                                 '',
                                                 self.MAIN_TITLE_FONT_SIZE))
                self.paint_winner()  # displaying the winning discs

    def play_with_comp(self):
        """
        when this function is called, computer is playing. the function 
        determine in what column the computer should put the disc (if its 
        possible), then makes the move, and sends a message to the other
        player with the column the disc was placed in.
        :return: 
        """
        col = self.__ai.find_legal_move(self.__board, self.__board.make_move)
        self.put_comp_image(col)
        # send message to the other player, so he can play:
        self.__communicator.send_message(col)
        self.get_game_status()

    def put_comp_image(self, col):
        """
        checking which disc player should be added to the board, than check
        what is the row that the disc will be placed in, than call
        'put_image_helper' and update the graphic board. (Game() object has
        already updated).
        :param col: an integer (the column that the computer chose).
        :return: 
        """
        # disc is already updated on the board, so we need the opposite
        # player (not current one)
        num_of_discs = self.__board.count_discs()
        if num_of_discs % 2 == 0:
            player = self.__board.PLAYER_TWO
        else:
            player = self.__board.PLAYER_ONE
        row = self.__board.get_comp_row(col)
        self.put_image_helper(row, col, player, self.TAG)
        self.get_game_status()

if __name__ == '__main__':

    parent = tk.Tk()
    if MIN_ARGS <= len(sys.argv) <= MAX_ARGS:
        player_type = sys.argv[PLAYER_LOCATION]
        game_port = int(sys.argv[PORT_LOCATION])

        if not MIN_PORT < game_port < MAX_PORT:
            print(PARAM_ERROR_MESAGGE)

        elif player_type != HUMAN and player_type != COMPUTER:
            print(PARAM_ERROR_MESAGGE)

        else:
            if len(sys.argv) == MIN_ARGS:
                is_server = True
                server_ip = None
                Gui(parent, server_ip, game_port, is_server, player_type)
                parent.title("Server")
                parent.mainloop()

            elif len(sys.argv) == MAX_ARGS:
                is_server = False
                server_ip = sys.argv[IP_LOCATION]
                Gui(parent, server_ip, game_port, is_server, player_type)
                parent.title("Client")
                parent.mainloop()
    else:
        print(PARAM_ERROR_MESAGGE)

