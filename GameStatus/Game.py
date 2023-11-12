from abc import ABC, abstractmethod
from typing import List,Type

class Game(ABC):
    @abstractmethod
    def moves() -> List[Type['Game']]:
        pass
    
    @abstractmethod
    def randomMove() -> Type['Game']:
        pass