from Utils import *


def mirror(images):
    return [pygame.transform.flip(image, True, False) for image in images]


class Animation:
    def __init__(self, state):
        self.frame = 0
        self.state = state
        self.direction = state.player.direction

        if self.direction == 1:
            self.Image = self.ImageR
        else:
            self.Image = self.ImageL

        self.image, self.rect = self.get_frame()

    def mirror(self):
        self.__class__.ImageL = [pygame.transform.flip(image) for image in self.ImageR]

        self.__class__.ImageL = pygame.transform.flip(
            self.__class__.ImageR, True, False
        )

    def tick(self):
        self.image, self.rect = self.get_frame()

    def get_frame(self):
        if self.frame < len(self.ImageR):
            return self.Image[self.frame], self.Image[self.frame].get_rect()
        else:
            return None, None


class IdleAnimation(Animation):
    ImageR = [pygame.image.load("player1-idle.png").convert_alpha()]
    ImageL = mirror(ImageR)


class JumpingAnimation(IdleAnimation):
    pass


class WalkingAnimation(IdleAnimation):
    ImageR = IdleAnimation.ImageR * 10
    ImageL = mirror(ImageR)

    def tick(self):
        self.frame += 1
        super().tick()


class DuckingAnimation(WalkingAnimation):
    ImageR = [pygame.image.load("player1-ducking.png").convert_alpha()] * 10
    ImageL = mirror(ImageR)


class LandingAnimation(WalkingAnimation):
    ImageR = [pygame.image.load("player1-ducking.png").convert_alpha()] * 5
    ImageL = mirror(ImageR)


class RollingAnimation(WalkingAnimation):
    ImageR = [
        pygame.transform.rotate(DuckingAnimation.ImageR[0], -i * 360 / 20)
        for i in range(21)
    ]
    ImageL = mirror(ImageR)


class ReboundAnimation(WalkingAnimation):
    ImageR = [
        pygame.transform.rotate(image, 30) for image in WalkingAnimation.ImageR
    ] * 2
    ImageL = mirror(ImageR)


class UsingAnimation(WalkingAnimation):
    Frames = 40
