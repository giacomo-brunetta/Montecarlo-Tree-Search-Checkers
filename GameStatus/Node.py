from typing import List, Type

class Node:
    def __init__(self, obj, fatherReference: Type['Node']= None):
        self.__father= fatherReference
        self.__value = obj
        self.__children = []

    def newChild(self, node: Type['Node']) -> None:
        assert isinstance(node, Node), "expected Node element as leaf in the tree"
        #assert node.getFather() != None, "node child must point to the parent, cannot be None"
        assert node.getFather() == self, "to be inserted between childs the node must reference the father"
        self.__children.append(node)
    
    def getValue(self):
        return self.__value

    def getChildren(self) -> List[Type['Node']]:
        return self.__children
    
    def setFather(self, node: Type['Node']) -> None:
        self.__father= node

    def getFather(self) -> Type['Node']:
        return self.__father

    def __str__(self) -> str:
        assert hasattr(self.__value,"__str__"), "expected printable elment"
        assert type(self.__value) is str, "str() metod doese't return a string"
        return str(self.__value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other,Node) == False:
            return False
        return self.__value == other.getValue()