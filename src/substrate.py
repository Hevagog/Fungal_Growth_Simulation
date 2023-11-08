import numpy as np
import pygame
from . import config as cfg


class Substrate:
    def __init__(self, width, height, concentration=5000, decrease_rate=80):
        self.width = width+1
        self.height = height+1
        self.concentration = np.full((self.width, self.height), concentration)
        self.board = pygame.display.set_mode((width, height))
        self.decrease_rate = decrease_rate
        self.board.fill(cfg.WHITE)
        self.drain_points = []

    def add_drain_point(self, x, y):
        self.drain_points.append((x, y))

    def add_multiple_drain_points(self, points):
        self.drain_points += (points)

    def update(self):
        for point in self.drain_points:
            # for now decrease the concentration by a constant rate
            self.concentration[point[0], point[1]] -= self.decrease_rate
            if self.concentration[point[0], point[1]] <= 0:
                print("Concentration is 0 at point: ", point)
                self.drain_points.remove(point)
