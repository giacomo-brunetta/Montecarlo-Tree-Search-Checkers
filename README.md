# Montecarlo Tree Search applied to italian Checkers game
The progect compose of a:
- testing class tu run tests
- an abstract class for Game
- a class for the checkers board
- a class for pawns and kings
- and a montecarlo tree searc class, whitch extend the node class, and implment simulation on the board to probabilistically understend which is the best moove

The montecarlo tree search class can be used for every game with the following prerequisite:
- ajust the setting of random engine to provide a sufficient number of mooves compared to the size of the game; the bigger it is, more simulation are necessary to have a precise result;
- implement a Game instnce that implements transitions to the all next possible states (gameObj.moves()) and one that return only one of those possible (gameObj.randomMove()). Those two function must retun respectivelly a list of new possible Game states and one single Game state.
