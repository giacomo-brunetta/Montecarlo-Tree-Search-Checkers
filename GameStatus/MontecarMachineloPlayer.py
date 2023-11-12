from GameStatus.Player import Player
from GameStatus.Game import Game
from GameStatus.Checkers import Checkers
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch

from typing import Type

class MontecarMachineloPlayer(Player):
    def __init__(self, name: str, game: Type['Game'], levelsOfMemory: int, seconsPerMove: float, haveWhites: bool) -> None:
        self.name= name
        self.engine= MontecarloTreeSearch(game,levelsOfMemory,haveWhites,0,1)
        self.engine.setSecPerMove(seconsPerMove)

    def move(self, gameStatus: Type['Game']) -> Type['Game']:
        return self.engine.move()