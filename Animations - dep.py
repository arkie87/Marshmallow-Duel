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
        

