import pygame
import random

from . import obstacle as obs
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub
from . import scarcity as scr
from . import helper as hlp


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
    concentration = substrate.concentration[x, y]
    print(concentration)
    fungi.add_spore(myc.Spore(origin_x=x, origin_y=y,
                    substrate_concentration_at_origin=concentration))
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
            spore.reproduce = False
        if spore.reproduce:
            concentration = substrate.concentration[originx, originy]
            if concentration > 0:
                fungi.add_hypha(
                    myc.Hypha(origin_x=spore.origin_x, origin_y=spore.origin_y,
                              substrate_concentration_at_origin=concentration))
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
                concentration = substrate.concentration[originx, originy]
                fungi.add_spore(
                    myc.Spore(origin_x=collision[1][0], origin_y=collision[1][1], from_hypha=True,
                              substrate_concentration_at_origin=concentration))
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
            concentration = substrate.concentration[originx, originy]
            if concentration > 0:
                fungi.add_hypha(
                    myc.Hypha(origin_x=hypha.tip_x, origin_y=hypha.tip_y,
                              substrate_concentration_at_origin=concentration))
                substrate.add_drain_point(originx, originy)
            hypha.reproduce = False

    for point in substrate.drain_points:
        growth_rate = hlp.sigmoid(
            substrate.concentration[point[0], point[1]])
        substrate.fungal_biomass[point[0], point[1]
                                 ] += growth_rate*substrate.decrease_coefficient

        decay_rate = hlp.sigmoid(substrate.fungal_biomass[point[0], point[1]])
        substrate.concentration[point[0], point[1]
                                ] -= decay_rate * substrate.decrease_coefficient
        if substrate.concentration[point[0], point[1]] <= 0:
            # print("\t\t", "Concentration is 0 at point: ", point)
            substrate.drain_points.remove(point)


def start(spores: int = 1, num_of_obstacles: int = 0, obstacle_size: int = 100,
          num_of_scarcity: int = 0, scarcity_radius: int = 80):
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
