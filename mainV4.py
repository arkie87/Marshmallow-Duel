import pygame
from time import time as tic


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (125,125,125)
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
        if pressed[self.down]:
            inputs += ["down"]
        if pressed[self.up]:
            inputs += ["up"]
        if pressed[self.left]:
            inputs += ["left"]
        if pressed[self.right]:
            inputs += ["right"]
            
        return inputs


class Actions:
    """Maps inputs into actions, and applies action rules"""
    def __init__(self, player):
        self.player = player
        
    def do_action(self, inputs):
        if not inputs:
            self.idle()
        elif "left" in inputs and "right" in inputs:
            self.special()
        elif "up" in inputs and "down" in inputs:
            self.special2()
        elif "use" in inputs:
            self.use()
        elif "use2" in inputs:
            self.use2()
        else:
            getattr(self, '_'.join(inputs))()

    def idle(self):
        self.player.vx = 0.0
        self.player.animation = Standing(self.player)
            
    def use(self):
        log("using....")
        
    def up(self):
        if self.player.is_near_rope():
            self.climb(self.player.speed)
        else:
            self.jump()

    def down(self):
        if self.player.is_near_rope():
            self.climb(-self.player.speed)
        else:
            self.duck()
            
    def left(self):
        self.player.animation = Standing(self.player, direction=-1)
        self.player.vx = -self.player.speed
            
    def right(self):
        self.player.animation = Standing(self.player, direction=1)
        self.player.vx = self.player.speed
    
    def up_left(self):
        self.player.animation = Jumping(self.player, -1)
        self.player.vx = -self.player.speed
        self.player.vy = self.player.jump_speed
        
    def up_right(self):
        self.player.animation = Jumping(self.player, 1)
        self.player.vx = self.player.speed
        self.player.vy = self.player.jump_speed
        
    def down_left(self):
        self.player.animation = Rolling(self.player, direction=-1)
        self.player.vx = -1.5*self.player.speed
        
    def down_right(self):
        self.player.animation = Rolling(self.player, direction=1)
        self.player.vx = 1.5*self.player.speed
        
    def climb(self, speed):
        self.player.vx = 0
        self.player.vy = speed
        self.player.animation = Climbing(self.player)
    
    def jump(self):
        self.player.animation = Jumping(self.player)
        self.player.vx = 0.0
        self.player.vy = self.player.jump_speed 
    
    def duck(self):
        self.player.animation = Ducking(self.player)
        
    def special(self):
        log("special!")
        
    def special2(self):
        log("special2!!!")


class Platform:
    Image = None
    
    def init(self):
        image = pygame.Surface((32, 16))
        rect = image.get_rect()
        self.__class__.Nx = Game.SCREEN_WIDTH // rect.width
        self.__class__.Ny = Game.SCREEN_HEIGHT // rect.height
        
        self.__class__.Image = image

    def __init__(self, game, row, col, color=GREEN):
        if self.Image is None:
            self.init()
            
        self.game = game
        self.image = self.Image.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = col * self.rect.width
        self.rect.y = Game.SCREEN_HEIGHT - (row + 1) * self.rect.height
        
    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class Platform2(Platform):
    def __init__(self, game, row, col, color=RED):
        super().__init__(game, row, col, color)


class Map:
    Items = {0: Platform, 1: Platform2}
    def __init__(self, game, object_map):
        self.items = []
        for x, y, i in object_map:
            self.items += [Map.Items[i](game, x, y)]
            
    def draw(self):
        for item in self.items:
            item.draw()


class Animation:
    Frames = {}
    
    def __init__(self, player, direction=0):
        self.player = player
        self.direction = direction
        self.frame = 0
        self.init()
        if not self.Frames:
            self.init_frames()
        
    def init(self):
        self.ready = True
        self.no_frames = 10

    def init_frames(self):
        Image = pygame.image.load(self.Image)
        rect = Image.get_rect()
        Image = pygame.transform.scale_by(Image, Player.SCALE)
        
        self.__class__.Frames = {1:[], -1: [], 0: []}
        for d in self.Frames.keys():
            for i in range(self.no_frames):
                image = Image.copy()
                if d==-1:
                    image = pygame.transform.flip(image, True, False)
                image = pygame.transform.rotate(image, -d * i / self.no_frames * 360)
                image.convert_alpha()
                image.set_colorkey(WHITE)
                self.__class__.Frames[d] += [image]

    def get_frame(self):
        self.player.image = self.Frames[self.direction][self.frame]
        
        if self.frame >= self.no_frames - 1:
            self.reset()
        else:
            self.frame += 1
            
    def reset(self):
        self.player.animation = Standing(self.player, direction=self.direction)


class Climbing(Animation):
    Image = r"D:\Programming\Python\Marshmallow Duel\sprite.png"
    
    def reset(self):
        self.player.animation = Climbing(self.player, direction=self.direction)


class Standing(Animation):
    Image = r"D:\Programming\Python\Marshmallow Duel\sprite.png"
    

class Ducking(Animation):
    Image = r"D:\Programming\Python\Marshmallow Duel\ducking.png"
    
    def init(self):
        self.ready = True
        self.no_frames = 10
        self.player.vx = 0.0


class Jumping(Animation):
    Image = r"D:\Programming\Python\Marshmallow Duel\sprite.png"
    
    def init(self):
        self.ready = False
        self.no_frames = int(2 * self.player.jump_speed / self.player.Gravity)
        
    def get_frame(self):
        self.player.image = self.Frames[self.direction][self.frame]
        
        if self.player.is_supported():
            self.reset()
        
        self.frame = (1 + self.frame) % self.no_frames


class Rolling(Animation):
    Image = r"D:\Programming\Python\Marshmallow Duel\ducking.png"
    
    def init(self):
        self.ready = False
        self.no_frames = 10
        

class Player(pygame.sprite.Sprite):
    SCALE = 2
    Gravity = 1.0
    
    def __init__(self, game, x=30, y=30, player_no=0):
        super().__init__()
        self.game = game
        self.actions = Actions(self)
        self.controller = Controller(player_no=player_no)
        self.animation = Standing(self)
        self.image = self.animation.get_frame()
        if player_no==0:
            self.color = BLUE
        else:
            self.color = RED
        
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.speed = 5.0
        self.jump_speed = 10.0
    
    def move(self):
        self.rect = self.image.get_rect()
    
        self.x += self.vx
        if self.x<0:
            self.x = 0
            self.vx = -self.vx
        elif self.x > Game.SCREEN_WIDTH - self.rect.width:
            self.x = Game.SCREEN_WIDTH - self.rect.width
            self.vx = -self.vx

        if isinstance(self.animation, Climbing):
            print("******************** CLIMBING *******************")

        if self.is_supported() or isinstance(self.animation, Climbing):
            if self.vy <= 0:
                self.vy = 0.0
        else:
            self.vy -= 1
            
        self.y += self.vy
        
        self.rect.x, self.rect.y = self.x, Game.SCREEN_HEIGHT - (self.y + self.rect.height)
        
    def is_near_rope(self):
        if self.x < 10:
            return True
        else:
            return False
            
    def is_supported(self):
        if self.y <= Game.BOTTOM:
            return True
        else:
            return False
        
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        
    def update(self):
        if self.animation.ready:
            inputs = self.controller.get_inputs()
            self.actions.do_action(inputs)
        
        log(self.animation.ready, self.animation.direction, self.vx)
        self.animation.get_frame()
        self.move()


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
        self.players = [Player(self)]#, Player(self, player_no=1)]
        self.map = Map(self, [(0,1,0), (0, 2, 0), (0, 5, 0), (2,2,1), (2,1,0), (2,3,1)])
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
        self.screen.fill(GREY)
        
        self.map.draw()
        
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