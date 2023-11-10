import pygame


class Obstacle:
    def __init__(self, origin_x, origin_y, size) -> None:
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.size = size

        # For now, obstacles are squares, don't think we need to change that
        self.rect = pygame.Rect(origin_x, origin_y, size, size)

    def check_collision(self, tip_x, tip_y) -> tuple:
        if self.rect.collidepoint(tip_x, tip_y):
            intersection_x = max(self.rect.left, min(tip_x, self.rect.right))
            intersection_y = max(self.rect.top, min(tip_y, self.rect.bottom))
            return (True, (intersection_x, intersection_y))
        return (False, None)
