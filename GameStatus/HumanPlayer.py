from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import Type

class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        self.name= name

    def move(self, gameStatus: Type['Game']) -> Type['Game']:
        print(f"Dr. {self.name} is your turn. This is the game status")
        print(gameStatus)
        print("Insert a number to chose one of the following possible next states")
        moves= gameStatus.moves()
        if moves != None:
            for i, mov in enumerate(moves):
                print(f"Result of move numer {i}:")
                print(mov)
            while True:
                try:
                    num= int(input("Pick a move:"))
                except:
                    print("Error during selection. Insert a valid number")
                if num==0 or (num>0 and num<len(moves)):
                    break
            return moves[num].copy()
        else:
            return None
