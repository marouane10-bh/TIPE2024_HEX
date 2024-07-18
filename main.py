import logging

from rich import print
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

from classes.tournament import Tournament


def main(args):
    arena = Tournament(args)

    # if MODE == "cpu_vs_cpu":
    #     arena.championship()
    # if MODE == "man_vs_cpu":
    arena.single_game(blue_starts=True)


if __name__ == "__main__":
    BOARD_SIZE = 7
    ITERMAX = 500
    MODE = "man_vs_cpu"
    PLAYER1= "HUMAN"

    
    log = logging.getLogger("rich")
    print("What [bold blue]board size[/bold blue] do you want to play on?", end="\t")
    BOARD_SIZE = int(input())
    print("Chose the [bold blue]game mode[/bold blue]", end="\t")
    MODE = str(input())

    if MODE == "cpu_vs_cpu":
        print("Chose the [bold blue]blue player[/bold blue] strategy", end="\t")
        PLAYER1 = str(input())
        print("Chose the [bold red]red player[/bold red] strategy", end="\t")
        PLAYER2 = str(input())
    else:
        print()
        log.info("You will be playing as the BLUE player!")
        print()
        print("Chose the [bold red]red player[/bold red] strategy", end="\t")
        PLAYER2 = str(input())
    if PLAYER1 == "MCTS" or PLAYER2 == "MCTS":
        print("How many iterations should MCTS play ([bold red]itermax[/bold red])?", end="\t")
        ITERMAX = int(input())

    args = BOARD_SIZE, MODE, PLAYER1, PLAYER2, ITERMAX
    main(args)
