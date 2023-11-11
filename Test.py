import unittest
from GameStatus.Board import Board as Board
from GameStatus.Board import Tile as Tile


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