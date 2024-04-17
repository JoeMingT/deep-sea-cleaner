import pygame
from tile import *
from player import Player
from camera import *
from extra_functions import import_csv_layout, import_cut_tiles
from random import randint, choice
from hud import *
from menu import GameOverMenu, PauseMenu, VictoryMenu

class Level:
    # Level_data so that you can pass different level layouts
    # surface is the surface you will draw on
    def __init__(self, level_json, surface, user_json, level_id):
        self.display_surface = surface
        self.completion_req = 0
        self.collected_diamond = False
        self.trash_collected = 0
        self.level_clear = False

        self.user_json = user_json
        self.user_data = self.user_json.data
        self.level_id = level_id

        self.level_json = level_json
        self.level_data = self.level_json.data[f"level_{level_id}"]

        self.presets = self.level_data["Presets"]

        # self.tile_group = pygame.sprite.Group()
        # self.player_group = pygame.sprite.GroupSingle()

        self.import_tiles_assets()

        self.create_level(self.level_data)

        # self.create_level(level_data)

        # self.world_scroll_x = 0
        # self.world_scroll_y = 0

        # self.player_group.add(Player((100, 100)))

        self.camera = Camera(complex_camera, self.level_width, self.level_height)

        self.bar_group = pygame.sprite.Group()
        self.bar_group.add(Bar(self.player_group.sprite.pos))
        self.bar_group.add(InnerBar(self.player_group.sprite.pos))

        self.game_over_screen = GameOverMenu()

        self.hud = HUD()

        self.is_paused = False
        self.pause_menu = PauseMenu()

        self.victory = False
        self.victory_menu = VictoryMenu()


    def import_tiles_assets(self):
        self.terrain_tile_list = import_cut_tiles(255, f"level data/finalized tilesets png/Tileset{self.presets['tileset_type']}.png")
        # self.scaffolding_tile_list = import_cut_tiles(255, "level data/finalized tilesets png/Scaffolding.png")
        self.decorations_tile_list = import_cut_tiles(255, f"level data/finalized tilesets png/Tileset{self.presets['tileset_type']}.png")
        self.spikes_tile_list = import_cut_tiles(255, f"level data/finalized tilesets png/Spikes Type {self.presets['spike_type']}.png")
        self.spring_tile_list = import_cut_tiles(255, "level data/finalized tilesets png/Spring.png")
        self.trash_tile_list = import_cut_tiles(255, "level data/finalized tilesets png/Trash.png")
        self.player_tile_list = import_cut_tiles(255, "level data/finalized tilesets png/Player Setup.png")
        self.water_tile_list = import_cut_tiles(100, "level data/finalized tilesets png/Water.png")

    # First parameter: To get the layout for that layer
    # Second parameter: To specify which type of layer we are targeting
    def create_tile_group(self, layer_layout, type):
        sprite_group = pygame.sprite.Group()
        self.level_width = len(layer_layout[0] * TILE_SIZE)
        self.level_height = len(layer_layout * TILE_SIZE)

        for row_index, row in enumerate(layer_layout):
            for col_index, col in enumerate(row):
                # Make sure it's a string, not an integer (As CSV import files are imported as strings)
                if col != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == "Terrain":
                        terrain_surf = self.terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), TILE_SIZE, terrain_surf)
                    
                    # if type == "Scaffolding":
                    #     scaffolding_surf = self.scaffolding_tile_list[int(col)]
                    #     sprite = StaticTile((x, y), TILE_SIZE, scaffolding_surf)

                    # Empty For now
                    if type == "Decorations":
                        decorations_surf = self.decorations_tile_list[int(col)]
                        sprite = StaticTile((x, y), TILE_SIZE, decorations_surf)

                    if type == "Spikes":
                        spikes_surf = self.spikes_tile_list[int(col)]
                        sprite = StaticTile((x, y), TILE_SIZE, spikes_surf)

                    if type == "Spring":
                        sprite = Spring((x, y), TILE_SIZE, self.spring_tile_list)

                    if type == "Diamond":
                        sprite = Diamond((x, y), TILE_SIZE)

                    if type == "Bubble":
                        sprite = Bubble((x, y), TILE_SIZE)
                    
                    if type == "Water":
                        water_surf = self.water_tile_list[int(col)]
                        sprite = StaticTile((x, y), TILE_SIZE, water_surf)

                    if type == "Instructions":
                        sprite = Instructions((x, y), TILE_SIZE, col)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                # Make sure it's a string, not an integer (As CSV import files are imported as strings)
                if col != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    if col == '0':
                        self.player_group.add(Player((x, y)))
                    if col == '1':
                        self.completion_req += 1
                        end_surface = self.trash_tile_list[randint(0,2)]
                        sprite = Trash((x, y), TILE_SIZE, end_surface)
                        self.goal_group.add(sprite)                    

    

    def create_level(self, level_data):
        terrain_layout = import_csv_layout(level_data["Terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "Terrain")

        # scaffolding_layout = import_csv_layout(level_data["Scaffolding"])
        # self.scaffolding_sprites = self.create_tile_group(scaffolding_layout, "Scaffolding")

        decorations_layout = import_csv_layout(level_data["Decorations"])
        self.decorations_sprites = self.create_tile_group(decorations_layout, "Decorations")
        
        spikes_layout = import_csv_layout(level_data["Spikes"])
        self.spikes_sprites = self.create_tile_group(spikes_layout, "Spikes")

        spring_layout = import_csv_layout(level_data["Spring"])
        self.spring_sprites = self.create_tile_group(spring_layout, "Spring")
        
        diamond_layout = import_csv_layout(level_data["Diamond"])
        self.diamond_sprites = self.create_tile_group(diamond_layout, "Diamond")
        
        bubble_layout = import_csv_layout(level_data["Bubble"])
        self.bubble_sprites = self.create_tile_group(bubble_layout, "Bubble")

        player_layout = import_csv_layout(level_data["Player"])
        self.player_group = pygame.sprite.GroupSingle()
        self.goal_group = pygame.sprite.Group()
        self.player_setup(player_layout)

        water_layout = import_csv_layout(level_data["Water"])
        self.water_sprites = self.create_tile_group(water_layout, "Water")
        
        instructions_layout = import_csv_layout(level_data["Instructions"])
        self.instructions_sprites = self.create_tile_group(instructions_layout, "Instructions")

        background = [ "far.png", "background.png" ]
        self.background = pygame.transform.scale(pygame.image.load(f"level data/background/{choice(background)}").convert(), (WIDTH, HEIGHT))
        self.background.set_alpha(150)

        foreground = ["foregound-merged.png", "foreground-1.png", "foreground-2.png"]
        self.foreground = pygame.transform.scale(pygame.image.load(f"level data/background/{choice(foreground)}").convert_alpha(), (WIDTH, HEIGHT))
        self.foreground.set_alpha(150)


    ###################### Not In Use ##########################
    # def scroll_x(self):
    #     # player Class 
    #     player = self.player_group.sprite
    #     # the x_posiiton in center
    #     player_x = player.rect.centerx
    #     # The direction of the vector
    #     direction_x = player.direction.x

    #     # We will give the illusion of scrolling
    #     # When the player reaches a border, we will stop him in place
    #     # Instead we move the background with the same speed as the player
    #     # This gives off a similar feeling of scrolling through a map

    #     # As without direction.x, the player will be stuck on <200 x pos
    #     # Hence it will keep on scrolling and will be stuck
    #     # Adding direction.x (That changes depending on input) as a condition
    #     # will make sure that the screen will scroll when the player has an input
    #     if player.state == "Land":
    #         if player_x < WIDTH/4 and direction_x < 0:
    #             self.world_scroll_x = 8
    #             player.speed = 0
    #         elif player_x > WIDTH - WIDTH/4 and direction_x > 0:
    #             self.world_scroll_x = -8
    #             player.speed = 0
    #         else:
    #             self.world_scroll_x = 0
    #             player.speed = 8
    #     else:
    #         if player_x < WIDTH/4 and direction_x < 0:
    #             self.world_scroll_x = 4
    #             player.speed = 0
    #         elif player_x > WIDTH - WIDTH/4 and direction_x > 0:
    #             self.world_scroll_x = -4
    #             player.speed = 0
    #         else:
    #             self.world_scroll_x = 0
    #             player.speed = 4

    def check_victory(self):
        if self.trash_collected == self.completion_req:
            SFX.victory.play()
            self.level_clear = True
            

    def spring_collision(self):
        player = self.player_group.sprite

        for spring in self.spring_sprites:
            if spring.rect.collidepoint(player.hitbox.center):
                SFX.spring.play()
                player.bounce()
                spring.animation = True
                

    def spike_collision(self):
        player = self.player_group.sprite

        for spikes in self.spikes_sprites:
            if spikes.rect.collidepoint(player.hitbox.center):
                SFX.death.play()
                player.dead = True
                player.action = "Death"
                player.frame_index = 0

    def bubble_collision(self):
        player = self.player_group.sprite

        for bubbles in self.bubble_sprites:
            if bubbles.rect.collidepoint(player.hitbox.center):
                if bubbles.on_cooldown == False:
                    player.timer = player.max_time
                    bubbles.on_cooldown = True
                    SFX.bubble.play()

    def trash_collision(self):
        player = self.player_group.sprite

        for trash in self.goal_group:
            if trash.rect.collidepoint(player.hitbox.center):
                SFX.trash_collected.play()
                trash.collected = True
                self.trash_collected += 1
    
    def diamond_collision(self):
        player = self.player_group.sprite

        for diamond in self.diamond_sprites:
            if diamond.rect.collidepoint(player.hitbox.center):
                SFX.diamond_collected.play()
                diamond.collected = True
                self.collected_diamond = True


    def check_conditions(self):
        self.spring_collision()
        self.spring_sprites.update()
        self.spike_collision()
        self.bubble_collision()
        self.bubble_sprites.update()
        self.trash_collision()
        self.goal_group.update()
        self.diamond_collision()
        self.diamond_sprites.update()
        self.check_horizontal_collision()
        self.check_vertical_collision()

        self.check_victory()

    


    """ 
    How we check for collision in 2D platformer:
    - The problem with the collision in pygame is that it can tell you that it collided with something
      but could not tell you which side and where it has collided
    - If that's the case, 2D Platformer will be difficult to deal with as each side of the
      tile does different things (Left and right doesn't do anything, Up means that you can jump etc.)
    Solution:
    - We will check collision for both the x and y axis
    - Then using the information obtained, we can determine what we will do
    """

    # We will check collision in the Level class
    # The reason for this is because this class contains both the Tiles and Player
    # which will be needed to check for collision between each other
    def check_horizontal_collision(self):
        player = self.player_group.sprite
        player.pos.x += player.direction.x * player.speed
        player.rect.x = player.pos.x
        player.hitbox.x = player.offset.x + player.pos.x
        
        if player.hitbox.left <= 0:
            player.pos.x = -player.offset.x
        elif player.hitbox.right >= self.level_width:
            player.pos.x = self.level_width - player.hitbox.width - player.offset.x

        for sprite in self.terrain_sprites.sprites():
            # The reason we are not using sprite collision is because
            # we need to get the x and y position of the rectangle
            if sprite.rect.colliderect(player.hitbox):
                # To check if it's left or right side of the tile
                # If the direction is less than 0 it means it's moving to the left
                if player.direction.x < 0:
                    player.pos.x = sprite.rect.right - player.offset.x
                elif player.direction.x > 0:
                    player.pos.x = sprite.rect.left - player.hitbox.width - player.offset.x

        player.rect.x = player.pos.x
        player.hitbox.x = player.offset.x + player.pos.x

    def check_vertical_collision(self):
        player = self.player_group.sprite
        player.apply_gravity()

        # player.on_ground = False
        
        if player.hitbox.centery >= self.level_height:
            SFX.death.play()
            player.dead = True
        
        # Use hitbox rectangle to detect collision
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.direction.y > 0:
                    player.on_ground = True
                    # But change the position vector instead of changing the hitbox rectangle
                    # Because only hitbox rectangle is updated but image rectangle is not
                    player.pos.y = sprite.rect.top - player.hitbox.width - player.offset.y
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.on_ceiling = True
                    player.pos.y = sprite.rect.bottom - player.offset.y
                    player.direction.y = 0  

        if player.on_ground == True and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling == True and player.direction.y > 0:
            player.on_ceiling = False

        # Update it immediately (As any later will cause delay, which will make the game buggy)
        player.rect.y = player.pos.y
        player.hitbox.y = player.offset.y + player.pos.y



    def death_screen(self):
        player = self.player_group.sprite

        player.direction = (0, 0)
        player.play_death_animation()
        player.action = "Death"
        self.bar_group.update(player.pos, 1)

        self.game_over_screen.draw()


    def draw(self):
        # self.scroll_x()

        # Tiles
        # Calling the Tile method .update() through a Group
        # self.terrain_sprites.update(-5, 0)
        # self.terrain_sprites.draw(self.display_surface)
        
        SCREEN.blit(self.background, (0, 0))
        SCREEN.blit(self.foreground, (0, 0))

        # Since we can't use .draw groups we will apply the offset to each entity one by one
    
        # apply the offset to each entity.
        # call this for everything that should scroll,
        # which is basically everything other than GUI/HUD/UI

        for terrain in self.terrain_sprites:
            SCREEN.blit(terrain.image, self.camera.scroll(terrain))

        # for scaffolding in self.scaffolding_sprites:
        #     SCREEN.blit(scaffolding.image, self.camera.scroll(scaffolding))

        for decorations in self.decorations_sprites:
            SCREEN.blit(decorations.image, self.camera.scroll(decorations))

        for spikes in self.spikes_sprites:
            SCREEN.blit(spikes.image, self.camera.scroll(spikes))

        for diamond in self.diamond_sprites:
            SCREEN.blit(diamond.image, self.camera.scroll(diamond))

        for bubble in self.bubble_sprites:
            SCREEN.blit(bubble.image, self.camera.scroll(bubble))

        for spring in self.spring_sprites:
            SCREEN.blit(spring.image, self.camera.scroll(spring))

        for goal in self.goal_group:
            SCREEN.blit(goal.image, self.camera.scroll(goal))

        for player in self.player_group:
            SCREEN.blit(player.image, self.camera.scroll(player))

        for water in self.water_sprites:
            SCREEN.blit(water.image, self.camera.scroll(water))

        for bar in self.bar_group:
            SCREEN.blit(bar.image, self.camera.scroll(bar))

        for instructions in self.instructions_sprites:
            SCREEN.blit(instructions.image, self.camera.scroll(instructions))




    def update(self):
        self.draw()


        if self.is_paused == False and self.victory == False:
            player = self.player_group.sprite
            progress = player.timer/player.max_time

            if player.dead == False:
                self.bar_group.update(player.pos, progress)

                self.check_conditions()
                self.hud.draw()

                # Player
                self.player_group.update()
            
            if player.dead == True:
                self.death_screen()

            if self.level_clear == True:
                self.victory = True
                self.victory_menu.draw()

        elif self.is_paused == True:
            self.hud.update_start_time()
            self.pause_menu.draw()

        elif self.victory == True:
            if self.user_data[f"level_{self.level_id}_status"]["best_time"] == 0:
                self.user_data[f"level_{self.level_id}_status"]["best_time"] = self.hud.time
            elif self.user_data[f"level_{self.level_id}_status"]["best_time"] != 0:
                if self.hud.time < self.user_data[f"level_{self.level_id}_status"]["best_time"]:
                    self.user_data[f"level_{self.level_id}_status"]["best_time"] = self.hud.time

            self.victory_menu.get_time(self.hud.time, self.user_data[f"level_{self.level_id}_status"]["best_time"])
            self.victory_menu.draw()

    # 
    def __del__(self):
        if self.player_group.sprite.dead == True:
            self.user_data["death_count"] += 1

        if self.victory == True:
            self.user_data[f"level_{self.level_id}_status"]["clear"] = True

            if self.collected_diamond == True:
                self.user_data[f"level_{self.level_id}_status"]["diamond_collected"] = True
            
            if self.level_id != len(self.level_json.data) - 1:
                self.user_data[f"level_{self.level_id + 1}_status"]["unlocked"] = True

        self.user_json.data = self.user_data
        self.user_json.dump_data()
