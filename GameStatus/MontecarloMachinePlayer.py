from GameStatus.Player import Player
from GameStatus.Game import Game
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch

from typing import Type

class MontecarloMachinePlayer(Player):
    def __init__(self, name: str, levelsOfMemory: int, secondsPerMove: float, numPlayers: int, verbose:bool = False) -> None:
        self._name= name
        self.__lvls= levelsOfMemory
        self.__sec= secondsPerMove
        self.__numPlayers= numPlayers
        self.__verbosity= verbose

    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        print(f"Loading {self._name}'s {turn} turn move...   [wait at least {self.__sec}s]")
        engine= MontecarloTreeSearch(None,gameStatus,self.__lvls,self.__numPlayers,0,turn,1)
        engine.verbosity(self.__verbosity)
        engine.setSecPerMove(self.__sec)
        return engine.move(turn)