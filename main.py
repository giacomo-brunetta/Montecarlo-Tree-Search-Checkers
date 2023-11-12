from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer

def main():
    gameTable= Checkers()
    human= HumanPlayer("Mario")
    machine= MontecarloMachinePlayer("Carlo",gameTable,2,5,True)
    humVSmac= Match([machine,human],gameTable)
    humVSmac.play()
    

if __name__ == "__main__":
    main()
    print("program ended")