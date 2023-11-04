import numpy as np
import pygame
from . import config as cfg


class Substrate:
    def __init__(self, width, height, concentration):
        self.width = width
        self.height = height
        self.concentration = concentration
        self.board = pygame.display.set_mode((width, height))
        self.board.fill(cfg.WHITE)
        self.drain_points = []

    def add_drain_point(self, x, y):
        self.drain_points.append((x, y))
