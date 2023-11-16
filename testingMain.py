from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer

def main():
    while True:
        try:
            smartness= int(input("Select smartness from 1 to 8 (the bigger it is the smarter it plays, but it will take longer to choose the move): "))
            if smartness>=1 and smartness<=8:
                break
        except:
            exit(-1)
    
    gameTable= Checkers()
    human= HumanPlayer("Mario")
    tempGameTablegameTable= gameTable
    machine= MontecarloMachinePlayer("Carlo",tempGameTablegameTable,smartness,10,True,True)#4 profondita (7 inizia a essere tantino), 30 sec per mossa
    humVSmac= Match([machine,human],gameTable)
    humVSmac.play()
    

if __name__ == "__main__":
    main()
    print("program ended")