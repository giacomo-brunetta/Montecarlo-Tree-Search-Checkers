import random

from GameStatus.Game import Game
from typing import List, Type

# TILES
EMPTY = 0
BLACK_CHECKER = -1
BLACK_KING = -2
WHITE_CHECKER = 1
WHITE_KING = 2


def is_white(piece: int):
    return piece > 0


def is_black(piece: int):
    return piece < 0


def is_empty(piece: int):
    return piece == 0


def is_king(piece: int):
    return piece == 2 or piece == -2


def is_checker(piece: int):
    return piece == 1 or piece == -1


class Move:
    def __init__(self, board: Type["Checkers"], eaten: List[int]):
        self.status = board.copy()
        self.eaten = eaten.copy()
        self.count = len(self.eaten)
        self.kings = 0
        for piece in self.eaten:
            if is_king(piece):
                self.kings += 1

    def __lt__(self, other):
        if other is None:
            return False

        if other is self:
            return False

        if self.count < other.count:
            return True

        elif self.count == other.count:
            if self.kings < other.kings:
                return True

            else:
                for s, o in zip(self.eaten, other.eaten):
                    if is_king(s) and is_checker(o):  # a king is encountered before
                        return False
                    elif is_checker(s) and is_king(o):  # a king is encountered later
                        return True
                return False  # they are the same
        else:
            return False  # self is more than other

    def __le__(self, other):
        return not self.__gt__(other)

    def __gt__(self, other):
        if other is None:
            return True

        if other is self:
            return False

        if self.count > other.count:
            return True

        elif self.count == other.count:
            if self.kings > other.kings:
                return True

            else:
                for s, o in zip(self.eaten, other.eaten):
                    if is_king(s) and is_checker(o):  # a king is encountered before
                        return True
                    elif is_checker(s) and is_king(o):  # a king is encountered later
                        return False
                return False  # they are the same
        else:
            return False  # self is less than other

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if other is None:
            return False

        if other is self:
            return True

        if self.count != other.count or self.kings != other.kings:
            return False

        for s, o in zip(self.eaten, other.eaten):
            if is_king(s) != is_king(o):
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Checkers(Game):
    name = "Checkers"
    minRequiredPlayers = 2
    maxRequiredPlayers = 2
    branchingFactor = 7

    # CLASS BUILDERS
    def __init__(self, board=None):
        if board is None:
            self.__board = {}
            for i in range(12):
                self.__board[i] = WHITE_CHECKER
                self.__board[i+20] = BLACK_CHECKER
        else:
            self.__board = board.copy()
        self.rows = 8
        self.cols = 8

    def copy(self) -> Type['Checkers']:
        return Checkers(self.__board)

    def is_white_turn(self, turn:int):
        return turn % 2 == 0

    # CHECK POSITION
    def in_bounds(self, row: int, col: int) -> bool:
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def is_settable(self, row: int, col: int):
        return self.in_bounds(row, col) and (row + col) % 2 == 0

    # GETTERS and SETTERS
    def get(self, row: int, col: int) -> int:
        # assert self.in_bounds(row, col), "Index of bounds for board"
        if (row + col) % 2 == 1:
            return EMPTY
        col_mapped = int((col - (row % 2)) / 2)
        pos = row * 4 + col_mapped

        return self.__board[pos] if pos in self.__board else EMPTY

    def set(self, row: int, col: int, piece: int):
        # assert self.is_settable(row, col), "Cannot set this cell"
        col_mapped = int((col - (row % 2)) / 2)
        pos = row * 4 + col_mapped

        if piece == EMPTY and pos in self.__board:
            self.__board.pop(pos)
        else:
            self.__board[pos] = piece

    # VIEW
    def __repr__(self) -> str:
        unicode = {
            -1: "⚪",
            -2: "🤍",
            1: "⚫",
            2: "🖤"
        }
        string = ""
        for i in range(self.rows):
            for j in range(self.cols):
                tile = self.get(i, j)
                if is_empty(tile):
                    string += "🟨" if (i+j) % 2 == 0 else "🟩"
                else:
                    string += unicode[tile]
            string += "\n"
        return string

    def __str__(self) -> str:
        return self.__repr__()

    # COMPARATORS
    def __eq__(self, other) -> bool:
        # are the same type
        if other is self:
            return True

        if type(other) != type(self):
            return False

        # check that every pos is equal
        for row in range(self.rows):
            for col in range(row % 2, self.cols, 2):
                if self.get(row, col) != other.get(row, col):
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    # METHODS FOR EVALUATING MOVES
    def _check_for_upgrade(self, row: int, col: int):
        if row != 0 and row != self.cols - 1:
            return
        piece = self.get(row, col)
        if is_checker(piece):
            if is_white(piece) and row == self.rows-1:
                self.set(row, col, WHITE_KING)
            if is_black(piece) and row == 0:
                self.set(row, col, BLACK_KING)

    def __move_on_or_eat(self, row: int, col: int, piece: int):
        # assert self.in_bounds(row, col)
        if is_checker(piece):
            if is_white(piece):
                return [(row + 1, col + 1), (row + 1, col - 1)]
            elif is_black(piece):
                return [(row - 1, col + 1), (row - 1, col - 1)]
        elif is_king(piece):
            return [(row + 1, col + 1), (row + 1, col - 1), (row-1, col + 1), (row-1, col - 1)]
        else:
            return []

    def __land_on(self, row: int, col: int, piece: int):
        # assert self.in_bounds(row, col)
        if is_checker(piece):
            if is_white(piece):
                return [(row+2, col+2), (row+2, col - 2)]
            elif is_black(piece):
                return [(row - 2, col + 2), (row - 2, col - 2)]
        elif is_king(piece):
            return [(row + 2, col + 2), (row + 2, col - 2), (row-2, col + 2), (row-2, col - 2)]
        else:
            return []

    def __move_piece(self, row: int, col: int) -> List["Move"]:
        # assert self.in_bounds(row, col)
        piece = self.get(row, col)
        possible_positions = self.__move_on_or_eat(row, col, piece)
        valid_moves = []
        for pos in possible_positions:
            if self.in_bounds(pos[0], pos[1]) and is_empty(self.get(pos[0], pos[1])):
                board_with_move = self.copy()
                board_with_move.set(row, col, EMPTY)
                board_with_move.set(pos[0], pos[1], piece)
                board_with_move._check_for_upgrade(pos[0], pos[1])
                valid_moves.append(board_with_move)

        return [Move(move, []) for move in valid_moves]

    def __valid_jump(self, piece: int, target: int, landing: int):
        different_color = (is_white(piece) and is_black(target)) or (is_black(piece) and is_white(target))
        respect_power_of_pieces = is_king(piece) or is_checker(target)
        return different_color and respect_power_of_pieces and is_empty(landing)

    def _jumps(self, row: int, col: int, eaten_before: List["int"] = []) -> List["Move"]:
        piece = self.get(row, col)
        to_eat = self.__move_on_or_eat(row, col, piece)
        to_land_on = self.__land_on(row, col, piece)

        moves_with_jumps = []

        for i in range(len(to_eat)):
            target_pos = to_eat[i]
            landing_pos = to_land_on[i]

            # both target and landing need to be in bounds. Checking for landing is sufficient
            if self.in_bounds(landing_pos[0], landing_pos[1]):

                target = self.get(target_pos[0], target_pos[1])
                landing = self.get(landing_pos[0], landing_pos[1])

                # cannot eat same color and landing needs to empty
                if self.__valid_jump(piece, target, landing):

                    # create a new board and perform the jump
                    new_board = self.copy()
                    new_board.set(target_pos[0], target_pos[1], EMPTY)
                    new_board.set(row, col, EMPTY)
                    new_board.set(landing_pos[0], landing_pos[1], piece)

                    # call jump recursively
                    further_jumps = new_board._jumps(landing_pos[0], landing_pos[1], eaten_before + [target])

                    # the upgrade to king is done only after the recursive call
                    new_board._check_for_upgrade(landing_pos[0], landing_pos[1])

                    # add all the possible sequences of jumps
                    if len(further_jumps) == 0:
                        moves_with_jumps.append(Move(new_board, eaten_before + [target]))
                    else:
                        moves_with_jumps += further_jumps

        return moves_with_jumps

    def moves(self, turn: int) -> List["Checkers"]:
        isWhiteTurn = self.is_white_turn(turn)
        moves = []
        max_jump = None

        for pos, piece in self.__board.items():
            # the piece belong to the player that moves this turn
            if (isWhiteTurn and is_white(piece)) or (not isWhiteTurn and is_black(piece)):
                # Move is a class that supports comparators so ==, >, max() are overloaded
                row = pos // 4
                col = (pos % 4) * 2 + (row % 2)
                jump_moves = self._jumps(row, col)  # eval jump moves.

                if len(jump_moves) > 0:
                    # if new best is found clear list and update the best
                    temp_max = max(jump_moves)
                    if temp_max > max_jump:
                        max_jump = temp_max
                        moves.clear()

                    # append only the best moves
                    for move in jump_moves:
                        if move == max_jump:
                            moves.append(move)

                # if no jumps are available, eval simple moves
                elif max_jump is None:
                    moves += self.__move_piece(row, col)

        return [move.status for move in moves]

    def randomMove(self, turn: int) -> Type['Checkers']:
        moves = self.moves(turn)
        if len(moves) == 0:
            return None
        else:
            return random.choice(moves)
