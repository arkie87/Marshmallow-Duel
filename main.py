from Players import *


class Game:
    FPS = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    BOTTOM = 30

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Arkie's Marshmallow Duel")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.players = [PlayerOne(self)]  # , Player(self, player_no=1)]
        # self.map = Map(self, [(0, 1, 0), (0, 2, 0), (0, 5, 0), (2, 2, 1), (2, 1, 0), (2, 3, 1)])
        self.gameloop()

    def gameloop(self):
        self.running = True
        while self.running:
            self.tick()
            self.draw()
            self.clock.tick(Game.FPS)
            self.check_quit()

    def tick(self):
        for player in self.players:
            player.tick()

    def draw(self):
        self.screen.fill(GREY)

        # self.map.draw()

        for player in self.players:
            player.draw()

        pygame.display.flip()

    def check_quit(self):
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                self.quit()

    def quit(self):
        pygame.quit()
        self.running = False
        exit(0)


if __name__ == "__main__":
    g = Game()
