from Animations import *


class State:
    def __init__(self, player):
        self.player = player
        self.animation = self.Animation(self.player.direction)

    def tick(self):
        if not self.animation.tick():
            self.player.state = Idle(self.player)
        print(self)

    def use(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def up(self):
        pass

    def down(self):
        pass


class Idle(State):
    Animation = IdleAnimation

    def __init__(self, player):
        super().__init__(player)
        self.player.vx = 0

    def use(self):
        self.player.state = Use(self.player)

    def left(self):
        self.player.direction = -1
        self.player.vx = -self.player.speed
        self.player.state = Moving(self.player)

    def right(self):
        self.player.direction = 1
        self.player.vx = self.player.speed
        self.player.state = Moving(self.player)

    def down(self):
        self.player.state = Ducking(self.player)

    def up(self):
        self.player.state = Jumping(self.player)


class Moving(Idle):
    Animation = WalkingAnimation

    def __init__(self, player):
        State.__init__(self, player)

    def left(self):
        pass

    def right(self):
        pass

    def down(self):
        self.player.state = Rolling(self.player)


class Rolling(State):
    Animation = RollingAnimation


class Ducking(Idle):
    Animation = DuckingAnimation

    def left(self):
        self.player.direction = -1
        self.player.vx = -self.player.speed
        self.player.state = Rolling(self.player)

    def right(self):
        self.player.direction = 1
        self.player.vx = self.player.speed
        self.player.state = Rolling(self.player)


class Jumping(State):
    Animation = JumpingAnimation

    def __init__(self, player):
        State.__init__(self, player)
        self.player.vy = self.player.jump_speed


class Use(State):
    Animation = UsingAnimation


class Rebounding(State):
    Animation = ReboundAnimation


if __name__ == "__main__":
    import pygame

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Arkie's Marshmallow Duel")

    while True:

        screen.fill((0, 255, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            # check if the event is the X button
            if event.type == pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_e] or pressed[pygame.K_q]:
            p.use()
        if pressed[pygame.K_a]:
            p.left()
        if pressed[pygame.K_d]:
            p.right()
        if pressed[pygame.K_w]:
            p.up()
        if pressed[pygame.K_s]:
            p.down()

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit(0)

        p.tick()

        clock.tick(60)
