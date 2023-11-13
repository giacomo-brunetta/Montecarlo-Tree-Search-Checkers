from GameStatus.Player import Player
from GameStatus.Game import Game

from typing import List,Type


class Match:
    def __init__(self, players: List[Type['Player']], initialGameStatus: Type['Game']) -> None:
        self.__palayers= players.copy()
        self.__game= initialGameStatus.copy()
        self.__isGameOver= False
        self.__turn= 0

    def move(self, player: Type['Player']) -> None:
        #print(f"match-deb---------------------player {player.name} has this game status\n{self.__game}")
        newGameStatus= player.move(self.__game, self.__turn)
        if newGameStatus == None:
            self.end()
        else:
            self.__game= newGameStatus
            print(f"Tew game status after {player.name} move is:\n{self.__game}")

    def play(self):
        numPlayers= len(self.__palayers)
        assert numPlayers>=self.__game.getMinNumPLayers(), "not enought player for this game"
        assert numPlayers<=self.__game.getMaxNumPLayers(), "too many player for this game"
        while True:
            playerOnMove= self.__palayers[self.__turn%numPlayers]
            self.move(playerOnMove)
            if self.__isGameOver == True:
                break
            
            self.__turn+= 1

    def end(self) -> None:
        self.__isGameOver= True