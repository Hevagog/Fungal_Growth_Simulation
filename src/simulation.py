import pygame
import random
import numpy as np

from . import obstacle as obs
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub
from . import scarcity as scr
from . import helper as hlp


def add_spore(fungi: myc.Fungi, substrate: sub.Substrate, breed: int):
    x, y = random.randint(1, cfg.SCREEN_WIDTH -
                          1), random.randint(1, cfg.SCREEN_HEIGHT - 1)

    if len(fungi.obstacles) > 0:
        obstacles = [obs for obs in fungi.obstacles
                     if not obs.check_collision(x, y)[0]]
        if obstacles:
            fungi.add_spore(myc.Spore(origin_x=x, origin_y=y, breed=breed))
            substrate.add_drain_point(x, y, breed)
    else:
        fungi.add_spore(myc.Spore(origin_x=x, origin_y=y, breed=breed))
        substrate.add_drain_point(x, y, breed)


def update_spore(fungi: myc.Fungi, substrate: sub.Substrate):
    alive_spores = [spore for spore in fungi.spores if spore.is_alive]

    for spore in alive_spores:
        origin_x, origin_y = int(spore.origin_x), int(spore.origin_y)
        concentration = substrate.concentration[origin_x, origin_y]

        if concentration <= 0:
            spore.is_alive = False
        else:
            spore.die_or_reproduce()

        if not spore.is_alive:
            fungi.kill_spore(spore)
            spore.reproduce = False

        if spore.reproduce and concentration > 0:
            fungi.add_hypha(
                myc.Hypha(origin_x=spore.origin_x, origin_y=spore.origin_y,
                          breed=spore.breed_id))
            substrate.add_drain_point(origin_x, origin_y, spore.breed_id)
            spore.reproduce = False


def update_hypha(fungi: myc.Fungi, substrate: sub.Substrate):
    obstacles = fungi.obstacles
    concentration = substrate.concentration

    for hypha in fungi.hyphae:
        origin_x, origin_y = int(hypha.origin_x), int(hypha.origin_y)

        if concentration[origin_x, origin_y] <= 0 or not hypha.is_alive or \
                (substrate.fungal_teritory[int(hypha.tip_x), int(hypha.tip_y)] != hypha.breed_id and
                 substrate.fungal_teritory[int(hypha.tip_x), int(hypha.tip_y)] != -1):
            hypha.is_alive = False
            fungi.kill_hypha(hypha)
            break

        for obs in obstacles:
            if obs.check_collision(hypha.tip_x, hypha.tip_y)[0]:
                hypha.is_alive = False
                break

        hypha.update()
        if substrate.fungal_teritory[int(hypha.tip_x), int(hypha.tip_y)] != -1 and \
                substrate.fungal_teritory[int(hypha.tip_x), int(hypha.tip_y)] != hypha.breed_id:
            hypha.is_alive = False
            break
        substrate.add_multiple_drain_points(hypha.drain_points, hypha.breed_id)

        if hypha.reproduce:
            fungi.add_hypha(
                myc.Hypha(origin_x=hypha.tip_x, origin_y=hypha.tip_y,
                          breed=hypha.breed_id,
                          ))
            substrate.add_drain_point(origin_x, origin_y, hypha.breed_id)
            hypha.reproduce = False


def update_substrate(substrate: sub.Substrate):
    drain_points_copy = set(substrate.drain_points.copy())
    for point in drain_points_copy:
        substrate.update_concentration(point[0], point[1])
        if substrate.concentration[point[0], point[1]] <= 0.5:
            substrate.drain_points.remove(point)


def grow_fungi(fungi: myc.Fungi, substrate: sub.Substrate):
    update_spore(fungi, substrate)
    update_hypha(fungi, substrate)
    update_substrate(substrate)


def start(spores: int = 1, num_of_obstacles: int = 0, obstacle_size: int = 100,
          num_of_scarcity: int = 0, scarcity_radius: int = 80):
    # pygame initialization and map creation
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    substrate = sub.Substrate(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.s_0)
    fungi = myc.Fungi()
    for _ in range(num_of_scarcity):
        x = random.randint(0, cfg.SCREEN_WIDTH)
        y = random.randint(0, cfg.SCREEN_HEIGHT)
        scarcity = scr.Scarcity(x, y, scarcity_radius)
        fungi.add_scarcity(scarcity)
        pygame.draw.circle(substrate.board, cfg.SCARCITY_COLOR,
                           [x, y], scarcity.radius, 3)
        substrate.add_dead_zone(x, y, scarcity.radius)
    for _ in range(num_of_obstacles):
        x = random.randint(0, cfg.SCREEN_WIDTH)
        y = random.randint(0, cfg.SCREEN_HEIGHT)
        fungi.add_obstacle(obs.Obstacle(x, y, obstacle_size))

    # for now there are only 3 breeds (0, 1, 2)
    for i in range(spores):
        add_spore(fungi, substrate, breed=i)

    # Main loop
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
            else:
                fungi.kill_spore(spore)

        for hypha in fungi.hyphae:
            if hypha.is_alive:
                pygame.draw.line(substrate.board, hypha.color,
                                 (int(hypha.origin_x), int(hypha.origin_y)),
                                 (int(hypha.tip_x), int(hypha.tip_y)), 1)
            else:
                fungi.kill_hypha(hypha)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
