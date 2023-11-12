from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import List,Type


class Match:
    def __init__(self, players: List[Type['Player']], initialGameStatus: Type['Game']) -> None:
        self.__palayers= players.copy()
        self.__game= initialGameStatus.copy()
        self.__isGameOver= False

    def move(self, player: Type['Player']) -> None:
        newGameStatus= player.move(self.__game)
        if newGameStatus == None:
            self.end()
        else:
            self.__game= newGameStatus

    def play(self):
        numPlayers= len(self.__palayers)
        assert numPlayers>=2
        i=0
        while True:
            playerOnMove= self.__palayers[i%numPlayers]
            self.move(playerOnMove)
            i+= 1
            if self.__isGameOver == True:
                break

    def end(self) -> None:
        self.__isGameOver= True