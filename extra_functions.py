from os import walk
import pygame
from config import *
# Allows us to work use CSV files (Which is where all the Tiled data is sored)
# reader allows us to read the file (We don't need any other functions to write or anything else)
from csv import reader

def bulk_import(path):
    frames_list = []
    for _, __, img_files in walk(path):
        for sprite in img_files:
            frames_list.append( pygame.image.load(path + "/" + sprite).convert_alpha() )

    return frames_list

# We need to import the CSV as readable data in Pygame
# Then, import the images / tilesets used in Tiled (Sliced it)
# Finally, use the data to place the images in the correct location
def import_csv_layout(path):
    layer_layout = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            layer_layout.append(list(row))
    return layer_layout


def import_cut_tiles(alpha, path):
    image = pygame.image.load(path).convert_alpha()
    num_of_horizontal_tiles = int(image.get_width() / TILE_SIZE)
    num_of_vertical_tiles = int(image.get_height() / TILE_SIZE)

    sliced_tiles = []
    for row in range(num_of_vertical_tiles):
        for col in range(num_of_horizontal_tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            # flags = pygame.SRCALPHA will copy the transparency to the game itself
            temp_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags = pygame.SRCALPHA)
            # The third parameter determines the specific area you want to blit onto (rect object)
            temp_surf.blit(image, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            temp_surf.set_alpha(alpha)
            sliced_tiles.append(temp_surf)
    
    return sliced_tiles


