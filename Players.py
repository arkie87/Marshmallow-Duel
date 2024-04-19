from Actions import *
from Controllers import *


class Player(pygame.sprite.Sprite):
    SCALE = 2
    Gravity = 1.0

    def __init__(
        self,
        game,
        direction,
        controller,
        x,
        y,
        color,
    ):
        super().__init__()
        self.game = game
        self.direction = direction
        self.controller = controller(self)
        self.color = color
        self.x, self.y = x, y
        self.state = Idle(self)
        self.vx = self.vy = 0.0
        self.speed = 5.0
        self.jump_speed = 15.0

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if direction:
            self._direction = direction

    def tick(self):
        self.state.tick()

        actions = self.controller.get_actions()
        for action in actions:
            action()

        self.image = self.state.animation.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.move()

    def move(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
            self.state.rebound()
        elif self.x > SCREEN_WIDTH - self.rect.width:
            self.x = SCREEN_WIDTH - self.rect.width
            self.vx = -self.vx
            self.state.rebound()

        if self.is_supported():
            if self.vy <= 0:
                self.vy = 0.0
        else:
            self.vy -= 1

        self.y += self.vy

        if self.is_supported():
            if isinstance(self.state, Jumping):
                self.state.landed()

        self.rect.x, self.rect.y = self.x, SCREEN_HEIGHT - (self.y + self.rect.height)

    def is_near_rope(self):
        if self.x < 10:
            return True
        else:
            return False

    def is_supported(self):
        if self.y <= self.game.BOTTOM:
            return True
        else:
            return False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class PlayerOne(Player):
    def __init__(self, game):
        super().__init__(game, 1, FirstPlayerController, 30, 50, BLUE)


class PlayerTwo:
    def __init__(self, game):
        super().__init__(game, -1, SecondPlayerController, 300, 50, RED)
