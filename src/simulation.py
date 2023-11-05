import pygame
import random
import time
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub


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
        if substrate.concentration[originx, originy] <= 0:
            hypha.is_alive = False
        else:
            hypha.update()
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


def start(spores: int = 1):
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    substrate = sub.Substrate(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.s_0)
    fungi = myc.Fungi()

    for _ in range(spores):
        x = random.randint(0, cfg.SCREEN_WIDTH)
        y = random.randint(0, cfg.SCREEN_HEIGHT)
        fungi.add_spore(myc.Spore(origin_x=x, origin_y=y))
        substrate.add_drain_point(x, y)

    while running:
        print(len(fungi.spores), len(fungi.hyphae), len(substrate.drain_points))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # fungi.update()
        # substrate.update()
        grow_fungi(fungi, substrate)
        for spore in fungi.spores:
            if spore.is_alive:
                x = spore.origin_x
                y = spore.origin_y
                pygame.draw.circle(substrate.board, cfg.SPORE_COLOR,
                                   (int(x), int(y)), 1)

        for hypha in fungi.hyphae:
            if hypha.is_alive:
                x1 = hypha.origin_x
                y1 = hypha.origin_y
                x2 = hypha.tip_x
                y2 = hypha.tip_y
                pygame.draw.line(substrate.board, cfg.HYPHA_COLOR,
                                 (int(x1), int(y1)), (int(x2), int(y2)), 1)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
