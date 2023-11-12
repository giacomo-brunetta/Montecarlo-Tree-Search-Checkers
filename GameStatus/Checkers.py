from GameStatus.Tile import Tile
from GameStatus.Game import Game
from typing import List, Type
from random import randint

class Checkers(Game):
    def __to_tiles(self):
        for i in range(len(self.__board)):
            for j in range(len(self.__board[0])):
                self.__board[i][j] = Tile(self.__board[i][j])

    def __init__(self, checkersToCopy = None):
        if checkersToCopy == None:
            self.__board = [
                [1, 0, 1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, -1, 0, -1, 0, -1, 0, -1],
                [-1, 0, -1, 0, -1, 0, -1, 0],
                [0, -1, 0, -1, 0, -1, 0, -1]
            ]
            self.__to_tiles()
        else:
            assert isinstance(checkersToCopy, Checkers)
            self.__board = [[element for element in line] for line in checkersToCopy.__board]
        self.rows = len(self.__board)
        self.cols = len(self.__board[0])


    def is_white_turn(self, turn:int):
        return turn % 2 == 0

    def is_settable(self, row:int, col:int):
        return self.in_bounds(row, col) and (row + col) % 2 == 0

    def get(self, row: int, col: int) -> Tile:
        assert self.in_bounds(row,col), "Index of bounds for board"
        return self.__board[row][col]

    def set(self, row: int, col: int, piece: Tile):
        assert self.is_settable(row, col), "Cannot set this cell"
        self.__board[row][col] = piece

    def __repr__(self) -> str:
        string = ""
        for row in self.__board:
            for tile in row:
                string += str(tile) + " "
            string += "\n"
        return string

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        # are the same type
        if type(other) != type(self):
            return False

        rows = len(self.__board)
        cols = len(self.__board[0])

        # have the same shape
        if not rows == len(other.__board) or not cols == len(other.__board[0]):
            return False

        # check that every pos is equal
        for i in range(rows):
            for j in range(cols):
                if self.__board[i][j] != other.__board[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def in_bounds(self, row: int, col: int) -> bool:
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def __move_on_or_eat(self,row: int, col: int, piece: Tile):
        assert self.in_bounds(row, col)
        if piece.is_checker():
            if piece.is_white():
                return [(row + 1, col + 1), (row + 1, col - 1)]
            elif piece.is_black():
                return [(row - 1, col + 1), (row - 1, col - 1)]
        elif piece.is_king():
            return [(row + 1, col + 1), (row + 1, col - 1), (row-1, col + 1), (row-1, col - 1)]
        else:
            return []

    def __land_on(self, row: int, col: int, piece: Tile):
        assert self.in_bounds(row, col)
        if piece.is_checker():
            if piece.is_white():
                return [(row+2, col+2), (row+2, col - 2)]
            elif piece.is_black():
                return [(row - 2, col + 2), (row - 2, col - 2)]
        elif piece.is_king():
            return [(row + 2, col + 2), (row + 2, col - 2), (row-2, col + 2), (row-2, col - 2)]
        else:
            return []

    def _place(self, row: int, col: int, piece: Tile):
        if row == 0 and piece.is_black():
            self.set(row, col, Tile.BLACK_KING)

        elif row == self.rows - 1 and piece.is_white():
            self.set(row, col, Tile.WHITE_KING)

        else:
            self.set(row, col, piece)

    def __move_piece(self, row: int, col: int) -> List["Checkers"]:
        assert self.in_bounds(row, col)
        piece = self.__board[row][col]
        possible_positions = self.__move_on_or_eat(row, col, piece)
        valid_moves = []

        for pos in possible_positions:
            if self.in_bounds(pos[0], pos[1]) and self.__board[pos[0]][pos[1]] == Tile.EMPTY:
                board_with_move = Checkers(self)
                board_with_move.set(row, col, Tile.EMPTY)
                board_with_move._place(pos[0], pos[1], piece)
                valid_moves.append(board_with_move)

        return valid_moves

    def __jumps(self, row: int, col: int, jumps: int = 0):
        assert self.in_bounds(row, col)
        piece = self.__board[row][col]
        to_eat = self.__move_on_or_eat(row, col, piece)
        to_land_on = self.__land_on(row, col, piece)

        moves_with_jumps = []
        for i in range(len(to_eat)):
            target_pos = to_eat[i]
            landing_pos = to_land_on[i]
            # both target and landing need to be in bounds. Checking for landing is sufficient
            if self.in_bounds(landing_pos[0], landing_pos[1]):
                # cannot eat same color and landing needs to empty
                target = self.__board[target_pos[0]][target_pos[1]]
                landing = self.__board[landing_pos[0]][landing_pos[1]]

                # can only eat a piece of opposite color with equal or inferior value
                if (((piece.is_white() and target.is_black()) or (piece.is_black() and target.is_white())) and
                        landing.is_empty() and (piece.is_king() or target.is_checker())):

                    # create a new board and perform the jump
                    new_board = Checkers(self)
                    new_board.set(target_pos[0], target_pos[1], Tile.EMPTY)
                    new_board.set(row, col, Tile.EMPTY)
                    new_board.set(landing_pos[0], landing_pos[1], piece) # place the piece in the landing position

                    # call jump recursively
                    further_jumps = new_board.__jumps(landing_pos[0], landing_pos[1], jumps=jumps+1)

                    # in case of pawn evaluate the upgrade only after the recursive calls
                    if piece.is_checker():
                        new_board._place(landing_pos[0], landing_pos[1], piece)

                    # add all the possible sequences of jumps
                    if len(further_jumps) > 0:
                        moves_with_jumps.extend(further_jumps)
                    else:
                        moves_with_jumps.append((new_board, jumps+1))

        # keep only the boards with the biggest amount of jumps
        max_jumps = 0
        for move in moves_with_jumps:
            max_jumps = max(max_jumps, move[1])
        valid_moves = []
        for move in moves_with_jumps:
            if move[1] == max_jumps:
                valid_moves.append(move)
        return valid_moves

    def moves(self, turn: int) -> List["Checkers"]:
        isWhiteTurn = self.is_white_turn(turn)
        moves = []
        max_jumps = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    piece = self.__board[row][col]
                    if (piece.is_white() and isWhiteTurn) or (piece.is_black() and not isWhiteTurn):
                        jump_moves = self.__jumps(row, col)
                        if len(jump_moves) > 0:
                            current_jumps = jump_moves[0][1]
                            if current_jumps > max_jumps:
                                max_jumps = current_jumps
                                moves.clear()
                            if current_jumps >= max_jumps:
                                for move in jump_moves:
                                    moves.append(move[0])
                        if max_jumps == 0:
                            moves.extend(self.__move_piece(row, col))
        return moves

    def randomMove(self, turn: int) -> Type['Checkers']:
        valid_moves = self.moves(turn)
        if len(valid_moves) == 0:
            return None
        rnd = randint(0, len(valid_moves)-1)
        return valid_moves[rnd]


