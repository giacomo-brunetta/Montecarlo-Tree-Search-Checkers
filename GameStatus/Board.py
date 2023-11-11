from GameStatus.Tile import Tile

class Board:
    def __to_tiles(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[i][j] = Tile(self.matrix[i][j])

    def __init__(self, boardToCopy = None):
        if boardToCopy == None:
            self.matrix = [
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
            self.matrix = [[element for element in line] for line in boardToCopy.matrix]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def __repr__(self):
        string = ""
        for row in self.matrix:
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

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # have the same shape
        if not rows == len(other.matrix) or not cols == len(other.matrix[0]):
            return False

        # check that every pos is equal
        for i in range(rows):
            for j in range(cols):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def in_bounds(self, row, col):
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def move_piece(self, row, col, piece):
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
                if self.in_bounds(new_row, new_col) and self.matrix[new_row][new_col] == Tile.NONE:
                    board_with_move = Board(self)
                    board_with_move.matrix[row][col] = Tile.NONE
                    board_with_move.matrix[new_row][new_col] = piece
                    valid_moves.append(board_with_move)
        return valid_moves

    def eat_piece(self, row, col, piece):
        print("gnammmm")

    def moves(self, whiteTurn):
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if piece.is_white() == whiteTurn:
                    moves.extend(self.move_piece(row, col, piece))
        return moves
