from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer
from os import system

#il puntatore al padre non serve perché usi la ricorsione
def main():
    system('clear')
    while True:
        try:
            smartness= int(input("Select smartness from 1 to 8 (the bigger it is the smarter it plays, but it will take longer to choose the move): "))
            if smartness>=1 and smartness<=8:
                break
        except:
            exit(-1)

    gameTable= Checkers()
    machine=  MontecarloMachinePlayer("PrimoGiocatore1",smartness,4,2,True)#4 profondita (7 inizia a essere tantino), 30 sec per mossa
    nothuman= MontecarloMachinePlayer("SecondoGiocatore2",smartness,8,2,True)#HumanPlayer("Mario")
    humVSmac= Match([machine,nothuman],gameTable)
    humVSmac.play() 

if __name__ == "__main__":
    main()
    print("program ended")