from Utils import *


class Controller:
    def __init__(self, player):
        self.player = player

    def get_inputs(self):
        inputs = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            inputs += [self.player.state.use]
        if pressed[self.use2]:
            inputs += [self.player.state.use]
        if pressed[self.left]:
            inputs += [self.player.state.left]
        if pressed[self.right]:
            inputs += [self.player.state.right]
        if pressed[self.down]:
            inputs += [self.player.state.down]
        if pressed[self.up]:
            inputs += [self.player.state.up]

        return inputs


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


if __name__ == "__main__":
    pygame.init()
    c = FirstPlayerController()
    clock = pygame.time.Clock()

    while True:
        pygame.display.set_mode((100, 100))
        actions = c.get_inputs()
        print(actions)
        clock.tick(10)
