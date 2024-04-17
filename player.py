import pygame
from config import *
from extra_functions import bulk_import


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Player Sprites and Animation
        self.directory = "graphics/Player/"
        self.animations = {
            "Death" : [],
            "Idle" : [],
            "Jump" : [],
            "Fall" : [],
            "Land" : [],
            "Run" : []
        }
        self.frame_index = 0
        self.animation_speed = 0.1 
        self.import_player_sprites()


        # Position, Image (Sized properly)
        self.effects_group = pygame.sprite.Group()
        """ 
        Add effects into list (Positioned at player's feet)
        - Always read list
        - Set a timer
        - Timer counts when you run left or right
        - Add effect onto list
        - Effect will stay at position
        - Once finished effect, effect will be destroyed from list
        - Timer stops/resets when you idle
        > Note: First Step will always have unique effect
        > Note: Need to create a condition to check for the first step
        """

        # Player Movement
        # This is how to initialize a vector
        # The first parameter is x position, the second parameter is the y position
        # A Vector2(100, 50) is a vector that moves in the direction of 100 pixels to the right and 50 up (?)
        # Adding this to the rectangle's position will remove the need for us to create 2 variables to handle both x and y
        self.direction = pygame.math.Vector2(0, 0)
        self.state = "Land" # Water or Land
        self.gravity = 0.5
        self.jump_speed = -14
        self.speed = 8

        # Player Mechanics
        self.timer = 1.25
        self.max_time = 1.25
        # self.block = False

        # Player States
        self.action = "Idle"
        self.dead = False
        self.is_bounce = False
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.face_right = True

        # Complex Hitbox
        # Create original rectangle
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        # Create Hitbox Rectangle
        self.hitbox = self.rect.inflate(-20, -20)
        self.offset = pygame.Vector2(10, 20)
        # Get position
        self.pos = pygame.Vector2(self.rect.topleft)

    def import_player_sprites(self):
        for animation_type in self.animations.keys():
            full_path = self.directory + animation_type
            image_list = bulk_import(full_path)
        
            for image in image_list:
                scaled_img = pygame.transform.scale(image, (TILE_SIZE*2, TILE_SIZE*2))
                self.animations[animation_type].append(scaled_img)


    def animate(self):
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.action]):
            if self.action == "Jump" or self.action == "Fall":
                self.frame_index = len(self.animations[self.action]) - 1 
            else:
                self.frame_index = 0
        
        image = self.animations[self.action][int(self.frame_index)]
        if self.face_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # # Create a new rect (To create a more complex collision system)
        # if self.on_ground:
        #     self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #     self.rect = self.image.get_rect(center = self.rect.center)

    def play_death_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.action]):
            self.frame_index = len(self.animations[self.action]) - 1

        self.image = self.animations[self.action][int(self.frame_index)]
        

    def get_action(self):
        # if self.dead == False:
            if self.direction.y < 0:
                self.action = "Jump"
            # If the direction.y is >0 it will cause a problem
            # As the program continuously cycles between falling, idling and running
            # This is because our character's direction is never equals to 0
            # And we reset it to 0 when it's more than a certain amount
            # Hence it will cycle between 0 and 0.2 (on the ground when we reset), causing it to run both sides
            elif self.direction.y > 1:
                self.action = "Fall"
            else:
                if self.direction.x != 0:
                    self.action = "Run"
                else:
                    self.action = "Idle"

    # This time we'll use vector
    # Instead of the traditional rect.x += 1
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            # We add 1 to x if we moving right
            self.direction.x = 1
            self.face_right = True
        elif keys[pygame.K_LEFT]:
            # -1 if left
            self.direction.x = -1
            self.face_right = False
        else:
            self.direction.x = 0

        # if keys[pygame.K_SPACE]:
        #     self.jump()

    def countdown_timer(self):
        if self.timer >= 0:
            self.timer -= 0.0167
        else:
            self.change_state()
            # self.block = True

    def regenerate_time(self):
        self.timer += 0.015
        if self.timer >= self.max_time:
            self.timer = self.max_time
            # self.block = False

    def change_state(self):
        # self.direction.y = 0
        if self.state == "Water":
            self.state = "Land"
            SFX.change_state2.play()
        elif self.state == "Land":  # and self.block == False
            self.state = "Water"
            SFX.change_state.play()
    
    def change_movement(self):
        if self.is_bounce == False:
            if self.state == "Water":
                self.speed -= 0.08
                if self.speed <= 3:
                    self.speed = 3

                self.gravity -= 0.5
                if self.gravity <= 0.3:
                    self.gravity = 0.3

                self.jump_speed += 2
                if self.jump_speed >= -4:
                    self.jump_speed = -4 

            elif self.state == "Land":
                self.speed += 1
                if self.speed >= 8:
                    self.speed = 8

                self.gravity += 1
                if self.gravity >= 0.5:
                    self.gravity = 0.5

                self.jump_speed -= 1 
                if self.jump_speed <= -10:
                    self.jump_speed = -10

        else:
            if self.state == "Land":
                self.direction.y = -16
                self.is_bounce = False
                
            
            elif self.state == "Water":
                self.direction.y = -10
                self.is_bounce = False
        
    def apply_gravity(self):
        # if self.dead == False:
            if self.state == "Land":
                self.direction.y += self.gravity

            elif self.state == "Water":
                self.direction.y += self.gravity
                if self.direction.y >= 5:
                    self.direction.y = 5
            # Update position
            self.pos.y += self.direction.y 
            # Then use position to update both image rectangle and hitbox rectangle
            self.rect.y = self.pos.y
            self.hitbox.y = self.offset.y + self.pos.y

    def jump(self):
        if self.state == "Land" and self.on_ground == True:
            SFX.jump.play()
            self.direction.y = self.jump_speed
            
        elif self.state == "Water":
            SFX.jump.play()
            self.direction.y = self.jump_speed

    def bounce(self):
        self.is_bounce = True

    def update(self):
        self.get_input()
        self.animate()
        self.get_action()

        # Then update it by adding the vector's x pos multiplied with speed/velocity of player
        # with the rectangle's x
        # self.rect.x += self.direction.x * self.speed 
        # self.apply_gravity() 
        
        if self.state == "Water":
            self.countdown_timer()
        elif self.state == "Land":
            self.regenerate_time()

        self.change_movement()


# Water mode > Add a timer (More like an Energy Meter that takes time to recharge) -> To avoid state switching exploit thingy
# Land Mode > Do something to make more OP (Also refreshes the water mode timer)
        
