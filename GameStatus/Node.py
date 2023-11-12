class Node:
    def __init__(self, obj):
        self.__value = obj
        self.__children = []

    def newChild(self, node):
        assert isinstance(node, Node), "expected Node element as leaf in the tree"
        self.__children.append(node)
    
    def getValue(self):
        return self.__value

    def getChildren(self):
        return self.__children

    def __str__(self):
        assert hasattr(self.__value,"__str__"), "expected printable elment"
        assert isinstance(str(self.__value),str), "str() metod doese't return a string"
        return str(self.__value)

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other,Node) == False:
            return False
        return self.__value == other.getValue()