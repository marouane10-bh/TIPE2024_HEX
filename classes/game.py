import sys

import pygame
from rich.console import Console
from rich.table import Table
import time
from classes.logic import Logic
from classes.ui import UI
from classes.player import RandomPlayer, HumanPlayer
from classes.minMax import MinimaxPlayer
from classes.mcts import MCTSPlayer

class Game:
    def __init__(self, board_size: int, player1: str, player2: str, mode: str, itermax: int, blue_starts: bool = True):
        # Select mode
        self.modes = {"cpu_vs_cpu": 0,
                      "man_vs_cpu": 0}
        self.modes[mode] = 1
        
        # Instantiate classes
        self.ui = UI(board_size)
        self.logic = Logic(self.ui)
        self.itermax = itermax

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn = {True: self.ui.BLUE_PLAYER, False: self.ui.RED_PLAYER}

        # BLUE player starts
        self.turn_state = blue_starts
        self.players = {self.ui.BLUE_PLAYER: self.create_player(player1, self.ui.BLUE_PLAYER), self.ui.RED_PLAYER: self.create_player(player2, self.ui.RED_PLAYER)}

    def create_player(self, strategy, color):
        if strategy == "HUMAN":
            return HumanPlayer(self.logic,self.ui, color)
        elif strategy == "RANDOM":
            return RandomPlayer(self.logic,self.ui, color)
        elif strategy == "MCTS":
            return MCTSPlayer(self.logic, self.ui, board_state=self.logic.logger, color=self.ui.RED_PLAYER, itermax=self.itermax)
        elif strategy == "MINMAX":
            return MinimaxPlayer(self.logic, self.ui, board_state=self.logic.logger, color=self.ui.RED_PLAYER, max_depth=2)

    def get_game_info(self, args):
        console = Console()

        table = Table(title="Hex Game", show_header=True, header_style="bold magenta")
        table.add_column("Parameters", justify="center")
        table.add_column("Value", justify="right")
        table.add_row("Board size", str(args[0]))
        table.add_row("Mode", str(args[1]))
        table.add_row("Blue Player", str(args[2]))
        table.add_row("Red Player", str(args[3]))
        table.add_row("MCTS Itermax", str(args[4]))

        console.print(table)

    def handle_events(self):
        if self.modes["man_vs_cpu"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP or self.modes["cpu_vs_cpu"]:
                    self.run_turn()

        if self.modes["cpu_vs_cpu"]:
            self.run_turn()

    def run_turn(self):
        if self.modes["cpu_vs_cpu"]:
            node = None
        if self.modes["man_vs_cpu"]:
            node = self.node

        # BLUE player's turn
        if not self.play_move(node, self.players[self.turn[self.turn_state]]):
            return
        # RED player's turn (always gonna be an AI)
        else:
            if not self.play_move(node, self.players[self.turn[self.turn_state]]):
                return

    def play_move(self, node, player):
        # Forbid playing on already busy node
        try:
            self.winner = self.logic.get_action(node, player)
            print("winner", self.winner)
        except AssertionError:
            return False

        # Next turn
        self.turn_state = not self.turn_state

        # If there is a winner, break the loop
        if self.get_winner():
            self.ui.draw_board()
            pygame.display.update()
            # TODO add graphic to show who won
            time.sleep(2)
            return False

        return True

    def get_winner(self):
        if self.winner:
            print("Player {} wins!".format(self.winner))
            return True

    def play(self):
        self.ui.draw_board()

        if self.modes["man_vs_cpu"]:
            self.node = self.ui.get_node_hover()

        pygame.display.update()
        self.ui.clock.tick(30)
        self.handle_events()
