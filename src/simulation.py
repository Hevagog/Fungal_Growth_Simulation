import pygame
import random
import numpy as np
import time

from . import obstacle as obs
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub


def add_spore(fungi: myc.Fungi, substrate: sub.Substrate):
    outside_obstacle = False
    x, y = 0, 0
    while not outside_obstacle:
        x = random.randint(0, cfg.SCREEN_WIDTH)
        y = random.randint(0, cfg.SCREEN_HEIGHT)
        for obs in fungi.obstacles:
            if not obs.check_collision(x, y)[0]:
                outside_obstacle = True
            else:
                outside_obstacle = False
                break
        if outside_obstacle:
            break
    fungi.add_spore(myc.Spore(origin_x=x, origin_y=y))
    substrate.add_drain_point(x, y)


def grow_fungi(fungi: myc.Fungi, substrate: sub.Substrate):
    for spore in fungi.spores:
        originx, originy = int(spore.origin_x), int(spore.origin_y)
        if substrate.concentration[originx, originy] <= 0:
            spore.is_alive = False
        else:
            spore.update()
        if not spore.is_alive:
            fungi.kill_spore(spore)
        if spore.reproduce:
            fungi.add_hypha(
                myc.Hypha(origin_x=spore.origin_x, origin_y=spore.origin_y))
            substrate.add_drain_point(originx, originy)

            spore.reproduce = False

    for hypha in fungi.hyphae:
        originx, originy = int(hypha.origin_x), int(hypha.origin_y)

        for obs in fungi.obstacles:
            collision = obs.check_collision(hypha.tip_x, hypha.tip_y)
            if collision[0]:
                hypha.is_alive = False
                hypha.tip_x = collision[1][0]
                hypha.tip_y = collision[1][1]
                fungi.add_spore(
                    myc.Spore(origin_x=collision[1][0], origin_y=collision[1][1], from_hypha=True))
                substrate.add_drain_point(
                    int(collision[1][0]), int(collision[1][1]))
                break

        if hypha.is_alive and substrate.concentration[originx, originy] <= 0:
            hypha.is_alive = False
        else:
            hypha.update()
            substrate.add_multiple_drain_points(hypha.drain_points)
            hypha.drain_points = []
        if not hypha.is_alive:
            fungi.kill_hypha(hypha)
        elif hypha.reproduce:
            fungi.add_hypha(
                myc.Hypha(origin_x=hypha.tip_x, origin_y=hypha.tip_y))
            substrate.add_drain_point(originx, originy)
            hypha.reproduce = False

    for point in substrate.drain_points:
        # for now decrease the concentration by a constant rate
        substrate.concentration[point[0], point[1]] -= substrate.decrease_rate
        if substrate.concentration[point[0], point[1]] <= 0:
            substrate.drain_points.remove(point)


def start(spores: int = 1, num_of_obstacles: int = 0, obstacle_size: int = 100):
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    substrate = sub.Substrate(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.s_0)
    fungi = myc.Fungi()
    for _ in range(num_of_obstacles):
        x = random.randint(0, cfg.SCREEN_WIDTH)
        y = random.randint(0, cfg.SCREEN_HEIGHT)
        fungi.add_obstacle(obs.Obstacle(x, y, obstacle_size))

    for _ in range(spores):
        add_spore(fungi, substrate)

    while running:
        print(len(fungi.spores), len(fungi.hyphae), len(substrate.drain_points))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for obstacle in fungi.obstacles:
            pygame.draw.rect(substrate.board, cfg.OBSTACLE_COLOR,
                             obstacle.rect, 2)
        grow_fungi(fungi, substrate)
        for spore in fungi.spores:
            if spore.is_alive:
                x = spore.origin_x
                y = spore.origin_y
                color = cfg.SPORE_COLOR
                if spore.from_hypha:
                    color = cfg.SPORE_COLOR_FROM_HYPHA
                pygame.draw.circle(substrate.board, color,
                                   (int(x), int(y)), 1)

        for hypha in fungi.hyphae:
            if hypha.is_alive:
                pygame.draw.line(substrate.board, cfg.HYPHA_COLOR,
                                 (int(hypha.origin_x), int(hypha.origin_y)),
                                 (int(hypha.tip_x), int(hypha.tip_y)), 1)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
