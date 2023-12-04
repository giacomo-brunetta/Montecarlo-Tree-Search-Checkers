from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer
from os import system

def main():
    """
    system('clear')
    while True:
        try:
            smartness= int(input("Select smartness from 1 to 4 (the bigger it is the smarter it plays, but it will take longer to choose the move): "))
            if smartness>=1 and smartness<=4:
                break
        except:
            exit(-1)
    """
    smartness = 2
    gameTable= Checkers()
    machine=  MontecarloMachinePlayer("FirstPlayer", smartness,1,2,False)
    nothuman= MontecarloMachinePlayer("SecondPlayer",smartness,1,2,False)
    #nothuman= HumanPlayer("Mario")
    humVSmac= Match([machine,nothuman],gameTable)
    humVSmac.play() 

if __name__ == "__main__":
    main()
    print("program ended")