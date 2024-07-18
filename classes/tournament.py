import os
import pickle

# Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from classes.game import Game

class Tournament:
    def __init__(self, args):
        self.args = args

        self.BOARD_SIZE = args[0]
        self.MODE = args[1]
        self.PLAYER1 = args[2]
        self.PLAYER2 = args[3]
        self.ITERMAX = args[4]

    #function to start one game between two players
    #blue player always start
    def single_game(self, blue_starts: bool = True):
        pygame.init()
        pygame.display.set_caption("Hex")

        game = Game(board_size=self.BOARD_SIZE, player1= self.PLAYER1, player2=self.PLAYER2, mode=self.MODE, itermax=self.ITERMAX, blue_starts=blue_starts)
        game.get_game_info([self.BOARD_SIZE,self.MODE, self.PLAYER1, self.PLAYER2, self.ITERMAX])
        #infinite
        while not game.winner:
            game.play()