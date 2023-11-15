from GameStatus.Player import Player
from GameStatus.Game import Game
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch

from typing import Type

class MontecarloMachinePlayer(Player):
    def __init__(self, name: str, game: Type['Game'], levelsOfMemory: int, secondsPerMove: float, haveWhites: bool, verbose:bool = False) -> None:
        self._name= name
        self.__lvls= levelsOfMemory
        self.__sec= secondsPerMove
        self.__haveWhites= haveWhites
        self.__engine= MontecarloTreeSearch(None,game,levelsOfMemory,haveWhites,0,1)
        self.__engine.verbosity(verbose)
        self.__engine.setSecPerMove(secondsPerMove)

    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        print(f"Loading move...   [{self.__sec}s]")
        self.__engine= MontecarloTreeSearch(None,gameStatus,self.__lvls,self.__haveWhites,0,1)
        self.__engine.setSecPerMove(self.__sec)
        return self.__engine.move()