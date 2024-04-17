from Utils import *


class Controller:
    def __init__(self, player):
        self.player = player

    def get_actions(self):
        actions = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            actions += [self.player.use]
        if pressed[self.use2]:
            actions += [self.player.use]
        if pressed[self.left]:
            actions += [self.player.left]
        if pressed[self.right]:
            actions += [self.player.right]
        if pressed[self.down]:
            actions += [self.player.down]
        if pressed[self.up]:
            actions += [self.player.up]

        return actions


class FirstPlayerController(Controller):
    def __init__(self, player):
        super().__init__(player)
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.down = pygame.K_s
        self.up = pygame.K_w
        self.use = pygame.K_e
        self.use2 = pygame.K_q


class SecondPlayerController(Controller):
    def __init__(self, player):
        super().__init__(player)
        self.left = pygame.K_j
        self.right = pygame.K_l
        self.down = pygame.K_k
        self.up = pygame.K_i
        self.use = pygame.K_u
        self.use2 = pygame.K_o
