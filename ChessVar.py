# Author: Mike Neguse
# GitHub Username: MN724
# Date: 8/8/23
# Description: Program contains a chess board class and chess piece classes that are used to represent a modified game
# of chess where players alternate turns trying to get their king piece to row 8 on the board. Pieecs move as they do
# in regular chess, but the starting position is modified and players are not allowed to leave their king in check or
# place the other player's king in check.

class ChessVar:
    """Class represents a game of chess.
        Data members for each chess piece, a dictionary of chess piece objects and their positions, a list representing
        the board, the game state, the turn, and a flag for the final move of the game"""
    def __init__(self):
        """"""
        self._black_king = King('h1', 'black')
        self._black_rook = Rook('h2', 'black')
        self._black_bishop_1 = Bishop('g1', 'black')
        self._black_bishop_2 = Bishop('g2', 'black')
        self._black_knight_1 = Knight('f1', 'black')
        self._black_knight_2 = Knight('f2', 'black')
        self._white_king = King('a1', 'white')
        self._white_rook = Rook('a2', 'white')
        self._white_bishop_1 = Bishop('b1', 'white')
        self._white_bishop_2 = Bishop('b2', 'white')
        self._white_knight_1 = Knight('c1', 'white')
        self._white_knight_2 = Knight('c2', 'white')
        self._pos_dict = {
            self._black_king: self._black_king.get_pos(),
            self._black_rook: self._black_rook.get_pos(),
            self._black_bishop_1: self._black_bishop_1.get_pos(),
            self._black_bishop_2: self._black_bishop_2.get_pos(),
            self._black_knight_1: self._black_knight_1.get_pos(),
            self._black_knight_2: self._black_knight_2.get_pos(),
            self._white_king: self._white_king.get_pos(),
            self._white_rook: self._white_rook.get_pos(),
            self._white_bishop_1: self._white_bishop_1.get_pos(),
            self._white_bishop_2: self._white_bishop_2.get_pos(),
            self._white_knight_1: self._white_knight_1.get_pos(),
            self._white_knight_2: self._white_knight_2.get_pos(),
        }
        self._board = [
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 8'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 7'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 6'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 5'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 4'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', ' 3'],
            ['WR', 'WB', 'WN', '  ', '  ', 'BN', 'BB', 'BR', ' 2'],
            ['WK', 'WB', 'WN', '  ', '  ', 'BK', 'BB', 'BK', ' 1'],
            [' a', ' b', ' c', ' d', ' e', ' f', ' g', ' h', '  ']
        ]
        self._game_state = 'UNFINISHED'
        self._turn = 'white'
        self._white_turn_exception = 0

    def get_game_state(self):
        """Returns the current state of the game as 'UNFINISHED', 'BLACK_WON', 'WHITE_WON', or 'TIE'"""
        return self._game_state

    def set_game_state(self):
        """Sets the current state of the game to 'UNFINISHED', 'BLACK_WON', 'WHITE_WON', or 'TIE'"""
        for piece_obj in self._pos_dict:
            if piece_obj.get_type() == 'King':
                if self._pos_dict[piece_obj][1] == '8':
                    if piece_obj.get_color() == 'white':
                        self._white_turn_exception += 1
                        if self._white_turn_exception == 1:
                            self._game_state = 'UNFINISHED'
                            return
                        elif self._white_turn_exception == 2:
                            self._game_state = 'WHITE_WINS'
                            return
                    else:
                        if self._white_turn_exception == 1:
                            self._game_state = 'TIE'
                            return
                        else:
                            self._game_state = 'BLACK_WINS'
                            return

    def make_move(self, move_from, move_to):
        """Makes a piece move from the move_from position to the move_to position"""
        if self.get_game_state() != 'UNFINISHED':
            return False
        move = self.check_legal_move(move_from, move_to)
        if move is False:
            return False
        loops = 0
        for piece_obj_1 in self._pos_dict:
            if self._pos_dict[piece_obj_1] == move_from:
                if piece_obj_1.get_color() != self.check_turn():
                    return False
                move = self.check_path(piece_obj_1, move_from, move_to)
                if move is False:
                    return False
                move = self.is_check(move_from, move_to)
                if move is True:
                    return False
                for piece_obj_2 in self._pos_dict:
                    if self._pos_dict[piece_obj_2] == move_to:
                        if piece_obj_2.get_color() == self.check_turn():
                            return False
                        piece_obj_2.is_captured()
                move = piece_obj_1.move(move_to)
                if move is False:
                    return False
                break
            loops += 1
        if loops == 12:
            return False
        self.update_board()
        self.change_turn()
        self.set_game_state()
        return True

    def check_path(self, piece_obj, move_from, move_to):
        """Checks the path of a moving piece for any other pieces in between the starting and ending location"""
        converted_move_from = self.convert_pos(move_from)
        converted_move_to = self.convert_pos(move_to)
        from_col = converted_move_from[0]
        from_row = converted_move_from[1]
        to_col = converted_move_to[0]
        to_row = converted_move_to[1]

        if to_col > from_col:
            col_inc = 1
        elif to_col < from_col:
            col_inc = -1
        else:
            col_inc = 0

        if to_row > from_row:
            row_inc = 1
        elif to_row < from_row:
            row_inc = -1
        else:
            row_inc = 0

        from_row += row_inc
        from_col += col_inc

        if piece_obj.get_type() == 'Bishop' or piece_obj.get_type() == 'Rook':
            while from_row != to_row or from_col != to_col:
                for piece_obj_2 in self._pos_dict:
                    converted_dest = self.convert_pos(self._pos_dict[piece_obj_2])
                    if converted_dest is False:
                        converted_dest_col = ' '
                        converted_dest_row = ' '
                    else:
                        converted_dest_col = converted_dest[0]
                        converted_dest_row = converted_dest[1]
                    if from_col == converted_dest_col and from_row == converted_dest_row:
                        return False
                from_row += row_inc
                from_col += col_inc
            return
        else:
            return

    def check_legal_move(self, move_from, move_to):
        """Checks if the move_from and move_to positions provided by the user are on the board"""
        converted_move_from = self.convert_pos(move_from)
        if converted_move_from is False:
            return False

        converted_move_to = self.convert_pos(move_to)
        if converted_move_to is False:
            return False

    def change_turn(self):
        """Changes the current turn from 'black' to 'white' or 'white' to 'black'"""
        if self._turn == 'white':
            self._turn = 'black'
        else:
            self._turn = 'white'

    def check_turn(self):
        """Returns the current turn as either 'white' or 'black'"""
        return self._turn

    def is_check(self, move_from, move_to):
        """Checks to see if the currently queued move from the move_from position to the move_to position will result
        in a check for either king"""
        for piece_obj in self._pos_dict:
            if self._pos_dict[piece_obj] == move_from:
                moving_obj = piece_obj
                self._pos_dict[moving_obj] = move_to
                moving_obj.set_pos_temp(move_to)
                break

        for king_obj in self._pos_dict:
            if king_obj.get_type() == 'King':
                king_color = king_obj.get_color()
                king_pos = self._pos_dict[king_obj]

                for piece_obj in self._pos_dict:
                    if piece_obj.get_type() != 'King' and piece_obj.get_color() != king_color:
                        if piece_obj.get_pos() != '  ':
                            legal_move = piece_obj.check_legal_move(king_pos)
                        else:
                            legal_move = False
                        if legal_move is not False:
                            path = self.check_path(piece_obj, self._pos_dict[piece_obj], king_pos)
                            if path is not False:
                                self._pos_dict[moving_obj] = move_from
                                moving_obj.set_pos_temp(move_from)
                                return True
                            else:
                                self._pos_dict[moving_obj] = move_from
                                moving_obj.set_pos_temp(move_from)
                                return

        self._pos_dict[moving_obj] = move_from
        moving_obj.set_pos_temp(move_from)




        # Check if other team's pieces can move to king space

    def show_board(self):
        """Prints out the current game board"""
        for row in self._board:
            print(row)
        return

    def update_board(self):
        """Updates the game board to reflect the current positions of all of the game pieces"""
        self.update_pos_dict()
        row_num = 0
        while row_num < 8:
            row = self._board[row_num]
            index = 0
            while index < 8:
                row[index] = '  '
                index += 1
            row_num += 1
        for piece in self._pos_dict:
            if self._pos_dict[piece] != '  ':
                converted_pos = self.convert_pos(self._pos_dict[piece])
                piece_color = piece.get_color()
                if piece_color == 'white':
                    piece_letters = 'W'
                else:
                    piece_letters = 'B'
                piece_type = piece.get_type()
                if piece_type == 'King':
                    piece_letters += 'K'
                elif piece_type == 'Rook':
                    piece_letters += 'R'
                elif piece_type == 'Bishop':
                    piece_letters += 'B'
                elif piece_type == 'Knight':
                    piece_letters += 'N'

                self._board[converted_pos[1]][converted_pos[0]] = piece_letters

    def update_pos_dict(self):
        """Updates the dictionary containing all the piece objects as keys and piece positions as values"""
        self._pos_dict = {
            self._black_king: self._black_king.get_pos(),
            self._black_rook: self._black_rook.get_pos(),
            self._black_bishop_1: self._black_bishop_1.get_pos(),
            self._black_bishop_2: self._black_bishop_2.get_pos(),
            self._black_knight_1: self._black_knight_1.get_pos(),
            self._black_knight_2: self._black_knight_2.get_pos(),
            self._white_king: self._white_king.get_pos(),
            self._white_rook: self._white_rook.get_pos(),
            self._white_bishop_1: self._white_bishop_1.get_pos(),
            self._white_bishop_2: self._white_bishop_2.get_pos(),
            self._white_knight_1: self._white_knight_1.get_pos(),
            self._white_knight_2: self._white_knight_2.get_pos(),
        }

    def convert_pos(self, pos):
        """Converts the algebraic position to the row and column positions in the game board list"""
        col = pos[0]
        if pos[1] == ' ':
            row = ' '
        else:
            row = int(pos[1])

        if col == 'a':
            col = 0
        elif col == 'b':
            col = 1
        elif col == 'c':
            col = 2
        elif col == 'd':
            col = 3
        elif col == 'e':
            col = 4
        elif col == 'f':
            col = 5
        elif col == 'g':
            col = 6
        elif col == 'h':
            col = 7
        else:
            return False

        if row == 1:
            row = 7
        elif row == 2:
            row = 6
        elif row == 3:
            row = 5
        elif row == 4:
            row = 4
        elif row == 5:
            row = 3
        elif row == 6:
            row = 2
        elif row == 7:
            row = 1
        elif row == 8:
            row = 0
        else:
            return False

        return [col, row]


class ChessPiece:
    """Represents a generic chess piece
        Data members include piece position and color
        Methods to update the position, return the color, return the position, capture the piece, and convert the
        algebraic position to the row and column"""
    def __init__(self, pos, color):
        self._pos = pos
        self._color = color

    def move(self, move_to):
        """Sets the position of the chess piece to the move_to position"""
        self._pos = move_to
        return

    def get_color(self):
        """Returns the color of the chess piece"""
        return self._color

    def get_pos(self):
        """Returns the position of the chess piece"""
        return self._pos

    def set_pos_temp(self, pos):
        """Sets the position of the chess piece
            Only used to temporarily set the position in order to simulate a movement"""
        self._pos = pos

    def is_captured(self):
        """Clears the position of the chess piece to signify that it has been captured"""
        self._pos = '  '

    def convert_pos(self, move_from, move_to):
        """Converts the algebraic position to just the row and column of the board"""
        move_from_row = int(move_from[1])
        move_to_row = int(move_to[1])
        move_from_col = move_from[0]
        move_to_col = move_to[0]

        if move_from_col == 'a':
            move_from_col = 1
        elif move_from_col == 'b':
            move_from_col = 2
        elif move_from_col == 'c':
            move_from_col = 3
        elif move_from_col == 'd':
            move_from_col = 4
        elif move_from_col == 'e':
            move_from_col = 5
        elif move_from_col == 'f':
            move_from_col = 6
        elif move_from_col == 'g':
            move_from_col = 7
        elif move_from_col == 'h':
            move_from_col = 8

        if move_to_col == 'a':
            move_to_col = 1
        elif move_to_col == 'b':
            move_to_col = 2
        elif move_to_col == 'c':
            move_to_col = 3
        elif move_to_col == 'd':
            move_to_col = 4
        elif move_to_col == 'e':
            move_to_col = 5
        elif move_to_col == 'f':
            move_to_col = 6
        elif move_to_col == 'g':
            move_to_col = 7
        elif move_to_col == 'h':
            move_to_col = 8

        return [move_from_col, move_from_row, move_to_col, move_to_row]


class King(ChessPiece):
    """Class represents a king piece
        Contains the current location of the piece and checks if a move is legal
        Communicates with the ChessVar class to receive move information"""

    def __init__(self, pos, color):
        super().__init__(pos, color)
        self._type = 'King'

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def move(self, move_to):
        """Move method checks if movement is legal and then updates position appropriately"""
        if self.check_legal_move(move_to) is False:
            return False
        return super().move(move_to)

    def check_legal_move(self, move_to):
        """Checks if the move_to position is legal for this type of chess piece"""
        move_from = super().get_pos()
        if move_from == move_to:
            return False
        converted_pos_list = super().convert_pos(move_from, move_to)
        move_from_col = converted_pos_list[0]
        move_from_row = converted_pos_list[1]
        move_to_col = converted_pos_list[2]
        move_to_row = converted_pos_list[3]

        if abs(move_to_col - move_from_col) > 1 or abs(move_to_row - move_from_row) > 1:
            return False
        else:
            return True

    def get_pos(self):
        """Returns the current position of the piece
            To be used by the ChessVar class object as needed to retrieve positions on the board"""
        return super().get_pos()


class Rook(ChessPiece):
    """Class represents a rook piece
        Contains the current location of the piece and checks if a move is legal
        Communicates with the ChessVar class to receive move information"""

    def __init__(self, pos, color):
        super().__init__(pos, color)
        self._type = 'Rook'

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def move(self, move_to):
        """Move method checks if movement is legal and then updates position appropriately"""
        if self.check_legal_move(move_to) is False:
            return False
        return super().move(move_to)

    def check_legal_move(self, move_to):
        """Checks if the move_to position is legal for this type of chess piece"""
        move_from = super().get_pos()
        if move_from == move_to:
            return False
        converted_pos_list = super().convert_pos(move_from, move_to)
        move_from_col = converted_pos_list[0]
        move_from_row = converted_pos_list[1]
        move_to_col = converted_pos_list[2]
        move_to_row = converted_pos_list[3]

        if abs(move_to_col - move_from_col) != 0 and abs(move_to_row - move_from_row) != 0:
            return False
        else:
            return True

    def get_pos(self):
        """Returns the current position of the piece
            To be used by the ChessVar class object as needed to retrieve positions on the board"""
        return super().get_pos()


class Bishop(ChessPiece):
    """Class represents a bishop piece
        Contains the current location of the piece and checks if a move is legal
        Communicates with the ChessVar class to receive move information"""

    def __init__(self, pos, color):
        super().__init__(pos, color)
        self._type = 'Bishop'

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def move(self, move_to):
        """Move method checks if movement is legal and then updates position appropriately"""
        if self.check_legal_move(move_to) is False:
            return False
        return super().move(move_to)

    def check_legal_move(self, move_to):
        """"""
        move_from = super().get_pos()
        if move_from == move_to:
            return False
        converted_pos_list = super().convert_pos(move_from, move_to)
        move_from_col = converted_pos_list[0]
        move_from_row = converted_pos_list[1]
        move_to_col = converted_pos_list[2]
        move_to_row = converted_pos_list[3]

        if abs(move_to_col - move_from_col) != abs(move_to_row - move_from_row):
            return False
        else:
            return True


class Knight(ChessPiece):
    """Class represents a knight piece
        Contains the current location of the piece and checks if a move is legal
        Communicates with the ChessVar class to receive move information"""

    def __init__(self, pos, color):
        super().__init__(pos, color)
        self._type = 'Knight'

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def move(self, move_to):
        """Move method checks if movement is legal and then updates position appropriately"""
        if self.check_legal_move(move_to) is False:
            return False
        return super().move(move_to)

    def check_legal_move(self, move_to):
        """Checks if the move_to position is legal for this type of chess piece"""
        move_from = super().get_pos()
        if move_from == move_to:
            return False
        converted_pos_list = super().convert_pos(move_from, move_to)
        move_from_col = converted_pos_list[0]
        move_from_row = converted_pos_list[1]
        move_to_col = converted_pos_list[2]
        move_to_row = converted_pos_list[3]

        if (abs(move_to_col - move_from_col) != 2 or abs(move_to_row - move_from_row) != 1) and\
                (abs(move_to_col - move_from_col) != 1 or abs(move_to_row - move_from_row) != 2):
            return False
        else:
            return True


game = ChessVar()
game.show_board()