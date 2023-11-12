from GameStatus.Tile import Tile
from GameStatus.Game import Game
from typing import List, Type
from random import randint


class JumpMove:
    def __init__(self, board: Type["Checkers"], eaten: List["Tile"]):
        self.board = board.copy()
        self.eaten = eaten.copy()

    def get_eaten_list(self):
        return self.eaten.copy()

    def count(self):
        return len(self.eaten)

    def count_kings(self):
        kings = 0
        for piece in self.eaten:
            if piece.is_king():
                kings += 1
        return kings

    def __lt__(self, other):
        assert type(other) == JumpMove

        if self.count() < other.count() or self.count_kings() < other.count_kings():
            return True

        for i in range(self.count()):
            s = self.eaten[i]
            o = other.eaten[i]
            if s.is_king() and o.is_checker():
                return False
            elif s.is_checker() and o.is_king():
                return True

        return False

    def __le__(self, other):
        return not self.__gt__(other)

    def __gt__(self, other):
        assert type(other) == JumpMove

        if self.count() > other.count() or self.count_kings() > other.count_kings():
            return True

        for i in range(self.count()):
            s = self.eaten[i]
            o = other.eaten[i]
            if s.is_king() and o.is_checker():
                return True
            elif s.is_checker() and o.is_king():
                return False

        return False

    def __ge__(self, other):
        return not self.__le__(other)

    def __eq__(self, other):
        if type(other) != JumpMove:
            return False

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

    def __init__(self):
        self._board = [
            [Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY],
            [Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER],
            [Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY, Tile.WHITE_CHECKER, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER],
            [Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY],
            [Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER, Tile.EMPTY, Tile.BLACK_CHECKER]
        ]
        self.rows = len(self._board)
        self.cols = len(self._board[0])

    def copy(self) -> Type['Checkers']:
        checkers_copy = Checkers()
        checkers_copy._board = [[element for element in line] for line in self._board]
        return checkers_copy

    def is_white_turn(self, turn:int):
        return turn % 2 == 1

    def is_settable(self, row:int, col:int):
        return self.in_bounds(row, col) and (row + col) % 2 == 0

    def get(self, row: int, col: int) -> Tile:
        assert self.in_bounds(row,col), "Index of bounds for board"
        return self._board[row][col]

    def set(self, row: int, col: int, piece: Tile):
        assert self.is_settable(row, col), "Cannot set this cell"
        self._board[row][col] = piece

    def __repr__(self) -> str:
        string = ""
        for row in self._board:
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

        rows = len(self._board)
        cols = len(self._board[0])

        # have the same shape
        if not rows == len(other._board) or not cols == len(other._board[0]):
            return False

        # check that every pos is equal
        for i in range(rows):
            for j in range(cols):
                if self._board[i][j] != other._board[i][j]:
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

    def __move_piece(self, row: int, col: int) -> List["Checkers"]:
        assert self.in_bounds(row, col)
        piece = self._board[row][col]
        possible_positions = self.__move_on_or_eat(row, col, piece)
        valid_moves = []
        for pos in possible_positions:
                if self.in_bounds(pos[0], pos[1]) and self._board[pos[0]][pos[1]] == Tile.EMPTY:
                    board_with_move = self.copy()
                    board_with_move.set(row, col, Tile.EMPTY)
                    board_with_move.set(pos[0], pos[1], piece)
                    valid_moves.append(board_with_move)
        return valid_moves

    def __valid_jump(self, piece: Tile, target: Tile, landing: Tile):
        different_color = (piece.is_white() and target.is_black()) or (piece.is_black() and target.is_white())
        respect_power_of_pieces = (piece.is_king() or target.is_checker())
        return different_color and respect_power_of_pieces and landing.is_empty()

    def __jumps(self, row: int, col: int, jumps: int = 0):
        assert self.in_bounds(row, col)
        piece = self._board[row][col]
        to_eat = self.__move_on_or_eat(row, col, piece)
        to_land_on = self.__land_on(row, col, piece)

        moves_with_jumps = []

        for i in range(len(to_eat)):
            target_pos = to_eat[i]
            landing_pos = to_land_on[i]

            # both target and landing need to be in bounds. Checking for landing is sufficient
            if self.in_bounds(landing_pos[0], landing_pos[1]):
                # cannot eat same color and landing needs to empty
                target = self._board[target_pos[0]][target_pos[1]]
                landing = self._board[landing_pos[0]][landing_pos[1]]

                if self.__valid_jump(piece, target, landing):

                    # create a new board and perform the jump
                    new_board = self.copy()
                    new_board.set(target_pos[0], target_pos[1], Tile.EMPTY)
                    new_board.set(row, col, Tile.EMPTY)
                    new_board.set(landing_pos[0], landing_pos[1], piece)

                    # call jump recursively
                    further_jumps = new_board.__jumps(landing_pos[0], landing_pos[1], jumps=jumps+1)

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
                if self.is_settable(row, col):
                    piece = self._board[row][col]

                    # the piece belong to the player that moves this turn
                    if (piece.is_white() and isWhiteTurn) or (piece.is_black() and not isWhiteTurn):

                        # eval jump moves
                        jump_moves = self.__jumps(row, col)
                        if len(jump_moves) > 0:
                            current_jumps = jump_moves[0][1]
                            if current_jumps > max_jumps:
                                max_jumps = current_jumps
                                moves.clear()
                            if current_jumps >= max_jumps:
                                for move in jump_moves:
                                    moves.append(move[0])

                        # if no jumps are available, eval symple moves
                        if max_jumps == 0:
                            moves.extend(self.__move_piece(row, col))

        return moves

    def randomMove(self, turn: int) -> Type['Checkers']:
        valid_moves = self.moves(turn)
        if len(valid_moves) == 0:
            return None
        rnd = randint(0, len(valid_moves)-1)
        return valid_moves[rnd]