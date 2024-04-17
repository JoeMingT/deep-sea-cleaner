import pygame
from config import *


class Bar(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        super().__init__()
        self.image = pygame.image.load("graphics/Objects/health_bar.png").convert_alpha()
        self.bar_size = (78, 3)
        self.rect = self.image.get_rect(topleft = player_pos)
        self.pos = pygame.Vector2(player_pos)
        self.offset = pygame.Vector2(-10, -5)
        
    
    def update(self, player_pos, progress):
        if self.bar_size[0] * progress != self.bar_size[0]:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        self.pos = player_pos
        self.rect.topleft = self.pos + self.offset


class InnerBar(Bar):
    def __init__(self, player_pos):
        super().__init__(player_pos)
        self.bar_size = (78, 3)
        self.image = pygame.Surface(self.bar_size, flags=pygame.SRCALPHA)
        self.image.fill("Green") 
        self.rect = self.image.get_rect(topleft = player_pos)
        self.pos = pygame.Vector2(player_pos)
        self.offset = pygame.Vector2(-8,-3)

    def update(self, player_pos, progress):
        if self.bar_size[0] * progress != self.bar_size[0] and progress > 0:
            self.image = pygame.Surface((self.bar_size[0] * progress, self.bar_size[1]), flags = pygame.SRCALPHA)
            self.image.fill("Green")
        else:
            self.image.set_alpha(0)
        self.pos = player_pos
        self.rect.topleft = self.pos + self.offset
        


#  # https://stackoverflow.com/questions/54502683/how-can-i-display-a-smooth-loading-bar-in-pygame

#     def draw_bar(self, pos, size, border_color, bar_color, progress):
#         pygame.draw.rect(SCREEN, border_color, (pos, size), 1)
#         inner_bar_pos = (pos[0] + 3, pos[1] + 3)
#         inner_bar_size = ((size[0]-6) * progress, size[1]-6)
#         pygame.draw.rect(SCREEN, bar_color, (inner_bar_pos, inner_bar_size))


class HUD:
    def __init__(self):
        self.time = 0
        self.start_time = pygame.time.get_ticks()
        self.stored_time = 0

        self.pause_button = pygame.transform.scale(pygame.image.load("graphics/GUI/esc_key.png").convert_alpha(), (40, 40))
        self.pause_text = EXPRESSION_PRO.render("Pause", 0, WHITE)

    def update_time(self):
        self.time = pygame.time.get_ticks() - self.start_time + self.stored_time
        self.time_text = EXPRESSION_PRO.render(f"Time: {(self.time / 1000):.2f}s", 0, WHITE)

    def store_time(self):
        self.stored_time = self.time

    def update_start_time(self):
        self.start_time = pygame.time.get_ticks()
    
    def draw(self):
        self.update_time()
        SCREEN.blit(self.time_text, (WIDTH/2 - self.time_text.get_width()/2, HEIGHT/8 - self.time_text.get_height()/2))
        SCREEN.blit(self.pause_button, (WIDTH/16 - self.pause_button.get_width()/2, HEIGHT/9 - self.pause_button.get_height()/2))
        SCREEN.blit(self.pause_text, (WIDTH/16 + self.pause_button.get_width(), HEIGHT/9 - self.pause_text.get_height()/2 ))