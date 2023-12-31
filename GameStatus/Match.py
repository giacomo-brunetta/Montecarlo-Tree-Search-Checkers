from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import List,Type
from time import time


class Match:
    def __init__(self, players: List[Type['Player']], initialGameStatus: Type['Game']) -> None:
        self.__palayers= players.copy()
        self.__game= initialGameStatus.copy()
        self.__isGameOver= False
        self.__turn= 0
        self.__timesMoves= [[0,0] for i in range(len(players))]

    def move(self, player: Type['Player']) -> None:
        #print(f"match-deb---------------------player {player.name} has this game status\n{self.__game}")
        newGameStatus= player.move(self.__game, self.__turn)
        if newGameStatus is None:
            self.end(player)
        else:
            self.__game= newGameStatus
            print(f"The game status after {player._name} move is:\n{self.__game}")

    def play(self):
        numPlayers= len(self.__palayers)
        assert numPlayers>=self.__game.getMinNumPLayers(), "not enough players for this game"
        assert numPlayers<=self.__game.getMaxNumPLayers(), "too many player for this game"
        while True:
            playerOnMove= self.__palayers[self.__turn%numPlayers]
            start= time()
            self.move(playerOnMove)
            timeUsed= time() - start
            self.__timesMoves[self.__turn%numPlayers][0] += timeUsed
            self.__timesMoves[self.__turn%numPlayers][1] += 1 if timeUsed>0.1 else 0
            print(f"Time spent by {playerOnMove._name} for this move is {round(timeUsed,2)} sec")
            if self.__isGameOver == True:
                for player, t in zip(self.__palayers,self.__timesMoves):
                    print(f"Average time per move spent by {player._name} is {round(t[0]/t[1],2)} sec")
                break
            self.__turn+= 1

    def end(self,player: Type['Player']) -> None:
        print(f"{player} lost. Game over.")
        self.__isGameOver= True