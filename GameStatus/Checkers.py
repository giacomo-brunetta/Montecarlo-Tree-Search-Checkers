from GameStatus.Tile import Tile
from GameStatus.Game import Game
from typing import List, Type
from random import randint


class Move:
    def __init__(self, board: Type["Checkers"], eaten: List["Tile"]):
        self.status = board.copy()
        self.eaten = eaten.copy()

    def get_eaten_list(self):
        return self.eaten.copy()

    def get_status(self):
        return self.status

    def count(self):
        return len(self.eaten)

    def count_kings(self):
        kings = 0
        for piece in self.eaten:
            if piece.is_king():
                kings += 1
        return kings

    def __lt__(self, other):
        if other is None:
            return False

        if other is self:
            return False

        if self.count() < other.count():
            return True

        elif self.count() == other.count():
            if self.count_kings() < other.count_kings():
                return True

            else:
                for i in range(self.count()):
                    s = self.eaten[i]
                    o = other.eaten[i]
                    if s.is_king() and o.is_checker():  # a king is encountered before
                        return False
                    elif s.is_checker() and o.is_king():  # a king is encountered later
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

        if self.count() > other.count():
            return True

        elif self.count() == other.count():
            if self.count_kings() > other.count_kings():
                return True

            else:
                for i in range(self.count()):
                    s = self.eaten[i]
                    o = other.eaten[i]
                    if s.is_king() and o.is_checker():  # a king is encountered before
                        return True
                    elif s.is_checker() and o.is_king():  # a king is encountered later
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

        if self.count() != other.count() or self.count_kings() != other.count_kings():
            return False

        for i in range(self.count()):
            s = self.eaten[i]
            o = other.eaten[i]
            if s.is_king() != o.is_king():
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Checkers(Game):
    name = "Checkers"
    minRequiredPlayers = 2
    maxRequiredPlayers = 2
    branchingFactor= 7

    def __init__(self, board=None):
        if board is None:
            self.__board = [[Tile.WHITE_CHECKER] * 4,
                            [Tile.WHITE_CHECKER] * 4,
                            [Tile.WHITE_CHECKER] * 4,
                            [Tile.EMPTY] * 4,
                            [Tile.EMPTY] * 4,
                            [Tile.EMPTY] * 4,
                            [Tile.BLACK_CHECKER] * 4,
                            [Tile.BLACK_CHECKER] * 4,
                            [Tile.BLACK_CHECKER] * 4]
        else:
            self.__board = [line.copy() for line in board]
        self.rows = 8
        self.cols = 8

    def copy(self) -> Type['Checkers']:
        return Checkers(self.__board)

    def in_bounds(self, row: int, col: int) -> bool:
        return row < self.rows and row >= 0 and col < self.cols and col >= 0

    def is_white_turn(self, turn:int):
        return turn % 2 == 0

    def is_settable(self, row: int, col:int):
        return self.in_bounds(row, col) and (row + col) % 2 == 0

    def get(self, row: int, col: int) -> Tile:
        # assert self.in_bounds(row, col), "Index of bounds for board"
        if (row + col) % 2 == 1:
            return Tile.EMPTY

        col_mapped = int((col - (row % 2)) / 2)
        return self.__board[row][col_mapped]

    def set(self, row: int, col: int, piece: Tile):
        assert self.is_settable(row, col), "Cannot set this cell"
        col_mapped = int((col - (row % 2)) / 2)
        self.__board[row][col_mapped] = piece


    def _check_for_upgrade(self, row: int, col: int):
        if row != 0 and row != self.cols - 1:
            return
        piece = self.get(row, col)
        if piece.is_checker():
            if piece.is_white() and row == self.rows-1:
                self.set(row, col, Tile.WHITE_KING)
            if piece.is_black() and row == 0:
                self.set(row, col, Tile.BLACK_KING)

    def __repr__(self) -> str:
        string = ""
        for i in range(self.rows):
            for j in range(self.cols):
                tile = self.get(i, j)
                if tile.is_empty():
                    string += "🟨" if (i+j) % 2 == 0 else "🟩"
                else:
                    string += str(tile)
            string += "\n"
        return string

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        # are the same type
        if type(other) != type(self):
            return False

        # check that every pos is equal
        for i in range(int(self.rows)):
            for j in range(int(self.cols)):
                if self.get(i, j) != other.get(i, j):
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __move_on_or_eat(self, row: int, col: int, piece: Tile):
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

    def __move_piece(self, row: int, col: int) -> List["Move"]:
        assert self.in_bounds(row, col)
        piece = self.get(row, col)
        possible_positions = self.__move_on_or_eat(row, col, piece)
        valid_moves = []
        for pos in possible_positions:
            if self.in_bounds(pos[0], pos[1]) and self.get(pos[0], pos[1]) == Tile.EMPTY:
                board_with_move = self.copy()
                board_with_move.set(row, col, Tile.EMPTY)
                board_with_move.set(pos[0], pos[1], piece)
                board_with_move._check_for_upgrade(pos[0], pos[1])
                valid_moves.append(board_with_move)

        return [Move(move, []) for move in valid_moves]

    def __valid_jump(self, piece: Tile, target: Tile, landing: Tile):
        different_color = (piece.is_white() and target.is_black()) or (piece.is_black() and target.is_white())
        respect_power_of_pieces = piece.is_king() or target.is_checker()
        return different_color and respect_power_of_pieces and landing.is_empty()

    def _jumps(self, row: int, col: int, eaten_before: List["Tile"] = []) -> List["Move"]:
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
                    new_board.set(target_pos[0], target_pos[1], Tile.EMPTY)
                    new_board.set(row, col, Tile.EMPTY)
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

        for row in range(self.rows):
            for col in range(row % 2, self.cols, 2):  # only valid tiles
                piece = self.get(row, col)

                # the piece belong to the player that moves this turn
                if (piece.is_white() and isWhiteTurn) or (piece.is_black() and not isWhiteTurn):
                    # Move is a class that supports comparators so ==, >, max() are overloaded
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

        return [move.get_status() for move in moves]

    def randomMove(self, turn: int) -> Type['Checkers']:
        valid_moves = self.moves(turn)
        if len(valid_moves) == 0:
            return None
        rnd = randint(0, len(valid_moves)-1)
        return valid_moves[rnd]

    def heuristic(self):
        white_score = 0
        black_score = 0
        for row in range(self.rows):
            for col in range(row % 2, self.cols, 2):
                piece = self.get(row,col)
                if piece.is_white():
                    white_score += 2.2 if piece.is_king() else 1
                elif piece.is_black():
                    black_score += 2.2 if piece.is_king() else 1
        return white_score - black_score