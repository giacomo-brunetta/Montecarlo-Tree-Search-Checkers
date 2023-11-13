# Montecarlo Tree Search for Board Games

## Goal of the project

The goal of the project is to have a game engine that supports potentially any game with 1 to N players.
The players can be:
- Human players: provided with a CLI interface that allows them to play
- BOTs: that play autonomously

## The algorithm

![MCTS](https://i.stack.imgur.com/GR7qf.png)

To create game-agnostic BOTs we chose to implement [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search): a search algorithm that performs a sparse visit of the state space by performing random layouts.

### Pros: 
- it is context agnostic
- it does not require any heuristic
- it is an anytime method
- it is highly parallelizable

### Cons:
- it is not exact

## The supported game(s)
![Italian Draughts](https://img.freepik.com/premium-vector/checkers-chess-board-white-black-chips-placed-board-ancient-intellectual-board-game-illustration_255498-39.jpg)

To date, we only support [Italian Draughts](https://en.wikipedia.org/wiki/Italian_draughts), a game very similar to checkers.
We chose it because it is not trivial like Tick Tac Toe or Connect 4, but it has a reasonable branching factor compared to Chess or GO.

## The architecture
![Class diagram](https://github.com/giacomo-brunetta/Montecarlo-Tree-Search-Checkers/assets/102242995/e9b24470-883b-4e90-ae5a-2d2c7086a23d)

## Contributors
- __Brunetta Giacomo__ Github: _@giacomo-brunetta_ e-mail: giacomo.brunetta@mail.polimi.it
- GitHub: _@g7240_



