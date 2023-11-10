from enum import Enum

class Tile(Enum):
    NONE = 0
    BLACK_PAWN = -1
    BLACK_KING = -2
    WHITE_PAWN = 1
    WHITE_KING = 2

    def is_white(self):
        return self.value > 0

    def is_black(self):
        return self.value < 0

    def is_empty(self):
        return self.value == 0

    def is_king(self):
        return self.value == 2 or self.value == -2

class Board:
    def __init__(self, matrix):
        self.matrix = matrix

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