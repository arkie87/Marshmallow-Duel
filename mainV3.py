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
    """Defines key bindings and returns inputs"""
    def __init__(self, player_no=0):
        if player_no == 0:
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.down = pygame.K_s
            self.up = pygame.K_w
            self.use = pygame.K_e
            self.use2 = pygame.K_q
        elif player_no == 1:
            self.left = pygame.K_j
            self.right = pygame.K_l
            self.down = pygame.K_k
            self.up = pygame.K_i
            self.use = pygame.K_u
            self.use2 = pygame.K_o

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


class State:
    def __init__(self, player):
        self.player = player
        self.ready = True
        self.direction = 0


class Actions:
    """Maps inputs into actions, and applies action rules"""
    def __init__(self, player):
        self.player = player
        
    def get_action(self):
        inputs = self.player.controller.get_inputs()
        action = self.get_action_from_inputs(inputs)
        return self.apply_action_rules(action)

    def get_action_from_inputs(self, inputs):
        if not inputs:
            action = "idle"
        elif "left" in inputs and "right" in inputs:
            action = "special"
        elif "up" in inputs and "down" in inputs:
            action = "special 2"
        elif "use" in inputs:
            action = "use"
        elif "use2" in inputs:
            action = "use2"
        else:
            action = " ".join(inputs)

        return action

    def apply_action_rules(self, action):
        if not self.player.state.ready:
            return ""
        else:
            return action


class Animation:
    STANDING = pygame.Surface([20, 40])
    DUCKING = pygame.Surface([20, 20])
    SPECIAL = pygame.Surface([10, 40])
    
    def __init__(self):
        self.frame = 0
        self.no_frames = 10
        self.image = Animation.STANDING
        
    def get_image(self):
        self.frame += 1
        
        if self.frame >= self.no_frames:
            self.image = Standing()
            self.player.state.ready = True
        
        
class Jumping(Animation):
    print(__class__ )
    def __init__(self):
    


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=30, y=30, player_no=0):
        super().__init__()
        self.game = game
        self.actions = Actions()
        self.controller = Controller(player_no=player_no)
        self.animation = Animation().STANDING
        if player_no==0:
            self.color = BLUE
        else:
            self.color = RED
        
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.speed = 1.0
        self.jump_speed = 10.0
    
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
            self.actions.state = "ducking"
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, Game.SCREEN_HEIGHT - self.y
        
    def draw(self):
        self.image.fill(self.color)
        self.game.screen.blit(self.image, self.rect)
        
    def update(self):
        inputs = self.controller.get_inputs()
        action = self.actions.get_action_from_inputs(inputs)
        action = self.actions.apply_action_rules(action)
        self.do_action(action)
        log(self.actions.state)
        self.move()
        
    def do_action(self, action):
        if self.actions.state not in {"jumping", "falling", "rolling"}:
            self.vx = 0
            
        Player.ACTIONS[action](self)  # Do actions from hash table
        
    def none(self):
        pass
            
    def ready(self):
        self.vx = self.vy = 0.0
        self.image = Animation.STANDING
            
    def use(self):
        log("using....")
            
    def walk_left(self):
        self.actions.state = "walking"
        self.vx = -self.speed
            
    def walk_right(self):
        self.actions.state = "walking"
        self.vx = self.speed
        
    def up(self):
        # Check for ropes
        self.jump()
            
    def jump(self):
        self.actions.state = "jumping"
        self.vx = 0.0
        self.vy = self.jump_speed
    
    def jump_left(self):
        self.actions.state = "jumping"
        self.vx = -self.speed
        self.vy = self.jump_speed
        
    def jump_right(self):
        self.actions.state = "jumping"
        self.vx = self.speed
        self.vy = self.jump_speed
        
    def roll_left(self):
        self.actions.state = "rolling"
        self.vx = -self.speed
        self.image = Animation.DUCKING
        
    def roll_right(self):
        self.actions.state = "rolling"
        self.vx = self.speed
        self.image = Animation.DUCKING
        
    def duck(self):
        self.actions.state = "rolling"
        
    def special(self):
        self.image = Animation.SPECIAL
        log("special!")
        
    def special2(self):
        log("special2!!!")

    ACTIONS = {"": none,
       "idle": ready,
       "use": use,
       "left": walk_left,
       "right": walk_right,
       "up": up,
       "down": duck,
       "left up": jump_left,
       "right up": jump_right,
       "left down": roll_left,
       "right down": roll_right,
       "special": special,
       "special 2": special2}



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
        self.gameloop()
        
    def gameloop(self):
        self.running = True
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(Game.FPS)
            self.check_quit()
            
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
        self.running = False
        

if __name__ == "__main__":
    g = Game()