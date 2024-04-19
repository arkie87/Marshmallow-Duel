import pygame


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

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


pygame.init()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
