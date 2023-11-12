from abc import ABC, abstractmethod
from typing import List,Type

class Game(ABC):
    @abstractmethod
    def moves(self, turn: int) -> List[Type['Game']]:
        pass
    
    @abstractmethod
    def randomMove(self, turn: int) -> Type['Game']:
        pass

    @abstractmethod
    def copy() -> Type['Game']:
        pass