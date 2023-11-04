import pygame
import random
import time
from . import mycelium as myc
from . import config as cfg
from . import substrate as sub


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

    while running:
        print(len(fungi.spores), len(fungi.hyphae))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fungi.update()
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
