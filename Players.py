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
        self.state = Idle(self)
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.speed = 5.0
        self.jump_speed = 10.0

    def move(self):
        self.rect = self.image.get_rect()
        self.x += self.vx
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
            self.state = Rebounding(self)
        elif self.x > self.game.SCREEN_WIDTH - self.rect.width:
            self.x = self.game.SCREEN_WIDTH - self.rect.width
            self.vx = -self.vx
            self.state = Rebounding(self)

        if self.is_supported():
            if self.vy <= 0:
                self.vy = 0.0
        else:
            self.vy -= 1

        self.y += self.vy

        if self.is_supported():
            if isinstance(self.state, Jumping):
                self.state = Ducking(self)

        self.rect.x, self.rect.y = self.x, self.game.SCREEN_HEIGHT - (
            self.y + self.rect.height
        )

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

    def tick(self):
        actions = self.controller.get_inputs()
        for action in actions:
            action()
        self.state.tick()
        self.image = self.state.animation.image
        self.rect = self.image.get_rect()
        self.move()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class PlayerOne(Player):
    def __init__(self, game):
        super().__init__(game, 1, FirstPlayerController, 30, 50, BLUE)


class PlayerTwo:
    def __init__(self, game):
        super().__init__(game, -1, SecondPlayerController, 300, 50, RED)
