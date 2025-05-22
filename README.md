# Montecarlo Tree Search for Board Games

## Goal of the project

The goal of the project is to have a game engine that supports potentially any game with 1 to N players.
The players can be:
- Human players: provided with a CLI interface that allows them to play
- BOTs: autonomous entities that can compete against humans or other bots

## The algorithm

![MCTS](https://i.stack.imgur.com/GR7qf.png)

To create game-agnostic BOTs we chose to implement [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search): a search algorithm that performs a sparse visit of the state space by performing random playouts. The move that lead to the highest probability of winning is chosen as the best.

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
![Class Diagram](https://github.com/giacomo-brunetta/Montecarlo-Tree-Search-Checkers/assets/102242995/37302bca-89d2-44c7-976c-fba34e000145)



## Contributors
- __Brunetta Giacomo__ Github: _@giacomo-brunetta_ e-mail: giacomo.brunetta@mail.polimi.it
- __Bellini Gabriele__ GitHub: [_@g7240_](https://github.com/g7240)



