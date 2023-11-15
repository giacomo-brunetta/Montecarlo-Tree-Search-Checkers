from GameStatus.Match import Match
from GameStatus.Checkers import Checkers as Checkers
from GameStatus.MontecarloMachinePlayer import MontecarloMachinePlayer
from GameStatus.HumanPlayer import HumanPlayer
from GameStatus.TestPlayer import TestPlayer
import sys, getopt

MOTD = """
██████╗ ██╗      █████╗ ██╗   ██╗    ███╗   ███╗ ██████╗ ███╗   ██╗████████╗███████╗     ██████╗ █████╗ ██████╗ ██╗      ██████╗ 
██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝    ████╗ ████║██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗
██████╔╝██║     ███████║ ╚████╔╝     ██╔████╔██║██║   ██║██╔██╗ ██║   ██║   █████╗      ██║     ███████║██████╔╝██║     ██║   ██║
██╔═══╝ ██║     ██╔══██║  ╚██╔╝      ██║╚██╔╝██║██║   ██║██║╚██╗██║   ██║   ██╔══╝      ██║     ██╔══██║██╔══██╗██║     ██║   ██║
██║     ███████╗██║  ██║   ██║       ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║   ██║   ███████╗    ╚██████╗██║  ██║██║  ██║███████╗╚██████╔╝
╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝                                                                                                                                                                                                                                                                        
"""


def main():
    argumentList = sys.argv[1:]
    # Options
    options = "hvg:p:m:s:"

    # Long options
    long_options = ["Help", "Verbose", "Game=", "Players=", "Memory=", "Seconds="]

    verbose = False
    game = None
    players = []
    levelsOfMemory = 4
    secondsPerMove = 5

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        players_str = ""

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):

                help_message = """--Verbose (-v) to see logging about Montecarlo Simulation
--Game (-g) = <Name of the game> to choose the game
--Players (-p) = <type of players> one letter per player. m for machine, h for human, t for test
--Memory (-m)  =  levels of the Tree to keep in memory (default = 4)
--Seconds (-s) = seconds per move. The more seconds, the more the bot gets strong (default = 5)

Try standard: -g Checkers -p mh
        """
                print(help_message)
                raise Exception()

            elif currentArgument in ("-g", "--Game"):
                if currentValue == "Checkers":
                    game = Checkers()
                # more games will be added

            elif currentArgument in ("-v", "--Verbose"):
                verbose = True
                print("Verbosity enabled")

            elif currentArgument in ("-p", "--Players"):
                players_str = currentValue

            elif currentArgument in ("-m", "--Memory"):
                levelsOfMemory = int(currentValue)
                print("levels of memory: ", levelsOfMemory)

            elif currentArgument in ("-s", "--Seconds"):
                secondsPerMove = float(currentValue)
                print("seconds per move: ", secondsPerMove)

            else:
                print(f"Warning: param{currentArgument} does not exist!")

        if players_str != "":
            for c in players_str:
                if c == "h":
                    name = input("Name of player: ")
                    players.append(HumanPlayer(name))

                elif c == "m":
                    players.append(MontecarloMachinePlayer("Carlo", game.copy(), levelsOfMemory, secondsPerMove, True, verbose))

                elif c == "t":
                    players.append(TestPlayer())

                else:
                    raise "Invalid player type! h: human, m: machine, t: test (stub)"
        else:
            print("Please specify players!")
            sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(0)

    print("BEGIN of the match!")

    match = Match(players, game)
    match.play()

if __name__ == "__main__":
    print(MOTD)
    main()
    print("program ended")