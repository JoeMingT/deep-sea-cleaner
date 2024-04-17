import pygame

pygame.mixer.init()



class SoundEffects:
    def __init__(self):
        self.bubble = pygame.mixer.Sound("audio/sfx/bubble.wav") # Higher
        self.confirm = pygame.mixer.Sound("audio/sfx/confirm.ogg") # Lower
        self.cancel = pygame.mixer.Sound("audio/sfx/cancel.ogg") # lower a bit  
        self.death = pygame.mixer.Sound("audio/sfx/death.ogg")
        self.jump = pygame.mixer.Sound("audio/sfx/jump.ogg") # Lower
        self.change_state = pygame.mixer.Sound("audio/sfx/change_state.wav") # Higher a bit
        self.change_state2 = pygame.mixer.Sound("audio/sfx/change_state2.wav") # Higher a bit
        self.move_arrow = pygame.mixer.Sound("audio/sfx/move_arrow.wav")
        self.trash_collected = pygame.mixer.Sound("audio/sfx/trash_collected.wav") # Higher a bit
        self.diamond_collected = pygame.mixer.Sound("audio/sfx/diamond_collected.ogg")
        self.spring = pygame.mixer.Sound("audio/sfx/spring.ogg")
        self.victory = pygame.mixer.Sound("audio/sfx/victory.wav")

    def change_audio(self, volume):
        self.bubble.set_volume(volume)
        self.confirm.set_volume(volume)
        self.cancel.set_volume(volume)
        self.death.set_volume(volume)
        self.jump.set_volume(volume)
        self.change_state.set_volume(volume)
        self.change_state2.set_volume(volume)
        self.move_arrow.set_volume(volume)
        self.trash_collected.set_volume(volume)
        self.diamond_collected.set_volume(volume)
        self.spring.set_volume(volume)
        self.victory.set_volume(volume)

class Music:
    def __init__(self):
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel3 = pygame.mixer.Channel(2)
        self.music = pygame.mixer.Sound("audio/music/bgm.wav") # Lower
        self.music2 = pygame.mixer.Sound("audio/music/bgm2.wav") # Lower
        self.ambience = pygame.mixer.Sound("audio/music/ambience.wav") # Lower a bit

    def change_audio(self, volume):
        self.channel1.set_volume(volume)
        self.channel2.set_volume(volume)
        self.channel3.set_volume(volume)
