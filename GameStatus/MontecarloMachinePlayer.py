from GameStatus.Player import Player
from GameStatus.Game import Game
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch

from typing import Type

class MontecarloMachinePlayer(Player):
    def __init__(self, name: str, game: Type['Game'], levelsOfMemory: int, seconsPerMove: float, haveWhites: bool) -> None:
        self.__name= name
        self.__lvls= levelsOfMemory
        self.__sec= seconsPerMove
        self.__haveWhites= haveWhites
        self.__engine= MontecarloTreeSearch(game,levelsOfMemory,haveWhites,0,1)
        self.__engine.setSecPerMove(seconsPerMove)

    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        self.__engine= MontecarloTreeSearch(gameStatus,self.__lvls,self.__haveWhites,0,1)
        self.__engine.setSecPerMove(self.__sec)
        return self.__engine.move()