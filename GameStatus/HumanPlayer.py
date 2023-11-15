from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import Type

class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        self._name= name
        self.__boards_per_level = 5

    def setBoardsPerLevel(self, bpl: int):
        self.__boards_per_level = bpl

    def __playerChoice(self, max_num):
        while True:
            try:
                num = int(input("Pick a move or -1 to surrender:"))
                if num == -1:
                    return None
                if num == 0 or (num > 0 and num < max_num):
                    break
            except:
                print("Error during selection. Insert a valid number")
        return num

    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        print(f"It's {self._name}'s turn. Insert a number to chose one of the following possible next states")
        moves = gameStatus.moves(turn)

        descriptions = []
        levels = []

        if moves is not None:
            for i, mov in enumerate(moves):
                descriptions.append(f"Result of move {i}:")
                levels.append(str(mov).split('\n'))
                if i % self.__boards_per_level == 0:
                    print("          ".join(descriptions))
                    for j in range(len(levels[0])):
                        print("         ".join([row[j] for row in levels]))
                    descriptions.clear()
                    levels.clear()

            num = self.__playerChoice(len(moves))
            return moves[num].copy()
        else:
            return None
