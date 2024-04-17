import pygame


pygame.init()


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)

TROUBLESHOOTING = True


def log(*strings):
    if TROUBLESHOOTING:
        print(*strings)
