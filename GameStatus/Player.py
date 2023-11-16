from abc import ABC, abstractmethod
from typing import Type
from GameStatus.Game import Game

class Player(ABC):
    _name= None
    
    @abstractmethod
    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        pass

    def __str__(self):
        return str(self._name)