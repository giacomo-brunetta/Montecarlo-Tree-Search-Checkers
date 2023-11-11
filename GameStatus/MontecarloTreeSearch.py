from GameStatus.Node import Node as Node

class MontecarloTreeSearch(Node):
    def __init__(self, obj):
        super().__init__(obj)
        self.__wons= 0
        self.__losses= 0
        self.__stalemate= 0
        self.__probability= 0

