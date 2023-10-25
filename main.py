import pygame
import sys

from src import mycelium as myc

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
SPORE_COLOR = (0, 0, 255)
HYPHA_COLOR = (0, 255, 0)


def visualize(fungi):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fungal Growth Visualization")

    running = True
    clock = pygame.time.Clock()

    while running:
        print(len(fungi.spores), len(fungi.hyphae))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fungi.update()
        screen.fill(WHITE)

        for spore in fungi.spores:
            if spore.is_alive:
                x = spore.origin_x
                y = spore.origin_y
                pygame.draw.circle(screen, SPORE_COLOR, (int(x), int(y)), 1)

        for hypha in fungi.hyphae:
            if hypha.is_alive:
                x1 = hypha.origin_x
                y1 = hypha.origin_y
                x2 = hypha.tip_x
                y2 = hypha.tip_y
                pygame.draw.line(screen, HYPHA_COLOR,
                                 (int(x1), int(y1)), (int(x2), int(y2)), 1)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    fungi = myc.Fungi()
    fungi.add_spore(myc.Spore(origin_x=SCREEN_WIDTH /
                    2, origin_y=SCREEN_HEIGHT / 2))
    visualize(fungi)
