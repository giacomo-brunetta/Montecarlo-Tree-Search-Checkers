from GameStatus.Player import Player
from abc import ABC, abstractmethod
from typing import Type
from GameStatus.Game import Game

class TestPlayer(Player):
    _name = "Test"
    def move(self, gameStatus: Type['Game'], turn: int) -> Type['Game']:
        moves = gameStatus.moves(turn)
        if moves is None:
            print("No moves available")
            return None
        else:
            return moves[0]