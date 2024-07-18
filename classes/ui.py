from math import cos, sin, pi, radians

import numpy as np
import pygame
from pygame import gfxdraw
from pygame import time


class UI:
    def __init__(self, board_size: int):

        # Colors
        self.red = (222, 29, 47)
        self.blue = (0, 121, 251)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (40, 40, 40)
        self.gray = (70, 70, 70)


        self.clock = time.Clock()
        #set dimensions and draw the screen of the game 
        self.board_size = board_size
        assert 1 < self.board_size <= 26
        self.hex_radius = 20
        self.x_offset, self.y_offset = 60, 60
        self.text_offset = 45
        self.screen = pygame.display.set_mode(
            (self.x_offset + (2 * self.hex_radius) * self.board_size + self.hex_radius * self.board_size,
             round(self.y_offset + (1.75 * self.hex_radius) * self.board_size)))
        
        self.screen.fill(self.black)
        self.fonts = pygame.font.SysFont("Sans", 20)

        # Players
        self.BLUE_PLAYER = 1
        self.RED_PLAYER = 2

       
        #self.rects : cells
        #self.color : colors of the cells
        #self.node : current played cell
        self.hex_lookup = {}
        self.rects, self.color, self.node = [], [self.white] * (self.board_size ** 2), None
        

    def draw_hexagon(self, surface: object, color: tuple, position: tuple, node: int):
        # Vertex count and radius
        n = 6 #hexagone
        x, y = position
        offset = 3

        # Outline / jnab
        self.hex_lookup[node] = [(x + (self.hex_radius + offset) * cos(radians(90) + 2 * pi * _ / n),
                                  y + (self.hex_radius + offset) * sin(radians(90) + 2 * pi * _ / n))
                                 for _ in range(n)]
        gfxdraw.aapolygon(surface,
                          self.hex_lookup[node],
                          color)

        # Shape /hexa shape
        gfxdraw.filled_polygon(surface,
                               [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                                 y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                                for _ in range(n)],
                               self.color[node])

        # Antialiased shape outline
        gfxdraw.aapolygon(surface,
                          [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
                            y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
                           for _ in range(n)],
                          self.black)

        # Placeholder
        rect = pygame.draw.rect(surface,
                                self.color[node],
                                pygame.Rect(x - self.hex_radius + offset, y - (self.hex_radius / 2),
                                            (self.hex_radius * 2) - (2 * offset), self.hex_radius))
        self.rects.append(rect)

        # Bounding box (colour-coded)
        bbox_offset = [0, 3]

        # Top side
        if 0 < node < self.board_size:
            points = ([self.hex_lookup[node - 1][3][_] - bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node - 1][4][_] - bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node][3][_] - bbox_offset[_] for _ in range(2)])
            gfxdraw.filled_polygon(surface,
                                   points,
                                   self.red)
            gfxdraw.aapolygon(surface,
                              points,
                              self.red)

        # Bottom side
        if self.board_size ** 2 - self.board_size < node < self.board_size ** 2:
            points = ([self.hex_lookup[node - 1][0][_] + bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node - 1][5][_] + bbox_offset[_] for _ in range(2)],
                      [self.hex_lookup[node][0][_] + bbox_offset[_] for _ in range(2)])
            gfxdraw.filled_polygon(surface,
                                   points,
                                   self.red)
            gfxdraw.aapolygon(surface,
                              points,
                              self.red)

        # Left side
        bbox_offset = [3, -3]

        if node % self.board_size == 0:
            if node >= self.board_size:
                points = ([self.hex_lookup[node - self.board_size][1][_] - bbox_offset[_] for _ in range(2)],
                          [self.hex_lookup[node - self.board_size][0][_] - bbox_offset[_] for _ in range(2)],
                          [self.hex_lookup[node][1][_] - bbox_offset[_] for _ in range(2)])
                gfxdraw.filled_polygon(surface,
                                       points,
                                       self.blue)
                gfxdraw.aapolygon(surface,
                                  points,
                                  self.blue)

        # Right side
        if (node + 1) % self.board_size == 0:
            if node > self.board_size:
                points = ([self.hex_lookup[node - self.board_size][4][_] + bbox_offset[_] for _ in
                           range(2)],
                          [self.hex_lookup[node - self.board_size][5][_] + bbox_offset[_] for _ in
                           range(2)],
                          [self.hex_lookup[node][4][_] + bbox_offset[_] for _ in range(2)])
                gfxdraw.filled_polygon(surface,
                                       points,
                                       self.blue)
                gfxdraw.aapolygon(surface,
                                  points,
                                  self.blue)

    def draw_text(self):
        alphabet = list(map(chr, range(97, 123)))

        for _ in range(self.board_size):
            # Columns
            text = self.fonts.render(alphabet[_].upper(), True, self.white, self.black)
            text_rect = text.get_rect()
            text_rect.center = (self.x_offset + (2 * self.hex_radius) * _, self.text_offset / 2)
            self.screen.blit(text, text_rect)

            # Rows
            text = self.fonts.render(str(_), True, self.white, self.black)
            text_rect = text.get_rect()
            text_rect.center = (
                (self.text_offset / 4 + self.hex_radius * _, self.y_offset + (1.75 * self.hex_radius) * _))
            self.screen.blit(text, text_rect)

    def draw_board(self, show_mcts_predictions: bool = True):
        counter = 0
        for row in range(self.board_size):
            for column in range(self.board_size):
                self.draw_hexagon(self.screen, self.black, self.get_coordinates(row, column), counter)
                counter += 1
        self.draw_text()

        # Filled polygons gradient-coloured based on MCTS predictions
        # (i.e. normalized #visits per node)
        # if show_mcts_predictions:
        #     try:
        #         n = 6
        #         for (row, column) in mcts_predictions.keys():
        #             x, y = self.get_coordinates(row, column)
        #             gfxdraw.filled_polygon(self.screen,
        #                                    [(x + self.hex_radius * cos(radians(90) + 2 * pi * _ / n),
        #                                      y + self.hex_radius * sin(radians(90) + 2 * pi * _ / n))
        #                                     for _ in range(n)],
        #                                    self.green + (mcts_predictions[(row, column)],))
        #     except NameError:
        #         pass

    def get_coordinates(self, row: int, column: int):
        x = self.x_offset + (2 * self.hex_radius) * column + self.hex_radius * row
        y = self.y_offset + (1.75 * self.hex_radius) * row

        return x, y

    def get_true_coordinates(self, node: int):
        return int(node / self.board_size), node % self.board_size

    #get the node where the mouse is hovering
    def get_node_hover(self):
        # Source: https://bit.ly/2Wl5Grz
        mouse_pos = pygame.mouse.get_pos()
        for _, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                self.node = _
                break
                     
        if type(self.node) is int:
            # Node
            row, column = int(self.node / self.board_size), self.node % self.board_size
            self.draw_hexagon(self.screen, self.green, self.get_coordinates(row, column), self.node)

            # Text
            x, y = self.get_true_coordinates(self.node)
            x, y = self.get_coordinates(x, y)
            alphabet = list(map(chr, range(97, 123)))
            txt = alphabet[column].upper() + str(row)
            node_font = pygame.font.SysFont("Sans", 18)
            foreground = self.black if self.color[self.node] is self.white else self.white
            text = node_font.render(txt, True, foreground, self.color[self.node])
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text, text_rect)

        return self.node

    def show_mcts_predictions(self, output: list, available_pos: list):
        global mcts_predictions
        # Remove position played by MCTS player
        visits = [node[1] for node in output]
        output.pop(np.argmax(visits))
        # Get normalized visits
        normalized_visits = self.get_normalized_visits([node[1] for node in output])
        mcts_predictions = {(row, column): alpha_value for ((row, column), alpha_value) in
                            zip(available_pos, normalized_visits)}

    def get_normalized_visits(self, visits: list):
        normalized_visits = [node_visits - min(visits) for node_visits in visits]
        # Maximum set to 200 instead of 255 (RGBA)
        return [int(node_visits / max(normalized_visits) * 200) for node_visits in normalized_visits]
