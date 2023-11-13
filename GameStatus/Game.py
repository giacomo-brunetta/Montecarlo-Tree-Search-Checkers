from abc import ABC, abstractmethod
from typing import List,Type

class Game(ABC):
    name= None
    minRequiredPlayers= None
    maxRequiredPlayers= None

    def getMinNumPLayers(self):
        return self.minRequiredPlayers
    
    def getMaxNumPLayers(self):
        return self.maxRequiredPlayers

    @abstractmethod
    def moves(self, turn: int) -> List[Type['Game']]:
        pass
    
    @abstractmethod
    def randomMove(self, turn: int) -> Type['Game']:
        pass

    @abstractmethod
    def copy() -> Type['Game']:
        pass