import pygame
from extra_functions import bulk_import

class Effects(pygame.sprite.Sprite):
    def __init__(self, action):
        self.effects_path = "/graphics/Effects/"
        super().__init__()
        
        self.action = action
        self.import_effects()

        self.frame_index = 0
        self.animation_speed = 0.3

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()

    def import_effects(self):
        full_path = self.effects_path + self.action
        self.animations = bulk_import(full_path)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.kill()
        
        image = self.animations[self.frame_index]
        

    def update(self):
        self.animate()
