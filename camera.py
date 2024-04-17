import pygame
from config import *

# Referenced (Or pretty much copied cus I suck) from:
# https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame


# We can't use the .draw function of the sprite group
# sprite doesn't need to know their position is not the position they are going to be drawn on screen


# Create a class called Camera which will handle all camera movements
class Camera():
    # Width being width of the whole level
    # Height being height of the whole level
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        # self.state is to hold the state of the offset
        self.state = pygame.Rect(0, 0, width, height)

    def scroll(self, target):
        return target.rect.move(self.state.topleft)

    # Once per iteration of the loop, we need to update the position of the camera
    # Hence the update() function
    # It will alter the state by calling the "camera_func" function (Explain later)
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    # We need to store the posiiton of the camera, 
    # the width and height of the whole level (in pixels) to prevent scrolling off the edge.
    # So we will store the value in a Rect object (Which simplifies the process)


# Now we create camera_func
# camera_func is basically different ways the camera will behave

# simple_camera:
# First parameter: Takes the camera's rect and get the width and height (So it's constantly same size as screen)
# Second parameter: Takes the target's rect (Player, Enemy, anything) and get it's x, y position
def simple_camera(camera, target_rect):
    left, top, _, __ = target_rect
    _, __, width, height = camera
    # Returns a Rect object that stores the new position of the camera
    return pygame.Rect(-left + WIDTH/2, -top + HEIGHT/2, width, height)


def complex_camera(camera, target_rect):

    x = -target_rect.center[0] + WIDTH/2
    y = -target_rect.center[1] + HEIGHT/2
    displacement = pygame.Vector2((x, y))

    # This will make the screen move with more smoothness (Not as static as simple_camera)
    camera.topleft += ( displacement - pygame.Vector2(camera.topleft) ) *  1
    # Then set the maximum and minimum x and y position so can prevent seeing outside the world
    camera.x = max( -(camera.width - WIDTH), min(0, camera.x) )
    camera.y = max( -(camera.height - HEIGHT), min(0, camera.y) )

    # Return the new camera Rect object
    return camera

# Playing around with stupid stuff don't worry about this camera_func
def static_camera(camera, target_rect):

    x = -target_rect.center[0] + WIDTH/2
    y = -target_rect.center[1] + HEIGHT/2
    displacement = pygame.Vector2((x, y))

    # Changing the multiply value (0.0000001) value will change the scroll speed
    # Changing the displacement value (pygame.Vector2((x, y))) will change where the camera pans
    camera.topleft += displacement - (pygame.Vector2(camera.topleft) * 0.0000001)
    camera.x = max(-(camera.width - WIDTH), min(0, camera.x))
    camera.y = max(-(camera.height - HEIGHT), min(0, camera.y))

    # Return the new camera Rect object
    return camera


""" 
Note: You can move these functions into the class itself
      But for simplicity sake, it'll be seperated
"""
