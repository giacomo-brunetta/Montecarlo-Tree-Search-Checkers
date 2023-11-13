from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer

def main():
    gameTable= Checkers()
    human= HumanPlayer("Mario")
    tempGameTablegameTable= gameTable
    machine= MontecarloMachinePlayer("Carlo",tempGameTablegameTable,1,2,True)#1 profondita, 2 sec per mossa
    humVSmac= Match([machine,human],gameTable)
    humVSmac.play()
    

if __name__ == "__main__":
    main()
    print("program ended")