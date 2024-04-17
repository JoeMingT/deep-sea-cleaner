from config import *
from extra_functions import bulk_import

class Tile(pygame.sprite.Sprite):
    # pos to tell where which tiles is
    # size to tell how large it needs to be
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)
    
    # To scroll the screen
    # Just move all the sprite to the direction you want
    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
        pass

class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface

class Trash(StaticTile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size, surface)
        self.collected = False
        
    def update(self):
        if self.collected == True:
            self.kill()

class Instructions(StaticTile):
    def __init__(self, pos, size, id):

        path = f"graphics/Images/png files/Instruction {id}.png"
        image = pygame.image.load(path).convert_alpha()

        super().__init__(pos, size, image)

class Diamond(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load("graphics/Objects/diamond.png").convert_alpha())
        offset = pygame.Vector2(0, 0)
        self.rect = self.image.get_rect(topleft = (pos + offset))
        self.collected = False

    def update(self):
        if self.collected == True:
            self.kill()
        
class Bubble(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load("graphics/Objects/bubble.png").convert_alpha())
        self.image.set_alpha(150)
        offset = pygame.Vector2(0, 0)
        self.rect = self.image.get_rect(topleft = (pos + offset))
        self.on_cooldown = False
        self.timer = 3
    
    def update(self):
        if self.on_cooldown == True:
            self.image.set_alpha(0)
            self.timer -= 0.0167
            if self.timer <= 0:
                self.on_cooldown = False
                self.timer = 3
                self.image.set_alpha(255)


class AnimatedTile(Tile):
    # We need the path to the folder with multiple images
    def __init__(self, pos, size, path):
        super().__init__(pos, size)
        self.frames = bulk_import(path)

class Spring(AnimatedTile):
    def __init__(self, pos, size, frames):
        super().__init__(pos, size, "")
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.frames[self.frame_index]

        self.animation = False

    def animate(self):
        if self.animation == True:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.animation = False
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

