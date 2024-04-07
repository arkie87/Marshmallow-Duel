import pygame


class Controller:
    def __init__(self, number=0):
        if number == 0:
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.down = pygame.K_s
            self.up = pygame.K_w
            self.use = pygame.K_e
        elif number == 1:
            self.left = pygame.K_j
            self.right = pygame.K_l
            self.down = pygame.K_k
            self.up = pygame.K_i
            self.use = pygame.K_u

    def get_action(self):
        actions = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            return "use"
        if pressed[self.left]:
            actions += ["left"]
        if pressed[self.right]:
            actions += ["right"]
        if pressed[self.down]:
            actions += ["down"]
        if pressed[self.up]:
            actions += ["up"]

        if "left" in actions and "right" in actions:
            action = "special"
        elif "up" in actions and "down" in actions:
            action = "special 2"
        else:
            action = " ".join(actions)

        return action
        

if __name__ == "__main__":
    pygame.init()
    c = Controller()
    clock = pygame.time.Clock()
    
    while True:
        actions = c.get_actions()
        print(actions)
        clock.tick(60)