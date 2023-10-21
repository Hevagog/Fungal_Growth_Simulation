import pygame
import sys
import random
import time

from . import config

SCREEN_SIZE = (800, 600)
white = (255, 255, 255)
blue = (0, 0, 255)


def start():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Fungal Growth Simulation")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(white)

        pygame.display.update()
    pygame.quit()
