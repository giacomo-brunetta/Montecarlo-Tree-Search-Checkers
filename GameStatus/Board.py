from GameStatus.Tile import Tile
from GameStatus.Game import Game
from typing import List, Type

class Board(Game):
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

    def __repr__(self) -> str:
        string = ""
        for row in self.__matrix:
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

    def __move_piece(self, row: int, col: int) -> List["Board"]:
        assert self.in_bounds(row, col)
        piece = self.__matrix[row][col]
        possible_positions = self.__move_on_or_eat(row,col,piece)
        valid_moves = []
        for pos in possible_positions:
                if self.in_bounds(pos[0], pos[1]) and self.__matrix[pos[0]][pos[1]] == Tile.EMPTY:
                    board_with_move = Board(self)
                    board_with_move.set(row, col, Tile.EMPTY)
                    board_with_move.set(pos[0], pos[1], piece)
                    valid_moves.append(board_with_move)
        return valid_moves

    def __jumps(self, row: int, col: int, jumps: int = 0):
        assert self.in_bounds(row, col)
        piece = self.__matrix[row][col]
        to_eat = self.__move_on_or_eat(row, col, piece)
        to_land_on = self.__land_on(row, col, piece)

        moves_with_jumps = []
        for i in range(len(to_eat)):
            target_pos = to_eat[i]
            landing_pos = to_land_on[i]
            # both target and landing need to be in bounds. Checking for landing is sufficient
            if self.in_bounds(landing_pos[0], landing_pos[1]):
                # cannot eat same color and landing needs to empty
                target = self.__matrix[target_pos[0]][target_pos[1]]
                landing = self.__matrix[landing_pos[0]][landing_pos[1]]
                if ((piece.is_white() and target.is_black()) or (piece.is_black() and target.is_white())) and landing.is_empty():
                    # create a new board and perform the jump
                    new_board = Board(self)
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

    def moves(self, whiteTurn: bool) -> List["Board"]:
        moves = []
        max_jumps = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 0:
                    piece = self.__matrix[row][col]
                    if (piece.is_white() and whiteTurn) or (piece.is_black() and not whiteTurn):
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

    def randomMove(self) -> Type['Board']:
        return Board()
