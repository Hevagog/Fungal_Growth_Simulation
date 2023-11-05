import numpy as np
import pygame
from . import config as cfg


class Substrate:
    def __init__(self, width, height, concentration=5000, decrease_rate=100):
        self.width = width
        self.height = height
        self.concentration = np.full((width, height), concentration)
        self.board = pygame.display.set_mode((width, height))
        self.decrease_rate = decrease_rate
        self.board.fill(cfg.WHITE)
        self.drain_points = []

    def add_drain_point(self, x, y):
        self.drain_points.append((x, y))
