import unittest
from GameStatus.Board import Board as Board
from GameStatus.Tile import Tile as Tile
from GameStatus.Node import Node as Node
from GameStatus.MontecarloTreeSearch import MontecarloTreeSearch as MontecarloTreeSearch


class TestBoard(unittest.TestCase):
    def test_equal(self):
        b = Board()
        b1 = Board()

        self.assertEqual(b, b)  # equal to self
        self.assertEqual(b, b1)  # equal to identical
        self.assertEqual(b1, b)

        b1.matrix[0][0] = Tile(2)

        # different from different board
        self.assertNotEqual(b, b1)
        self.assertNotEqual(b1, b)

        # different from other types

        self.assertNotEqual(0, b)
        self.assertNotEqual(b, 0)
        self.assertNotEqual(b, "ciao")
        self.assertNotEqual((), b)
    

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
        root9= Node(Board())
        root10= Node(Board())
        
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


    def testNewChild(self):
        node= Node("string value")
        with self.assertRaises(Exception):
            node.newChild("string")


    def testGetChildren(self):
        node0= Node(11)
        node0.newChild(Node(12))
        node0.newChild(Node(13))
        for child, expectedValue in zip(node0.getChildren(),[12,13]):
            self.assertEqual(child.getValue(),expectedValue)
        node1= Node("11")
        node1.newChild(Node("12"))
        node1.newChild(Node("13"))
        for child, expectedValue in zip(node1.getChildren(),["12","13"]):
            self.assertEqual(child.getValue(),expectedValue)
        self.assertTrue(len(Node(0).getChildren()) == 0)



class TestMontecarloTreeSearch(unittest.TestCase):
    def tes(self):
        pass

    def testInBounds(self):
        b = Board()
        self.assertTrue(b.in_bounds(0, 0))
        self.assertTrue(b.in_bounds(7, 7))
        self.assertFalse(b.in_bounds(-1, 0))
        self.assertFalse(b.in_bounds(7, -1))
        self.assertFalse(b.in_bounds(8, 0))
        self.assertFalse(b.in_bounds(0, 8))

    def testInit(self):
        b = Board()
        b.matrix[0][0] = Tile.BLACK_KING
        b1 = Board()
        b2 = Board(b)

        self.assertEqual(b, b2)
        self.assertNotEqual(b, b1)

    def testMoves(self):
        b = Board()
        self.assertEqual(len(b.moves(whiteTurn=True)), 7)
        self.assertEqual(len(b.moves(whiteTurn=False)), 7)


if __name__ == '__main__':
    unittest.main()