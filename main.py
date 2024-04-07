import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
TROUBLESHOOTING = True


def log(*strings):
    if TROUBLESHOOTING:
        print(*strings)


class Controller:
    def __init__(self, player, number):
        self.player = player
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

    def get_inputs(self):
        actions = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            return ["use"]
        if pressed[self.left]:
            actions += ["left"]
        if pressed[self.right]:
            actions += ["right"]
        if pressed[self.down]:
            actions += ["down"]
        if pressed[self.up]:
            actions += ["up"]

        return actions


class Player(pygame.sprite.Sprite):
    STANDING = pygame.Surface([20, 20])
    DUCKING = pygame.Surface([20, 10])
    
    

    def __init__(self, game, x=30, y=30, player_no=0):
        super().__init__()
        self.game = game
        self.controller = Controller(self, player_no)
        self.image = Player.STANDING
        if player_no==0:
            self.color = BLUE
        else:
            self.color = RED
        
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.speed = 1.0
        self.jump_speed = 10.0
        
    def update(self):
        self.get_states()
        actions = self.controller.get_inputs()
        self.action(actions)
        self.move()

    def get_states(self):
        if self.y == Game.BOTTOM:
            self.is_landed = True
        else:
            self.is_landed = False
            
        if self.vx == 0:
            self.is_moving = False
        else:
            self.is_moving = True
            
    def ready(self):
        self.vx = self.vy = 0.0
            
    def use(self):
        pass
            
    def left(self):
        if not self.is_moving:
            log("moving left")
            self.vx = -self.speed
            
    def right(self):
        if not self.is_moving:
            log("moving right")
            self.vx = self.speed
            
    def up(self):
        if self.is_landed:
            log("moving up")
            self.vy = self.jump_speed
            
    def down(self):
        log("ducking")
        self.image = Player.DUCKING
        self.rect = self.image.get_rect()
        
    def action(self, actions):
        for action in actions:
            Player.ACTIONS[action](self)

    def move(self):
        self.x += self.vx
        if self.x<0:
            self.x = 0
        elif self.x > Game.SCREEN_WIDTH:
            self.x = Game.SCREEN_WIDTH
        
        if not self.is_landed:
            self.vy -= 1
        self.y += self.vy
        if self.y < Game.BOTTOM:
            self.y = Game.BOTTOM
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, Game.SCREEN_HEIGHT - self.y
        
    def draw(self):
        self.image.fill(self.color)
        self.game.screen.blit(self.image, self.rect)
        
        
    ACTIONS = {"use": use,
               "left": left,
               "right": right,
               "up": up,
               "down": down}


class Game:
    FPS = 30
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    BOTTOM = 30
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Arkie's Marshmallow Duel")
        self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.players = [Player(self), Player(self, player_no=1)]
        self.run()
        
    def run(self):
        while True:
            self.check_quit()
            self.update()
            self.draw()
            self.clock.tick(Game.FPS)
            
    def update(self):
        for player in self.players:
            player.update()
            
    def draw(self):
        self.screen.fill(BLACK)
        
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
        

if __name__ == "__main__":
    g = Game()