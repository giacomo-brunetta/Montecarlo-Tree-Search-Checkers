from abc import ABC, abstractmethod
from typing import List,Type

class Game(ABC):
    name= None
    minRequiredPlayers= None
    maxRequiredPlayers= None
    branchingFactor= None

    def getMinNumPLayers(self):
        assert isinstance(self.minRequiredPlayers,int)
        return self.minRequiredPlayers
    
    def getMaxNumPLayers(self):
        assert isinstance(self.maxRequiredPlayers,int)
        return self.maxRequiredPlayers

    def getBranchingFactor(self) -> int:
        assert isinstance(self.branchingFactor,int)
        return self.branchingFactor

    @abstractmethod
    def moves(self, turn: int) -> List[Type['Game']]:
        pass
    
    @abstractmethod
    def randomMove(self, turn: int) -> Type['Game']:
        pass

    @abstractmethod
    def copy() -> Type['Game']:
        pass