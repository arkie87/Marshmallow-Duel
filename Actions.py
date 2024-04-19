from Animations import *


class State:
    def __init__(self, player, direction=0, vx=0, vy=0):
        self.player = player
        self.player.direction = direction
        self.player.vx, self.player.vy = vx, vy
        self.animation = self.Animation(self)

    def __repr__(self):
        return f"{self.__class__.__name__}, {self.player.vx}, {self.player.vy}"

    def tick(self):
        self.animation.tick()
        if not self.animation.image:
            self.end()
        print(self)

    def end(self):
        self.player.state = Idle(self.player, self.player.direction)

    def rebound(self):
        self.player.state = Rebounding(
            self.player, vx=self.player.vx, vy=self.player.jump_speed / 2
        )

    def landed(self):
        self.player.state = Landing(self.player, self.player.direction)

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

    def use(self):
        self.player.state = Use(self.player)

    def left(self):
        self.player.state = Walking(self.player, direction=-1, vx=-self.player.speed)

    def right(self):
        self.player.state = Walking(self.player, direction=1, vx=self.player.speed)

    def down(self):
        self.player.state = Ducking(self.player)

    def up(self):
        self.player.state = Jumping(
            self.player, vx=self.player.vx, vy=self.player.jump_speed
        )


class Walking(Idle):
    Animation = WalkingAnimation

    def left(self):
        pass

    def right(self):
        pass

    def down(self):
        self.player.state = Rolling(self.player, vx=self.player.vx)


class Rolling(State):
    Animation = RollingAnimation


class Ducking(State):
    Animation = DuckingAnimation

    def left(self):
        print("rolling left")
        self.player.state = Rolling(self.player, vx=-self.player.speed, direction=-1)
        print(self.player.state)

    def right(self):
        print("rolling right")
        self.player.state = Rolling(self.player, vx=self.player.speed, direction=1)
        print(self.player.state)


class Landing(State):
    Animation = LandingAnimation


class Jumping(State):
    Animation = JumpingAnimation


class Use(State):
    Animation = UsingAnimation


class Rebounding(State):
    Animation = ReboundAnimation
