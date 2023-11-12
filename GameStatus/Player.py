from abc import ABC, abstractmethod
from typing import Type
from GameStatus.Game import Game

class Player(ABC):
    name= None
    
    @abstractmethod
    def move(self, gameStatus: Type['Game']) -> Type['Game']:
        pass