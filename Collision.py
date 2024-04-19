from Utils import *


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color="green"):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.image)
        self.color = color

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    def tick(self):
        pass

    def draw(self):
        self.image.blit(self.image, (self.rect.x, self.rect.y), self.color)


class StaticObject(Object):
    Objects = []

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

        StaticObject.Objects += [self]


class Floor(StaticObject):
    def do_collisions(self):
        for object in MovingObject.Objects:
            if object.vy < 0 and pygame.sprite.collide_mask(self, object):
                object.rect.bottom = self.rect.top
                

class Bottom(Floor):
    def do_collisions(self):
        for object in MovingObject.Objects:
            if pygame.sprite.collide_mask(self, object):
                object.lose()


class Wall(StaticObject):
    def do_collisions(self):
        for object in MovingObject.Objects:
            if pygame.sprite.collide_mask(self, object):
                if object.vx > 0:
                    object.rect.right = self.rect.left
                else:
                    object.rect.left = self.rect.right

                object.rebound()


class Rope(StaticObject):
    pass


class MovingObject(Object):
    Objects = []

    def __init__(self, x, y, width, height, color="white"):
        super().__init__(x, y, width, height, color)
        self.vx = 0
        self.vy = 0

        MovingObject.Objects += [self]

    def tick(self):
        self.x += self.vx
        self.y += self.vy

    def get_collisions(self):
        static_collisions = []
        for object in StaticObject.Objects:
            if pygame.sprite.collide_mask(self, object):
                static_collisions += [object]

        moving_collisions = []
        for object in MovingObject.Objects:
            if pygame.sprite.collide_mask(self, object):
                moving_collisions += [object]

        return static_collisions, moving_collisions
