import pygame
from . import helper


class Scarcity:
    def __init__(self, origin_x, origin_y, radius) -> None:
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.radius = radius

        # For now, scarcity are circles, don't think we need to change that

    def check_collision(self, tip_x, tip_y) -> bool:
        if helper.l2_distance((self.origin_x, self.origin_y), (tip_x, tip_y)) < self.radius:
            return False
        return True
