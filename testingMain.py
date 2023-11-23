from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer
from os import system

#il puntatore al padre non serve perché usi la ricorsione
def main():
    smartness = 2

    gameTable= Checkers()
    machine=  MontecarloMachinePlayer("PrimoGiocatore1",smartness,1,2,verbose= False)#4 profondita (7 inizia a essere tantino), 30 sec per mossa
    nothuman= MontecarloMachinePlayer("SecondoGiocatore2",smartness,1,2, verbose=False)#HumanPlayer("Mario")
    humVSmac= Match([machine,nothuman],gameTable)
    humVSmac.play() 

if __name__ == "__main__":
    main()
    print("program ended")