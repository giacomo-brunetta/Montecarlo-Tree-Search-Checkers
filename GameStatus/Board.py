from GameStatus.Tile import Tile

class Board:
    def __to_tiles(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[i][j] = Tile(self.matrix[i][j])

    def __init__(self):
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
