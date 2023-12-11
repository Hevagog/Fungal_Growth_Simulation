import pygame
import random

from . import obstacle as obs
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub
from . import scarcity as scr
from . import helper as hlp


def add_spore(fungi: myc.Fungi, substrate: sub.Substrate, breed: int):
    outside_obstacle = False
    x, y = random.randint(1, cfg.SCREEN_WIDTH -
                          1), random.randint(1, cfg.SCREEN_HEIGHT-1)
    if len(fungi.obstacles) > 0:
        while not outside_obstacle:
            for obs in fungi.obstacles:
                if not obs.check_collision(x, y)[0]:
                    outside_obstacle = True
                else:
                    outside_obstacle = False
                    break
            if outside_obstacle:
                break
            x = random.randint(0, cfg.SCREEN_WIDTH)
            y = random.randint(0, cfg.SCREEN_HEIGHT)
    concentration = substrate.concentration[x, y]
    print(concentration)
    fungi.add_spore(myc.Spore(origin_x=x, origin_y=y,
                    substrate_concentration_at_origin=concentration, breed=breed))
    substrate.add_drain_point(x, y)


def update_spore(fungi: myc.Fungi, substrate: sub.Substrate):
    for spore in fungi.spores:
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
                          substrate_concentration_at_origin=concentration,
                          breed=spore.breed_id))
            substrate.add_drain_point(origin_x, origin_y)
            spore.reproduce = False


def update_hypha(fungi: myc.Fungi, substrate: sub.Substrate):
    for hypha in fungi.hyphae:
        origin_x, origin_y = int(hypha.origin_x), int(hypha.origin_y)

        for obs in fungi.obstacles:
            collision = obs.check_collision(hypha.tip_x, hypha.tip_y)

            if collision[0]:
                hypha.is_alive = False
                hypha.tip_x, hypha.tip_y = collision[1][0], collision[1][1]
                concentration = substrate.concentration[origin_x, origin_y]
                fungi.add_spore(
                    myc.Spore(origin_x=collision[1][0], origin_y=collision[1][1], from_hypha=True,
                              substrate_concentration_at_origin=concentration, breed=hypha.breed_id))
                substrate.add_drain_point(
                    int(collision[1][0]), int(collision[1][1]))
                break

        if hypha.is_alive and substrate.concentration[origin_x, origin_y] <= 0:
            hypha.is_alive = False
        else:
            hypha.update()
            substrate.add_multiple_drain_points(hypha.drain_points)
            hypha.drain_points = []

        if not hypha.is_alive:
            fungi.kill_hypha(hypha)
        elif hypha.reproduce:
            concentration = substrate.concentration[origin_x, origin_y]

            if concentration > 0:
                fungi.add_hypha(
                    myc.Hypha(origin_x=hypha.tip_x, origin_y=hypha.tip_y,
                              breed=hypha.breed_id,
                              substrate_concentration_at_origin=concentration))
                substrate.add_drain_point(origin_x, origin_y)
            hypha.reproduce = False


def update_substrate(substrate: sub.Substrate):
    for point in substrate.drain_points:
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
    for _ in range(spores):
        add_spore(fungi, substrate, breed=1)
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

        for hypha in fungi.hyphae:
            if hypha.is_alive:
                pygame.draw.line(substrate.board, hypha.color,
                                 (int(hypha.origin_x), int(hypha.origin_y)),
                                 (int(hypha.tip_x), int(hypha.tip_y)), 1)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
