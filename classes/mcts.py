import copy
from math import log, sqrt, inf
from random import choice

from classes.player import Player
import numpy as np
from rich.console import Console
from rich.progress import track
from rich.table import Table
from time import sleep

class Node(object):
    def __init__(self, logic, board, move=(None, None), wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child


class MCTSPlayer(Player):
    def __init__(self, logic, ui, board_state, color, itermax):
        super().__init__(logic, ui, color)
        self.root_state = copy.copy(board_state)
        self.state = copy.copy(board_state)
        self.color = color
        self.players = [1, 2]
        self.players.remove(self.color)
        self.other_player = self.players[0]
        self.turn = {True: self.color, False: self.other_player}
        self.turn_state = True
        self.itermax = itermax


    def start(self, verbose: bool = False, show_predictions: bool = False):
        root_node = Node(self.logic, self.root_state)
        # print("hadoo full", self.logic.get_occ_moves(self.root_state))

        for _ in track(range(self.itermax), description="MCTS:", total=self.itermax):
            node = root_node
            state = copy.deepcopy(self.root_state)
            self.turn_state = True
            # sleep(3)
            # Select
            # print("untried and children", node.untried_moves, node.children)
            # while the node is fully expanded and has children ( == not a leaf* ) we can select promosing child using UCB
            ### * == a leaf is a node that has a potential child from which no simulation has been played before (so if he has already a child
            ### that has been visited and other one not yet, it's still a leaf)
            while node.untried_moves == [] and node.children != []:
                # Node is fully expanded and non-terminal
                uct_values = [self.select(child) for child in node.children]
                # print("uct:", uct_values)
                # sleep(3)
                if all([value == inf for value in uct_values]):
                    node = choice(node.children)
                else:
                    node = node.children[np.argmax(uct_values)]

                x, y = node.move
                # print("x,y", x,y)
                state[x][y] = self.turn[self.turn_state]
                self.next_turn()

            # Expand
            # if the leaf has previous visits (his ucb != inf) time to explore his unexplored children
            if node.untried_moves != []: # and node.visits >0 :
                x, y = choice(node.untried_moves)
                state[x][y] = self.turn[self.turn_state]
                node.untried_moves.remove((x, y))
                node = node.add_child(Node(self.logic, state, (x, y)))
                self.next_turn()

            # Playout
            # TODO: For some reason, self.logic.get_possible_moves(state) must be added
            while not self.logic.MCTS_GAME_OVER and self.logic.get_possible_moves(state):
                x, y = choice(self.logic.get_possible_moves(state))
                state[x][y] = self.turn[self.turn_state]

                for player in [1, 2]:
                    global winner
                    winner = self.logic.is_game_over(player, state, True)
                    if winner:
                        break

                self.next_turn()

            # Reset MCTS_GAME_OVER
            self.logic.MCTS_GAME_OVER = False

            # Backpropagation
            while node != None:
                win_value = 1 if winner is self.color else 0

                node.wins += win_value
                node.visits += 1
                # print("node wins and visits : ", node.wins, node.visits, node.parent)
                # sleep(6)
                node = node.parent

            # root_node.wins += win_value
            # root_node.visits += 1
            # print("root wins and visits : ", root_node.wins, root_node.visits)

        visits = [float(node.wins)/float(node.visits) for node in root_node.children]
        result = root_node.children[np.argmax(visits)].move

        output = [(node.wins, node.visits, node.move) for node in root_node.children]
        if verbose:
            self.print_output(output, result)
        # if show_predictions:
        #     # Get a temporary board state to get the possible moves
        #     temp_state = self.state
        #     x, y = result
        #     temp_state[x][y] = self.starting_player
        #     available_pos = self.logic.get_possible_moves(temp_state)
        #     self.ui.show_mcts_predictions(output, available_pos)

        return result

    def next_turn(self):
        self.turn_state = not self.turn_state

    def select(self, node):
        # Constants
        c = sqrt(2)

        wi = node.wins
        Ni = node.parent.visits
        ni = node.visits

        # If node has not been visited yet
        if not Ni or not ni:
            value = inf

        else:
            value = wi / ni + c * sqrt(log(Ni) / ni)

        return value

    def print_output(self, output, result):
        output.sort(key=lambda k: [k[2][0], k[2][1]])
        console = Console()

        table = Table(show_header=True, header_style="bold red")
        table.add_column("Wins", justify="center")
        table.add_column("Visits", justify="center")
        table.add_column("Move", justify="center")
        for row in output:
            if row[2] == result:
                w = "[cyan]" + str(row[0]) + "[/cyan]"
                v = "[cyan]" + str(row[1]) + "[/cyan]"
                m = "[cyan]" + str(row[2]) + "[/cyan]"
            else:
                w = str(row[0])
                v = str(row[1])
                m = str(row[2])
            table.add_row(w, v, m)

        console.print(table)


    def select_move(self, node):
        self.root_state = copy.copy(self.logic.logger)
        self.state = copy.copy(self.logic.logger)
        x, y = self.start(verbose=True, show_predictions=True)
        return x,y