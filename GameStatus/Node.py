from typing import List, Type

class Node:
    def __init__(self, obj):
        assert obj is not None, "error in Node construction"
        self.__value = obj
        self.__children = []

    def newChild(self, node: Type['Node']) -> None:
        assert isinstance(node, Node), "expected Node element as leaf in the tree"
        self.__children.append(node)
    
    def getValue(self):
        return self.__value

    def getChildren(self) -> List[Type['Node']]:
        return self.__children

    def __str__(self) -> str:
        assert hasattr(self.__value,"__str__"), "expected printable elment"
        assert type(str(self.__value)) is str, "str() metod doese't return a string"
        return str(self.__value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other,Node) == False:
            return False
        return self.__value == other.getValue()