from Utils import *


class Animation:
    Frames = 1_000_000
    Image = pygame.image.load("sprite.png")

    def __init__(self, direction):
        self.frame = 0
        self.direction = direction
        self.image = self.Image
        self.rect = self.image.get_rect()

    def tick(self):
        self.frame += 1
        if self.frame <= self.Frames:
            self.image = self.next_frame()
            self.rect = self.image.get_rect()
            return True

    def next_frame(self):
        return self.Image


class IdleAnimation(Animation):
    pass


class JumpingAnimation(Animation):
    pass


class DuckingAnimation(Animation):
    Frames = 10


class RollingAnimation(Animation):
    Frames = 20


class ReboundAnimation(Animation):
    Frames = 20


class WalkingAnimation(Animation):
    Frames = 10


class UsingAnimation(Animation):
    Frames = 40
