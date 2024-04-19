from Utils import *


class Controller:
    def __init__(self, player):
        self.player = player

    def get_actions(self):
        actions = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            actions += [self.call_use]
        if pressed[self.use2]:
            actions += [self.call_use]
        if pressed[self.left]:
            actions += [self.call_left]
        if pressed[self.right]:
            actions += [self.call_right]
        if pressed[self.down]:
            actions += [self.call_down]
        if pressed[self.up]:
            actions += [self.call_up]

        return actions

    def call_use(self):
        self.player.state.use()

    def call_left(self):
        self.player.state.left()

    def call_right(self):
        self.player.state.right()

    def call_down(self):
        self.player.state.down()

    def call_up(self):
        self.player.state.up()


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
