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


if __name__ == '__main__':
    unittest.main()