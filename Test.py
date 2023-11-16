import unittest
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.Tile import Tile as Tile
from GameStatus.Node import Node as Node
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch as MontecarloTreeSearch


class TestBoard(unittest.TestCase):
    def test_equal(self):
        b = Checkers()
        b1 = Checkers()

        self.assertEqual(b, b)  # equal to self
        self.assertEqual(b, b1)  # equal to identical
        self.assertEqual(b1, b)

        b1.set(0, 0, Tile(2))

        # different from different board
        self.assertNotEqual(b, b1)
        self.assertNotEqual(b1, b)

        # different from other types

        self.assertNotEqual(0, b)
        self.assertNotEqual(b, 0)
        self.assertNotEqual(b, "ciao")
        self.assertNotEqual((), b)

    def testInit(self):
        b = Checkers()
        b1 = Checkers()

        self.assertEqual(b,b1)

        b.set(0, 0, Tile.BLACK_KING)
        self.assertNotEqual(b, b1)
    
    def testCopy(self):
        b0 = Checkers()
        b0.set(0, 0, Tile.WHITE_CHECKER)
        b1 = b0.copy()
        b2= b0.copy()
        self.assertTrue(b0 is not b1)
        self.assertEqual(b0, b1)
        self.assertTrue(b0 is not b2)
        self.assertEqual(b0, b2)


    def testInBounds(self):
        b = Checkers()
        self.assertTrue(b.in_bounds(0, 0))
        self.assertTrue(b.in_bounds(7, 7))
        self.assertFalse(b.in_bounds(-1, 0))
        self.assertFalse(b.in_bounds(7, -1))
        self.assertFalse(b.in_bounds(8, 0))
        self.assertFalse(b.in_bounds(0, 8))

    def testMoves(self):
        b = Checkers()
        self.assertEqual(len(b.moves(0)), 7)
        self.assertEqual(len(b.moves(1)), 7)

        b.set(3, 1, Tile.BLACK_CHECKER)
        b.set(3, 3, Tile.BLACK_CHECKER)
        b.set(5, 1, Tile.EMPTY)
        b.set(5, 3, Tile.EMPTY)

        self.assertEqual(len(b.moves(0)), 4)


        for row in range(6,b.rows):
            for col in range(b.cols):
                if b.is_settable(row,col):
                    b.set(row,col, Tile.EMPTY)

        self.assertEqual(len(b.moves(0)), 4)

        for row in range(b.rows):
            for col in range(b.cols):
                if b.is_settable(row, col):
                    b.set(row, col, Tile.EMPTY)

        b.set(4, 4, Tile.WHITE_KING)
        b.set(3, 3, Tile.BLACK_KING)
        b.set(1, 1, Tile.BLACK_KING)
        b.set(5, 5, Tile.BLACK_KING)

        self.assertEqual(len(b.moves(0)), 1)

        b.set(5, 3, Tile.BLACK_KING)

        self.assertEqual(len(b.moves(0)), 1)

        b.set(5, 1, Tile.BLACK_KING)

        self.assertEqual(len(b.moves(0)), 2)

        b.set(5, 1, Tile.BLACK_CHECKER)
        self.assertEqual(len(b.moves(0)), 1)

    def testImSpeed(self):
        b = Checkers()
        for i in range(1000):
            moves = b.randomMove(i)
            if moves is None:
                b = Checkers()
            b = b.moves(i)[0]

class TestNode(unittest.TestCase):
    def testGetValue(self):
        self.assertEqual(Node("string").getValue(), "string") 
        self.assertEqual(Node([1,'2',3]).getValue(), [1,'2',3]) 

    def testEqual(self):
        root0= Node(None)
        root1= Node(None)
        root2= Node(2)
        root3= Node(2)
        root4= Node(4)
        root5= Node("string")
        root6= Node("string")
        root7= Node([0,1,2])
        root8= Node([0,1,2])
        root9= Node(Checkers())
        root10= Node(Checkers())
        
        self.assertEqual(root0, root0)  # equal to self
        self.assertEqual(root0, root1)  # empty node equal to identical
        self.assertEqual(root2, root3)  # integer node equal to identical
        self.assertEqual(root5, root6)  # string node equal to identical
        self.assertEqual(root7, root8)  # list node equal to identical
        self.assertEqual(root9, root10)  # board node equal to identical

        self.assertNotEqual(root0, root2) # empty node is different from numerical node
        self.assertNotEqual(root3, root4) # int node different from different int node
        self.assertNotEqual(root4, root5) # int different from string node
        self.assertNotEqual(root4, root9) # int node different from board node
        self.assertNotEqual(root7, root9) # list node different from board node
    
    def testStr(self):
        root0= Node(None)
        root2= Node(2)
        root5= Node("string")
        root7= Node([0,1,2])
        #test __str__
        self.assertEqual(str(root0), "None") 
        self.assertEqual(str(root2), "2")
        self.assertEqual(repr(root2), "2")
        self.assertEqual(str(root5), "string")
        self.assertEqual(repr(root5), "string")
        self.assertEqual(str(root7), "[0, 1, 2]")
        self.assertEqual(repr(root7), "[0, 1, 2]")
        #test exeption
        class ErroneusPrintableObj():
            def __init__(self):
                self.atribute=5    
            def __str__(self):
                return 44
        node11= Node(ErroneusPrintableObj())
        with self.assertRaises(Exception):
            str(node11)

    def testFatherReference(self):
        root= Node(5,None)
        child0= Node(4,root)
        child1= Node(4,root)
        self.assertEqual(child0.getFather(),root)
        self.assertEqual(child0.getFather(),child1.getFather())
        self.assertNotEqual(child1.getFather(),None)
        falseChild= Node(3,child0)
        with self.assertRaises(Exception):
            root.newChild(falseChild)

    def testNewChild(self):
        node= Node("string value")
        with self.assertRaises(Exception):
            node.newChild("string")

    def testGetChildren(self):
        node0= Node(11)
        node0.newChild(Node(12,node0))
        node0.newChild(Node(13,node0))
        for child, expectedValue in zip(node0.getChildren(),[12,13]):
            self.assertEqual(child.getValue(),expectedValue)
        node1= Node("11")
        node1.newChild(Node("12",node1))
        node1.newChild(Node("13",node1))
        for child, expectedValue in zip(node1.getChildren(),["12","13"]):
            self.assertEqual(child.getValue(),expectedValue)
        self.assertTrue(len(Node(0).getChildren()) == 0)


class TestMontecarloTreeSearch(unittest.TestCase):
    def tes(self):
        #root= MontecarloTreeSearch(Board(),False,0,1)
        #child= MontecarloTreeSearch(Board().randomMove(),True,0,None)
        pass


if __name__ == '__main__':
    unittest.main()