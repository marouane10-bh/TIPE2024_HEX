from abc import ABC, abstractmethod
from random import choice
import numpy as np

class Player():
    def __init__(self, logic, ui, color):
        self.logic = logic
        self.ui = ui
        self.color = color

    @abstractmethod
    def select_move(self, node):
        pass


class RandomPlayer(Player):
    def select_move(self, node):
        x, y = choice(self.logic.get_possible_moves(self.logic.logger))
        return x, y

class HumanPlayer(Player):
    def select_move(self, node):
        x, y = self.ui.get_true_coordinates(node)
        return x,y  
    
