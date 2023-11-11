from GameStatus.Tile import Tile
from typing import List

class Board:
    def __to_tiles(self):
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[0])):
                self.__matrix[i][j] = Tile(self.__matrix[i][j])

    def __init__(self, boardToCopy = None):
        if boardToCopy == None:
            self.__matrix = [
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
            assert isinstance(boardToCopy, Board)
            self.__matrix = [[element for element in line] for line in boardToCopy.__matrix]
        self.rows = len(self.__matrix)
        self.cols = len(self.__matrix[0])

    def get(self, row: int, col: int) -> Tile:
        assert self.in_bounds(row,col), "Index of bounds for board"
        return self.__matrix[row][col]

    def set(self, row: int, col: int , piece: Tile):
        assert self.in_bounds(row, col), "Index of bounds for board"
        self.__matrix[row][col] = piece

    def __repr__(self):
        string = ""
        for row in self.__matrix:
            for tile in row:
                string += str(tile) + " "
            string += "\n"
        return string

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        # are the same type
        if type(other) != type(self):
            return False

        rows = len(self.__matrix)
        cols = len(self.__matrix[0])

        # have the same shape
        if not rows == len(other.__matrix) or not cols == len(other.__matrix[0]):
            return False

        # check that every pos is equal
        for i in range(rows):
            for j in range(cols):
                if self.__matrix[i][j] != other.__matrix[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def in_bounds(self, row: int, col: int) -> bool:
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def move_piece(self, row: int, col: int) -> List["Board"]:
        assert self.in_bounds(row, col)
        piece = self.__matrix[row][col]
        new_rows = []
        if piece.is_checker():
            if piece.is_white():
                new_rows.append(row+1)
            else:
                new_rows.append(row - 1)
        elif piece.is_king():
            new_rows = [row+1, row-1]
        else:
            return []
        valid_moves = []
        for new_row in new_rows:
            for new_col in [col+1, col-1]:
                if self.in_bounds(new_row, new_col) and self.__matrix[new_row][new_col] == Tile.EMPTY:
                    board_with_move = Board(self)
                    board_with_move.set(row, col, Tile.EMPTY)
                    board_with_move.set(new_row, new_col, piece)
                    valid_moves.append(board_with_move)
        return valid_moves

    def jump_with_piece(self, row: int, col: int) -> List["Board"]:
        assert self.in_bounds(row, col)
        piece = self.__matrix[row][col]
        to_eat = []
        to_land_on = []

        if piece.is_checker():
            if piece.is_white():
                to_eat.extend([(row+1, col + 1), (row+1, col - 1)])
                to_land_on.extend([(row+2, col+2), (row+2, col - 2)])
            else:
                to_eat.extend([(row-1, col + 1), (row-1, col - 1)])
                to_land_on.extend([(row - 2, col + 2), (row - 2, col - 2)])
        elif piece.is_king():
            to_eat.extend([(row + 1, col + 1), (row + 1, col - 1), (row-1, col + 1), (row-1, col - 1)])
            to_eat.extend([(row - 2, col + 2), (row - 2, col - 2), (row-1, col + 1), (row-1, col - 1)])
        else:
            return []
        valid_moves = []
        for i in range(len(to_eat)):
            target_pos = to_eat[i]
            landing_pos = to_land_on[i]
            # both target and landing need to be in bounds. Checking for landing is sufficient
            if self.in_bounds(landing_pos[0], landing_pos[1]):
                # cannot eat same color and landing needs to empty
                target = self.__matrix[target_pos[0]][target_pos[1]]
                landing = self.__matrix[landing_pos[0]][landing_pos[1]]
                if ((piece.is_white() and target.is_black()) or (piece.is_black() and target.is_white())) and landing.is_empty():
                    new_board = Board(self)
                    new_board.set(target_pos[0], target_pos[1], Tile.EMPTY)
                    new_board.set(row, col, Tile.EMPTY)
                    new_board.set(landing_pos[0], landing_pos[1], piece)
                    valid_moves.append(new_board)
                    # TODO recursive call for multiple jumps
        return valid_moves

    def moves(self, whiteTurn: bool) -> List["Board"]:
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    piece = self.__matrix[row][col]
                    if (piece.is_white() and whiteTurn) or (piece.is_black() and not whiteTurn):
                        moves.extend(self.move_piece(row, col))
                        moves.extend(self.jump_with_piece(row, col))
        return moves
