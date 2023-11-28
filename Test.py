import unittest
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.Node import Node as Node

EMPTY = 0
BLACK_CHECKER = -1
BLACK_KING = -2
WHITE_CHECKER = 1
WHITE_KING = 2

class TestBoard(unittest.TestCase):
    def test_equal(self):
        b = Checkers()
        b1 = Checkers()

        self.assertEqual(b, b)  # equal to self
        self.assertEqual(b, b1)  # equal to identical
        self.assertEqual(b1, b)

        b1.set(0, 0, 2)

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

        b.set(0, 0, BLACK_KING)
        self.assertNotEqual(b, b1)
    
    def testCopy(self):
        b0 = Checkers()
        b0.set(0, 0, WHITE_CHECKER)
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

        b.set(3, 1, BLACK_CHECKER)
        b.set(3, 3, BLACK_CHECKER)
        b.set(5, 1, EMPTY)
        b.set(5, 3, EMPTY)

        self.assertEqual(len(b.moves(0)), 4)

        for row in range(5,b.rows):
            for col in range(b.cols):
                if b.is_settable(row,col):
                    b.set(row,col, EMPTY)

        self.assertEqual(len(b.moves(0)), 4)

        for row in range(b.rows):
            for col in range(b.cols):
                if b.is_settable(row, col):
                    b.set(row, col, EMPTY)

        b.set(4, 4, WHITE_KING)
        b.set(3, 3, BLACK_KING)
        b.set(1, 1, BLACK_KING)
        b.set(5, 5, BLACK_KING)

        self.assertEqual(len(b.moves(0)), 1)

        b.set(5, 3, BLACK_KING)

        self.assertEqual(len(b.moves(0)), 1)

        b.set(5, 1, BLACK_KING)

        self.assertEqual(len(b.moves(0)), 2)

        b.set(5, 1, BLACK_CHECKER)
        self.assertEqual(len(b.moves(0)), 1)

    def testMoves2(self):
        b = Checkers()

        for r in range(b.rows):
            for c in range(b.cols):
                b.set(r,c, EMPTY)

        b.set(5,3,BLACK_CHECKER)
        b.set(5,5,BLACK_CHECKER)
        b.set(4,4,WHITE_CHECKER)
        print(b)

        for move in b.moves(1):
            print(move)

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
        root2= Node(2)
        root3= Node(2)
        root4= Node(4)
        root5= Node("string")
        root6= Node("string")
        root7= Node([0,1,2])
        root8= Node([0,1,2])
        root9= Node(Checkers())
        root10= Node(Checkers())
        
        self.assertEqual(root2, root2)  # equal to self
        self.assertEqual(root2, root3)  # integer node equal to identical
        self.assertEqual(root5, root6)  # string node equal to identical
        self.assertEqual(root7, root8)  # list node equal to identical
        self.assertEqual(root9, root10)  # board node equal to identical

        self.assertNotEqual(root3, root4) # int node different from different int node
        self.assertNotEqual(root4, root5) # int different from string node
        self.assertNotEqual(root4, root9) # int node different from board node
        self.assertNotEqual(root7, root9) # list node different from board node
    
    def testStr(self):
        root2= Node(2)
        root5= Node("string")
        root7= Node([0,1,2])
        #test __str__
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
        #root= MontecarloTreeSearch(Board(),False,0,1)
        #child= MontecarloTreeSearch(Board().randomMove(),True,0,None)
        pass


if __name__ == '__main__':
    unittest.main()