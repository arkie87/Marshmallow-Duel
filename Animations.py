from Utils import *


class Animation:
    Frames = 1_000_000
    Images = [pygame.image.load("sprite.png")]

    def __init__(self, state):
        self.frame = 0
        self.state = state
        self.direction = state.player.direction

        self.Image = self.Images[0]

        if self.direction == -1:
            self.Image = pygame.transform.flip(self.Image, flip_x=True, flip_y=False)

        self.image, self.rect = self.get_frame()

    def tick(self):
        self.frame += 1
        self.image, self.rect = self.get_frame()

    def get_frame(self):
        if self.frame <= self.Frames:
            return self.Image, self.Image.get_rect()
        else:
            self.state.end()
            return None, None


class IdleAnimation(Animation):
    pass


class JumpingAnimation(Animation):
    pass


class DuckingAnimation(Animation):
    Frames = 30
    Images = [pygame.image.load("ducking.png")]


class RollingAnimation(DuckingAnimation):
    Frames = 20


class ReboundAnimation(Animation):
    Frames = 20
    Images = [pygame.transform.rotate(Animation.Images[0], 30)]


class WalkingAnimation(Animation):
    Frames = 10


class UsingAnimation(Animation):
    Frames = 40
