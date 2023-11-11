from enum import Enum

class Tile(Enum):
    EMPTY = 0
    BLACK_CHECKER = -1
    BLACK_KING = -2
    WHITE_CHECKER = 1
    WHITE_KING = 2

    def is_white(self):
        return self.value > 0

    def is_black(self):
        return self.value < 0

    def is_empty(self):
        return self.value == 0

    def is_king(self):
        return self.value == 2 or self.value == -2

    def is_checker(self):
        return self.value == 1 or self.value == -1

    def __repr__(self):
        if self.value == 0:
            return "  "
        if self.value > 0:
            col = "w"
        else:
            col = "b"
        if abs(self.value) == 2:
            type = "K"
        else:
            type = "c"
        return type + col

    def __str__(self):
        return self.__repr__()