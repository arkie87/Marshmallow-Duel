import pygame
from time import time as tic


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
TROUBLESHOOTING = True


def log(*strings):
    if TROUBLESHOOTING:
        print(*strings)


class Controller:
    def __init__(self, player_no=0):
        if player_no == 0:
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.down = pygame.K_s
            self.up = pygame.K_w
            self.use = pygame.K_e
        elif player_no == 1:
            self.left = pygame.K_j
            self.right = pygame.K_l
            self.down = pygame.K_k
            self.up = pygame.K_i
            self.use = pygame.K_u

    def get_inputs(self):
        inputs = []
        pressed = pygame.key.get_pressed()
        if pressed[self.use]:
            inputs += ["use"]
        if pressed[self.left]:
            inputs += ["left"]
        if pressed[self.right]:
            inputs += ["right"]
        if pressed[self.down]:
            inputs += ["down"]
        if pressed[self.up]:
            inputs += ["up"]
            
        return inputs


class Action:
    def __init__(self, player):
        self.player = player
        self.state = "idle"
        self.direction = "none"
        self.start_time = None
        
    @property
    def state(self):
        return self._state
        
    @state.setter
    def state(self, state):
        self._state = state
        self.start_time = tic()
        
    def get_action(self, inputs):
        if "left" in inputs and "right" in inputs:
            action = "special"
        elif "up" in inputs and "down" in inputs:
            action = "special 2"
        else:
            action = " ".join(inputs)

        return action
        
    def action_rules(self, action):
        if self.state in {"idle", "walking", "ducking"}:
            return action
        else:
            return ""
            
    def do_action(self, action):
        if self.state not in {"jumping", "falling", "rolling"}:
            self.player.vx = 0
            
        Action.ACTIONS[action](self)  # Do actions from hash table
            
    def ready(self):
        self.vx = self.vy = 0.0
            
    def use(self):
        log("using....")
            
    def left(self):
        self.state = "walking"
        self.player.vx = -self.player.speed
            
    def right(self):
        self.state = "walking"
        self.player.vx = self.player.speed
            
    def up(self):
        self.state = "jumping"
        self.player.vy = self.player.jump_speed
    
    def jump_left(self):
        self.left()
        self.up()
        
    def jump_right(self):
        self.right()
        self.up()
        
    def roll_left(self):
        self.left()
        self.roll()
        
    def roll_right(self):
        self.right()
        self.roll()
        
    def roll(self):
        self.state = "rolling"
        self.player.image = Player.DUCKING
        
    def special(self):
        log("special!")
        
    def special2(self):
        log("special2!!!")
    
    ACTIONS = {"": ready,
           "use": use,
           "left": left,
           "right": right,
           "up": up,
           "down": roll,
           "left up": jump_left,
           "right up": jump_right,
           "left down": roll_left,
           "right down": roll_right,
           "special": special,
           "special 2": special2}


class Player(pygame.sprite.Sprite):
    STANDING = pygame.Surface([20, 20])
    DUCKING = pygame.Surface([20, 10])

    def __init__(self, game, x=30, y=30, player_no=0):
        super().__init__()
        self.game = game
        self.state = Action(self)
        self.controller = Controller(player_no=player_no)
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
        inputs = self.controller.get_inputs()
        action = self.state.get_action(inputs)
        action = self.state.action_rules(action)
        self.state.do_action(action)
        log(self.state.state)
        self.move()

    def move(self):
        self.x += self.vx
        if self.x<0:
            self.x = 0
        elif self.x > Game.SCREEN_WIDTH:
            self.x = Game.SCREEN_WIDTH
        
        self.vy -= 1
        self.y += self.vy
        if self.y < Game.BOTTOM:
            self.y = Game.BOTTOM
            self.vy = 0.0
            self.state.state = "idle"
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, Game.SCREEN_HEIGHT - self.y
        
    def draw(self):
        self.image.fill(self.color)
        self.game.screen.blit(self.image, self.rect)
        
        



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