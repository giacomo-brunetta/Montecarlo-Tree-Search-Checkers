from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import Type

class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        self._name= name
        self.__boardsPerLevel = 5

    def setBoardsPerLevel(self, bpl: int):
        assert bpl >= 1 and bpl <= 10, f"wrong parameter would cause unreadable output. bpl={bpl}"
        self.__boardsPerLevel = bpl

    def __playerChoice(self, max_num) -> int:
        while True:
            try:
                num = int(input("Pick a move or -1 to surrender: "))
                if num == -1 or (num >= 0 and num < max_num):
                    break
            except:
                print("Error during selection. Insert a valid number")
        return num

    def __showMoves(self,moves) -> None:
        descriptions = []
        levels = []
        for i, mov in enumerate(moves):
            descriptions.append(f"Result of move {i}:")
            levels.append(str(mov).split('\n'))
            if (i+1) % self.__boardsPerLevel == 0 or i==len(moves)-1:
                print("        ".join(descriptions))
                for j in range(len(levels[0])):
                    print("         ".join([row[j] for row in levels]))
                descriptions.clear()
                levels.clear()

    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        print(f"It's {self._name}'s turn. Insert a number to chose one of the following possible next states")
        moves = gameStatus.moves(turn)
        if len(moves)!=0:
            self.__showMoves(moves)
            num = self.__playerChoice(len(moves))
            if num == -1:
                return None
            else:
                return moves[num].copy()
        else:
            return None
