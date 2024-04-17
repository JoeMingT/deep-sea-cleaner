import pygame
from config import *
from extra_functions import bulk_import

class Menu:
    def __init__(self, user_data_json, level_data_json):

        self.user_json = user_data_json
        self.user_data = user_data_json.data

        self.level_data = level_data_json.data

        self.sound = self.user_data["sound"] * 10
        self.music = self.user_data["music"] * 10

        self.in_options = False
        self.in_leaderboards = False

        self.selection = 1
        self.option_select = 1

        self.load_images()
        self.render_text()
        self.load_controls()

        self.selection_text_size = self.game_start.get_size()


    def render_text(self):
        self.title_text = THALEAH_FAT.render("Deep Sea Cleaner", 0, WHITE)
        self.title_text2 = THALEAH_FAT.render("Deep Sea Cleaner", 0, BLACK)

        if self.user_data["first_run"] == True:
            self.game_start = MONOGRAM_EXTENDED.render("New Game", 0, WHITE)
        else:
            self.game_start = MONOGRAM_EXTENDED.render("Continue", 0, WHITE)
        self.options = MONOGRAM_EXTENDED.render("Options", 0, WHITE)
        self.leaderboards = MONOGRAM_EXTENDED.render("Leaderboards", 0, WHITE)
        self.exit_text = MONOGRAM_EXTENDED.render("Exit", 0, WHITE)

        self.option_text = THALEAH_FAT.render("Options", 0, WHITE)
        self.option_text2 = THALEAH_FAT.render("Options", 0, BLACK)
        self.reset_progress = MONOGRAM_EXTENDED.render("Reset Progress", 0, WHITE)

        self.leaderboards_text = THALEAH_FAT.render("Leaderboards", 0, WHITE)

    def load_images(self):
        self.background_image = pygame.transform.scale(pygame.image.load("level data/background/back.png").convert_alpha(), (WIDTH, HEIGHT))
        
        self.title_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_03.png").convert_alpha(), (950, 90))

        self.selection_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_04.png").convert_alpha(), (600, 350))
        self.selection_arrow = pygame.transform.scale(pygame.image.load("graphics/GUI/Arrow.png").convert_alpha(), (30, 30))

        self.leaderboards_background = pygame.Surface((WIDTH, HEIGHT))
        self.leaderboards_background.fill(BLACK)


    def load_controls(self):
        self.confirm_text = EXPRESSION_PRO.render("Select", 0, BLACK)
        self.return_text = EXPRESSION_PRO.render("Return", 0, BLACK)
        self.move_text = EXPRESSION_PRO.render("Move", 0, BLACK)

        self.z_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/z_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_z_key.png"), (25, 25)) ]
        self.space_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/spacebar_key.png").convert_alpha(), (75, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_spacebar_key.png").convert_alpha(), (75, 25)) ]
        self.up_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/up_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_up_key.png").convert_alpha(), (25, 25)) ]
        self.down_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/down_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_down_key.png").convert_alpha(), (25, 25)) ]
        self.left_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/left_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_left_key.png").convert_alpha(), (25, 25)) ]
        self.right_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/right_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_right_key.png").convert_alpha(), (25, 25)) ]
        self.esc_press_frames = [ pygame.transform.scale(pygame.image.load("graphics/GUI/esc_key.png").convert_alpha(), (25, 25)), pygame.transform.scale(pygame.image.load("graphics/GUI/pressed_esc_key.png").convert_alpha(), (25, 25)) ]
        self.frame_index = 0
        self.animation_speed = 0.025

    def refresh(self):
        self.z_image = self.z_press_frames[int(self.frame_index)]
        self.space_image = self.space_press_frames[int(self.frame_index)]
        self.up_image = self.up_press_frames[int(self.frame_index)]
        self.down_image = self.down_press_frames[int(self.frame_index)]
        self.left_image = self.left_press_frames[int(self.frame_index)]
        self.right_image = self.right_press_frames[int(self.frame_index)]
        self.esc_image = self.esc_press_frames[int(self.frame_index)]

    def draw_controls(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= 2:
            self.frame_index = 0

        self.refresh()

        SCREEN.blit(self.z_image, (WIDTH/16 - self.z_image.get_width()/2 - 20, HEIGHT - HEIGHT/10 - self.z_image.get_height()/2))
        SCREEN.blit(self.esc_image, (WIDTH/16 - self.esc_image.get_width()/2 + 20, HEIGHT - HEIGHT/10 - self.esc_image.get_height()/2))
        SCREEN.blit(self.space_image, (WIDTH/16 - self.space_image.get_width()/2, HEIGHT - HEIGHT/10 - self.space_image.get_height()/2 + 40))
        SCREEN.blit(self.up_image, (WIDTH/16 - self.up_image.get_width()/2, HEIGHT - HEIGHT/10 - self.up_image.get_height()/2 - 65))
        SCREEN.blit(self.down_image, (WIDTH/16 - self.down_image.get_width()/2, HEIGHT - HEIGHT/10 - self.down_image.get_height()/2 - 45))
        SCREEN.blit(self.left_image, (WIDTH/16 - self.left_image.get_width()/2 - 25, HEIGHT - HEIGHT/10 - self.left_image.get_height()/2 - 45))
        SCREEN.blit(self.right_image, (WIDTH/16 - self.right_image.get_width()/2 + 25, HEIGHT - HEIGHT/10 - self.right_image.get_height()/2 - 45))

        SCREEN.blit(self.return_text, (WIDTH/16 - self.return_text.get_width()/2 + 100, HEIGHT - HEIGHT/10 - self.return_text.get_height()/2))
        SCREEN.blit(self.confirm_text, (WIDTH/16 - self.confirm_text.get_width()/2 + 100, HEIGHT - HEIGHT/10 - self.confirm_text.get_height()/2 + 40))
        SCREEN.blit(self.move_text, (WIDTH/16 - self.return_text.get_width()/2 + 100, HEIGHT - HEIGHT/10 - self.return_text.get_height()/2 - 50))


    def draw_main_menu(self):
        SCREEN.blit(self.title_border, (WIDTH/2 - self.title_border.get_width()/2, HEIGHT/4 - self.title_border.get_height()/2))
        SCREEN.blit(self.title_text2, (WIDTH/2 - self.title_text2.get_width()/2 - 4, HEIGHT/4 - self.title_text2.get_height()/2))
        SCREEN.blit(self.title_text, (WIDTH/2 - self.title_text.get_width()/2, HEIGHT/4 - self.title_text.get_height()/2))

        SCREEN.blit(self.selection_border, (WIDTH/2 - self.selection_border.get_width()/2, HEIGHT/2 - self.selection_border.get_height()/2 + self.game_start.get_height()))
        SCREEN.blit(self.game_start, (WIDTH/2 - self.selection_text_size[0]/2, HEIGHT/2.25 - self.selection_text_size[1]/2))
        SCREEN.blit(self.options, (WIDTH/2 - self.selection_text_size[0]/2, HEIGHT/2.25 - self.selection_text_size[1]/2 + self.selection_text_size[1]))
        SCREEN.blit(self.leaderboards, (WIDTH/2 - self.selection_text_size[0]/2, HEIGHT/2.25 - self.selection_text_size[1]/2 + 2*self.selection_text_size[1]))
        SCREEN.blit(self.exit_text, (WIDTH/2 - self.selection_text_size[0]/2, HEIGHT/2.25 - self.selection_text_size[1]/2 + 3*self.selection_text_size[1]))
        SCREEN.blit(self.selection_arrow, (WIDTH/2 - self.selection_text_size[0] + self.selection_arrow.get_width(), HEIGHT/2.25 - self.selection_arrow.get_height()/2 + (self.selection - 1) * self.selection_text_size[1]))

    
    def draw_options_menu(self):
        SCREEN.blit(self.title_border, (WIDTH/2 - self.title_border.get_width()/2, HEIGHT/4 - self.title_border.get_height()/2))
        SCREEN.blit(self.option_text2, (WIDTH/2 - self.option_text2.get_width()/2 - 4, HEIGHT/4 - self.option_text2.get_height()/2))
        SCREEN.blit(self.option_text, (WIDTH/2 - self.option_text.get_width()/2, HEIGHT/4 - self.option_text.get_height()/2))

        SCREEN.blit(self.selection_border, (WIDTH/2 - self.selection_border.get_width()/2, HEIGHT/2 - self.selection_border.get_height()/2 + self.game_start.get_height()))
        SCREEN.blit(self.sound_text, (WIDTH/2.2 - self.selection_text_size[0]/2, HEIGHT/2.2 - self.selection_text_size[1]/2))
        SCREEN.blit(self.music_text, (WIDTH/2.2 - self.selection_text_size[0]/2, HEIGHT/2.2 - self.selection_text_size[1]/2 + self.selection_text_size[1]))
        SCREEN.blit(self.reset_progress, (WIDTH/2.2 - self.selection_text_size[0]/2, HEIGHT/2.2 - self.selection_text_size[1]/2 + 2*self.selection_text_size[1]))
        SCREEN.blit(self.exit_text, (WIDTH/2.2 - self.selection_text_size[0]/2, HEIGHT/2.2 - self.selection_text_size[1]/2 + 3*self.selection_text_size[1]))
        SCREEN.blit(self.selection_arrow, (WIDTH/2.2 - self.selection_text_size[0] + self.selection_arrow.get_width(), HEIGHT/2.2 - self.selection_arrow.get_height()/2 + (self.selection - 1) * self.selection_text_size[1]))

    def draw_leaderboards(self):
        SCREEN.blit(self.leaderboards_background, (0, 0))

        SCREEN.blit(self.leaderboards_text, (WIDTH/2 - self.leaderboards_text.get_width()/2, HEIGHT/10 - self.leaderboards_text.get_height()/2))
        SCREEN.blit(self.level_text, (WIDTH/2 - self.level_text.get_width()/2, 7*HEIGHT/10 - self.level_text.get_height()/2))
        SCREEN.blit(self.best_time, (WIDTH/2 - self.best_time.get_width()/2, 4*HEIGHT/10 - self.best_time.get_height()/2))
        SCREEN.blit(self.diamond_collected_text, (WIDTH/2 - self.diamond_collected_text.get_width()/2, 5*HEIGHT/10 - self.diamond_collected_text.get_height()/2))


    def draw(self):
        SCREEN.blit(self.background_image, (0, 0))
    
        if self.in_options == False and self.in_leaderboards == False:
            self.draw_main_menu()

            self.draw_controls()

        elif self.in_options == True:
            self.sound_text = MONOGRAM_EXTENDED.render(f"Sound  {int(self.sound)}", 0, WHITE)
            self.music_text = MONOGRAM_EXTENDED.render(f"Music  {int(self.music)}", 0, WHITE)
            self.draw_options_menu()

            self.draw_controls()

        else:
            self.level_text = FUTILE_PRO.render(f"Level {self.selection}", 0, WHITE)
            best_time = self.user_data[f'level_{self.selection-1}_status']['best_time']
            if best_time != 0:
                best_time_ms = best_time % 1000
                best_time_s = int(best_time/1000) % 60
                best_time_min = int(best_time/1000) // 60
            else:
                best_time_ms = best_time_min = best_time_s = "--"

            best_time_text = f"Best Time > {best_time_min}m : {best_time_s}s : {best_time_ms}ms"
            self.best_time = FUTILE_PRO.render(best_time_text, 0, WHITE)

            diamond_collected = self.user_data[f'level_{self.selection-1}_status']['diamond_collected']
            if diamond_collected:
                diamond_collected_text = f"Diamond Collected: Yes! Amazing"
            else:
                diamond_collected_text = f"Diamond Collected: No! Go find it!"
             
            self.diamond_collected_text = FUTILE_PRO.render(diamond_collected_text, 0, WHITE)

            self.draw_leaderboards()


    def reduce_sound(self):
        if self.sound != 0:
            self.sound -= 1

    def reduce_music(self):
        if self.music != 0:
            self.music -= 1

    def increase_sound(self):
        if self.sound != 10:
            self.sound += 1
    
    def increase_music(self):
        if self.music != 10:
            self.music += 1

    def option_menu(self):
        self.in_options = True
        self.selection = 1

    def leaderboards_menu(self):
        self.in_leaderboards = True
        self.selection = 1

    def return_to_menu_from_options(self):
        self.in_options = False
        self.user_data["sound"] = self.sound / 10
        self.user_data["music"] = self.music / 10
        self.user_json.data = self.user_data
        self.user_json.dump_data()
        self.selection = 1

    def return_to_menu_from_leaderboards(self):
        self.in_leaderboards = False
        self.selection = 1

    



class LevelSelect(Menu):
    def __init__(self, level_data_json, selection, user_data_json):
        self.background_image = pygame.transform.scale(pygame.image.load("level data/background/back.png").convert_alpha(), (WIDTH, HEIGHT))

        self.level_json = level_data_json
        self.level_data = level_data_json.data

        self.user_json = user_data_json
        self.user_data = self.user_json.data

        self.title_text = EIGHT_BIT_WONDER.render("LEVEL SELECT", 0, WHITE)
        self.title_text2 = EIGHT_BIT_WONDER.render("LEVEL SELECT", 0, BLACK)
        self.title_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_03.png").convert_alpha(), (900, 90))

        self.level_select_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_04.png").convert_alpha(), (450, 80))
        self.arrow_right = pygame.transform.scale(pygame.image.load("graphics/GUI/Arrow.png").convert_alpha(), (30, 30))
        self.arrow_left = pygame.transform.flip(self.arrow_right, 1, 0)

        self.selection = selection

        self.load_controls()
        self.load_preview()

    def load_preview(self):
        self.preview = []
        for i in range(len(self.level_data)):
            preview_img = pygame.transform.scale(pygame.image.load(f"graphics/Images/preview/level_{i}.png"), (WIDTH/1.25, HEIGHT/1.5))
            self.preview.append(preview_img)

        self.locked_img = pygame.transform.scale(pygame.image.load(f"graphics/Images/preview/locked.png"), (WIDTH/1.25, HEIGHT/1.5))

    def draw(self):
        SCREEN.blit(self.background_image, (0, 0))

        SCREEN.blit(self.title_border, (WIDTH/2 - self.title_border.get_width()/2, HEIGHT/10 - self.title_border.get_height()/2))
        SCREEN.blit(self.title_text2, (WIDTH/2 - self.title_text2.get_width()/2 - 4, HEIGHT/10 - self.title_text2.get_height()/2))
        SCREEN.blit(self.title_text, (WIDTH/2 - self.title_text.get_width()/2, HEIGHT/10 - self.title_text.get_height()/2))

        level_text = EXPRESSION_PRO.render(f"Level {self.selection + 1}", 0, WHITE)
        SCREEN.blit(self.level_select_border, (WIDTH/2 - self.level_select_border.get_width()/2, HEIGHT - HEIGHT/10 - self.level_select_border.get_height()/2))
        if self.user_data[f"level_{self.selection}_status"]["unlocked"] == False:
            SCREEN.blit(self.locked_img, (WIDTH/2 - self.locked_img.get_width()/2, HEIGHT/2 - self.locked_img.get_height()/2))
        else:
            SCREEN.blit(self.preview[self.selection], (WIDTH/2 - self.preview[self.selection].get_width()/2, HEIGHT/2 - self.preview[self.selection].get_height()/2))


        SCREEN.blit(level_text, (WIDTH/2 - level_text.get_width()/2, HEIGHT - HEIGHT/10 - level_text.get_height()/2))
        SCREEN.blit(self.arrow_left, (WIDTH/2.75 - self.arrow_left.get_width()/2, HEIGHT - HEIGHT/10 - self.arrow_left.get_height()/2))
        SCREEN.blit(self.arrow_right, (WIDTH - WIDTH/2.75 - self.arrow_right.get_width()/2, HEIGHT - HEIGHT/10 - self.arrow_left.get_height()/2))

        self.draw_controls()

        
        
        
class ConfirmExit:
    def __init__(self):
        self.load_image()
        self.load_text()

        self.exit_text = EXPRESSION_PRO.render("Do you want to Exit?", 0, WHITE)
        self.selection = 1


    def load_image(self):
        self.image = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
        self.image.fill(GREY)
        self.image.set_alpha(200)

        self.yes_button_image = pygame.transform.scale(pygame.image.load("graphics/GUI/button_01.png").convert_alpha(), (300, 100))
        self.yes_rect = self.yes_button_image.get_rect()
        self.no_button_image = self.yes_button_image
        self.no_rect = self.no_button_image.get_rect()

        self.selection_arrow = pygame.transform.scale(pygame.image.load("graphics/GUI/Arrow.png").convert_alpha(), (30, 30))

    
    def load_text(self):
        self.yes_text = COMPASS_PRO.render("Yes", 0, BLACK)
        self.no_text = COMPASS_PRO.render("No", 0, BLACK)
    
    def draw_essentials(self):
        SCREEN.blit(self.image, (0, 0))
        SCREEN.blit(self.yes_button_image, (WIDTH/3 - self.yes_button_image.get_width()/2, HEIGHT/1.5 - self.yes_button_image.get_height()/2))
        SCREEN.blit(self.no_button_image, (WIDTH - WIDTH/3 - self.no_button_image.get_width()/2, HEIGHT/1.5- self.no_button_image.get_height()/2))
        SCREEN.blit(self.yes_text, (WIDTH/3 - self.yes_text.get_width()/2, HEIGHT/1.5- self.yes_text.get_height()/2))
        SCREEN.blit(self.no_text, (WIDTH - WIDTH/3 - self.no_text.get_width()/2, HEIGHT/1.5- self.no_text.get_height()/2))
        SCREEN.blit(self.selection_arrow, ( (WIDTH/3 - self.selection_arrow.get_width()/2) + (self.selection * WIDTH/3) - self.yes_text.get_width(), HEIGHT/1.5- self.selection_arrow.get_height()/2) )

    def draw(self):
        self.draw_essentials()
        SCREEN.blit(self.exit_text, (WIDTH/2 - self.exit_text.get_width()/2, HEIGHT/3 - self.exit_text.get_height()/2))

class ConfirmReset(ConfirmExit):
    def __init__(self):
        self.load_image()
        self.load_text()

        self.reset_text = EXPRESSION_PRO.render("Are you sure you want to reset?", 0, WHITE)
        self.selection = 1

    def draw(self):
        self.draw_essentials()
        SCREEN.blit(self.reset_text, (WIDTH/2 - self.reset_text.get_width()/2, HEIGHT/3 - self.reset_text.get_height()/2))

class GameOverMenu:
    def __init__(self):
        self.import_text()

        self.game_over_screen_bg = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
        self.game_over_screen_bg.fill(GREY)
        self.game_over_screen_bg.set_alpha(120)

    def import_text(self):
        self.game_over_text = FUTILE_PRO.render("GAME OVER!", 0, WHITE)
        self.game_over_border = FUTILE_PRO.render("GAME OVER!", 0, BLACK)

        self.instruction = MONOGRAM_EXTENDED.render("Press Z to Restart!", 0, WHITE)
        self.exit_instruction = MONOGRAM_EXTENDED.render("Press Esc to Quit", 0, WHITE)

    def draw(self):
        SCREEN.blit(self.game_over_screen_bg, (0, 0))

        SCREEN.blit(self.game_over_border, (WIDTH/2 - self.game_over_text.get_width()/2 - 4, HEIGHT/4 - self.game_over_text.get_height()/2))
        SCREEN.blit(self.game_over_text, (WIDTH/2 - self.game_over_text.get_width()/2, HEIGHT/4 - self.game_over_text.get_height()/2))
        SCREEN.blit(self.instruction, (WIDTH/2 - self.instruction.get_width()/2, HEIGHT/1.5 - self.instruction.get_height()/2))
        SCREEN.blit(self.exit_instruction, (WIDTH/2 - self.exit_instruction.get_width()/2, HEIGHT/1.5 - self.exit_instruction.get_height()/2 + self.instruction.get_height()))


class PauseMenu:
    def __init__(self):

        self.load_image()
        self.load_text()

        self.selection = 1

    def load_image(self):
        self.game_over_screen_bg = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
        self.game_over_screen_bg.fill(GREY)
        self.game_over_screen_bg.set_alpha(120)

        self.title_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_03.png").convert_alpha(), (650, 100))
        self.button_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_04.png").convert_alpha(), (300, 100))
        self.arrow = pygame.transform.scale(pygame.image.load("graphics/GUI/Arrow.png").convert_alpha(), (30, 30))

    def load_text(self):
        self.pause_text = EIGHT_BIT_WONDER.render("Game Paused", 0, WHITE)
        self.pause_text_border = EIGHT_BIT_WONDER.render("Game Paused", 0, BLACK)
        self.continue_text = MATCHUP_PRO.render("Continue", 0, WHITE)
        self.restart_text = MATCHUP_PRO.render("Restart", 0, WHITE)
        self.exit_text = MATCHUP_PRO.render("Give Up", 0, WHITE)

    def draw(self):
        SCREEN.blit(self.game_over_screen_bg, (0, 0))
        SCREEN.blit(self.title_border, (WIDTH/2 - self.title_border.get_width()/2, HEIGHT/3 - self.title_border.get_height()/2))
        SCREEN.blit(self.pause_text_border, (WIDTH/2 - self.pause_text_border.get_width()/2 - 4, HEIGHT/3 - self.pause_text_border.get_height()/2))
        SCREEN.blit(self.pause_text, (WIDTH/2 - self.pause_text.get_width()/2, HEIGHT/3 - self.pause_text.get_height()/2))

        SCREEN.blit(self.button_border, (WIDTH/4 - self.button_border.get_width()/2, HEIGHT - HEIGHT/3 - self.button_border.get_height()/2))
        SCREEN.blit(self.button_border, (WIDTH/2 - self.button_border.get_width()/2, HEIGHT - HEIGHT/3 - self.button_border.get_height()/2))
        SCREEN.blit(self.button_border, (WIDTH - WIDTH/4 - self.button_border.get_width()/2, HEIGHT - HEIGHT/3 - self.button_border.get_height()/2))

        SCREEN.blit(self.continue_text, (WIDTH/4 - self.continue_text.get_width()/2, HEIGHT - HEIGHT/3 - self.continue_text.get_height()/2))
        SCREEN.blit(self.restart_text, (WIDTH/2 - self.restart_text.get_width()/2, HEIGHT - HEIGHT/3 - self.restart_text.get_height()/2))
        SCREEN.blit(self.exit_text, (WIDTH - WIDTH/4 - self.exit_text.get_width()/2, HEIGHT - HEIGHT/3 - self.exit_text.get_height()/2))

        SCREEN.blit(self.arrow, ( (WIDTH/4)*self.selection - self.arrow.get_width() - self.continue_text.get_width()/2 - 10, HEIGHT - HEIGHT/3 - self.arrow.get_height()/2 ))


class VictoryMenu:
    def __init__(self):
        self.selection = 1

        self.frame_index = 0
        self.animation_speed = 0.1

        self.load_image()
        self.load_text()
        self.load_animation()

        self.time = 0
        self.best_time = 0

        self.time_text = QUIXEL.render(f"Time: {(self.time/1000):.2f}", 0, WHITE)
        self.best_time_text = QUIXEL.render(f"Best Time: {(self.best_time/1000):.2f}", 0, WHITE)


    def get_time(self, time, best_time):
        self.time = time
        self.best_time = best_time

        self.time_text = QUIXEL.render(f"Time: {(self.time/1000):.2f}", 0, WHITE)
        self.best_time_text = QUIXEL.render(f"Best Time: {(self.best_time/1000):.2f}", 0, WHITE)

    def load_image(self):
        self.victory_screen_bg = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
        self.victory_screen_bg.fill(GREY)
        self.victory_screen_bg.set_alpha(120)

        self.title_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_03.png").convert_alpha(), (650, 100))
        self.button_border = pygame.transform.scale(pygame.image.load("graphics/GUI/border_04.png").convert_alpha(), (310, 100))
        self.arrow = pygame.transform.scale(pygame.image.load("graphics/GUI/Arrow.png").convert_alpha(), (30, 30))

    def load_animation(self):
        self.dance_frames = []

        for frames in bulk_import("graphics/Player/Dance"):
            scaled_img = pygame.transform.scale(frames, (2*TILE_SIZE, 2*TILE_SIZE))
            self.dance_frames.append(scaled_img)

        self.dance_image_right = self.dance_frames[int(self.frame_index)]
        self.dance_image_left = pygame.transform.flip(self.dance_image_right, 1, 0)

    def load_text(self):
        self.victory_text = FUTILE_PRO.render("Trash Collected!", 0, WHITE)
        self.victory_text_border = FUTILE_PRO.render("Trash Collected!", 0, BLACK)

        self.continue_text = MATCHUP_PRO.render("Next Level", 0, WHITE)
        self.restart_text = MATCHUP_PRO.render("Restart", 0, WHITE)
        self.exit_text = MATCHUP_PRO.render("Quit", 0, WHITE)


    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.dance_frames):
            self.frame_index = 0

        self.dance_image_right = self.dance_frames[int(self.frame_index)]
        self.dance_image_left = pygame.transform.flip(self.dance_image_right, 1, 0)

        SCREEN.blit(self.dance_image_right, (5*WIDTH/6 - self.dance_image_right.get_width()/2, HEIGHT/3 - self.dance_image_right.get_height()/2))
        SCREEN.blit(self.dance_image_left, (WIDTH/6 - self.dance_image_left.get_width()/2, HEIGHT/3 - self.dance_image_left.get_height()/2))

    def draw(self):
        SCREEN.blit(self.victory_screen_bg, (0, 0))
        SCREEN.blit(self.title_border, (WIDTH/2 - self.title_border.get_width()/2, HEIGHT/3 - self.title_border.get_height()/2))
        SCREEN.blit(self.victory_text_border, (WIDTH/2 - self.victory_text_border.get_width()/2 - 4, HEIGHT/3 - self.victory_text_border.get_height()/2))
        SCREEN.blit(self.victory_text, (WIDTH/2 - self.victory_text.get_width()/2, HEIGHT/3 - self.victory_text.get_height()/2))

        SCREEN.blit(self.button_border, (WIDTH/4 - self.button_border.get_width()/2, HEIGHT - HEIGHT/4 - self.button_border.get_height()/2))
        SCREEN.blit(self.button_border, (2*WIDTH/4 - self.button_border.get_width()/2, HEIGHT - HEIGHT/4 - self.button_border.get_height()/2))
        SCREEN.blit(self.button_border, (3*WIDTH/4 - self.button_border.get_width()/2, HEIGHT - HEIGHT/4 - self.button_border.get_height()/2))
        SCREEN.blit(self.continue_text, (WIDTH/4 - self.continue_text.get_width()/2, HEIGHT - HEIGHT/4 - self.continue_text.get_height()/2))
        SCREEN.blit(self.restart_text, (2*WIDTH/4 - self.restart_text.get_width()/2, HEIGHT - HEIGHT/4 - self.restart_text.get_height()/2))
        SCREEN.blit(self.exit_text, (3*WIDTH/4 - self.exit_text.get_width()/2, HEIGHT - HEIGHT/4 - self.exit_text.get_height()/2))

        SCREEN.blit(self.arrow, ( (WIDTH/4)*self.selection - self.arrow.get_width() - self.continue_text.get_width()/2 - 5, HEIGHT - HEIGHT/4 - self.arrow.get_height()/2 ))

        SCREEN.blit(self.time_text, (WIDTH/2 - self.time_text.get_width()/2 - 20, HEIGHT/2 - self.time_text.get_height()/2 + 20))
        SCREEN.blit(self.best_time_text, (WIDTH/2 - self.time_text.get_width()/2 - 20, HEIGHT/2 - self.time_text.get_height()/2 - 20))

        self.animate()


