from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer

MOTD = """
██████╗ ██╗      █████╗ ██╗   ██╗    ███╗   ███╗ ██████╗ ███╗   ██╗████████╗███████╗     ██████╗ █████╗ ██████╗ ██╗      ██████╗ 
██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝    ████╗ ████║██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗
██████╔╝██║     ███████║ ╚████╔╝     ██╔████╔██║██║   ██║██╔██╗ ██║   ██║   █████╗      ██║     ███████║██████╔╝██║     ██║   ██║
██╔═══╝ ██║     ██╔══██║  ╚██╔╝      ██║╚██╔╝██║██║   ██║██║╚██╗██║   ██║   ██╔══╝      ██║     ██╔══██║██╔══██╗██║     ██║   ██║
██║     ███████╗██║  ██║   ██║       ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║   ██║   ███████╗    ╚██████╗██║  ██║██║  ██║███████╗╚██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝                                                                                                                                                                                                                                                                        
"""


def main():
    gameTable= Checkers()
    human= HumanPlayer("Mario")
    tempGameTablegameTable= gameTable
    machine= MontecarloMachinePlayer("Carlo", tempGameTablegameTable, 4, 5, True, False)#4 profondita (7 inizia a essere tantino), 30 sec per mossa
    humVSmac= Match([machine,human],gameTable)
    humVSmac.play()

if __name__ == "__main__":
    print(MOTD)
    main()
    print("program ended")