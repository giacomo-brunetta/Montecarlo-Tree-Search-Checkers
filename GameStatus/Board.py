from GameStatus.Tile import Tile

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

    def get(self, row, col):
        assert self.in_bounds(row,col), "Index of bounds for board"
        return self.__matrix[row][col]

    def set(self, row, col, piece):
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

    def in_bounds(self, row, col):
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def move_piece(self, row, col):
        piece = self.__matrix[row][col]
        new_rows = []
        if piece.is_pawn():
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
                if self.in_bounds(new_row, new_col) and self.__matrix[new_row][new_col] == Tile.NONE:
                    board_with_move = Board(self)
                    board_with_move.set(row, col, Tile.NONE)
                    board_with_move.set(new_row, new_col, piece)
                    valid_moves.append(board_with_move)
        return valid_moves

    def eat_piece(self, row, col, piece):
        print("gnammmm")

    def moves(self, whiteTurn):
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    piece = self.__matrix[row][col]
                    if (piece.is_white() and whiteTurn) or (piece.is_black() and not whiteTurn):
                        moves.extend(self.move_piece(row, col))
        return moves
