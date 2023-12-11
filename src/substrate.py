import numpy as np
import pygame

from . import config as cfg
from . import helper as hlp


class Substrate:
    def __init__(self, width, height, concentration=5000, diffusion_rate=0.01, decay_rate=0.1, time_step=1/30):
        self.width = width+1
        self.height = height+1
        self.concentration = np.full((self.width, self.height), concentration)
        self.board = pygame.display.set_mode((width, height))
        self.diffusion_rate = diffusion_rate
        self.board.fill(cfg.WHITE)
        self.drain_points = []
        self.fungal_biomass = np.zeros((self.width, self.height))
        self.decay_rate = decay_rate
        self.time_step = time_step

    def add_drain_point(self, x, y):
        self.drain_points.append((x, y))

    def add_multiple_drain_points(self, points):
        self.drain_points += (points)

    def add_dead_zone(self, origin_x, origin_y, radius):
        for x in range(origin_x - radius, origin_x + radius):
            for y in range(origin_y - radius, origin_y + radius):
                if (x > 0 and x < self.width) and (y > 0 and y < self.height):
                    if (x - origin_x)**2 + (y - origin_y)**2 <= radius**2:
                        self.concentration[x, y] = 0

    def update_concentration(self, i, j):
        laplacian = 0

        if i > 0 and j < self.height - 1:
            laplacian += self.concentration[i - 1, j]
        if i < self.width - 1 and j < self.height - 1:
            laplacian += self.concentration[i + 1, j]
        if j > 0:
            laplacian += self.concentration[i, j - 1]
        if j < self.height - 1:
            laplacian += self.concentration[i, j + 1]

        laplacian -= 4 * self.concentration[i, j]

        diffusion = self.diffusion_rate * hlp.sigmoid(laplacian)
        decay = -self.decay_rate * self.concentration[i, j]

        self.concentration[i, j] += (diffusion + decay) * self.time_step
