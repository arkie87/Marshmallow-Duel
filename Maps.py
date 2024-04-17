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