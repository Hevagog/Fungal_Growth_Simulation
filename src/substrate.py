from collections import defaultdict
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
        self.drain_points = set()
        self.fungal_biomass = np.zeros((self.width, self.height))
        self.fungal_teritory = np.full((self.width, self.height), -1)
        self.decay_rate = decay_rate
        self.time_step = time_step

    def add_drain_point(self, x, y, breed_id):
        # if (x, y) not in self.drain_points:
        self.drain_points.add((x, y))
        self.fungal_teritory[x, y] = breed_id

    def add_multiple_drain_points(self, points, breed_id):
        self.drain_points.update(points)
        x_coords, y_coords = zip(*points)
        self.fungal_teritory[x_coords, y_coords] = breed_id

    def add_dead_zone(self, origin_x, origin_y, radius):
        for x in range(origin_x - radius, origin_x + radius):
            for y in range(origin_y - radius, origin_y + radius):
                if (x > 0 and x < self.width) and (y > 0 and y < self.height):
                    if (x - origin_x)**2 + (y - origin_y)**2 <= radius**2:
                        self.concentration[x, y] = 0

    def update_concentration(self, i, j):
        concentration_ij = self.concentration[i, j]
        concentration_neighbors = self.concentration[max(
            0, i-1):min(i+2, self.width), max(0, j-1):min(j+2, self.height)]
        laplacian = np.sum(concentration_neighbors) - 9 * concentration_ij
        diffusion = self.diffusion_rate * hlp.sigmoid(laplacian)
        decay = -self.decay_rate * concentration_ij

        self.concentration[i, j] += (diffusion + decay) * self.time_step
