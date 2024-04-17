import pygame
import sys
from levels import *
from json_handling import Json
from menu import Menu, LevelSelect, ConfirmExit, ConfirmReset

pygame.init()

# Game Handling
class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()

        self.level_json = Json("data/level_data.json")
        self.user_json = Json("data/user_data.json")
        self.default_json = Json("data/default.json")
        self.level_id = 0

        self.menu = Menu(self.user_json, self.level_json)
        self.level_select_menu = None
        self.confirm_exit_menu = None
        self.confirm_reset_menu = None
        self.level = None

        self.in_game = False
        self.in_main_menu = True
        self.in_level_select = False
        self.confirm_exit = False
        self.confirm_reset = False

        self.confirm = [pygame.K_RETURN, pygame.K_SPACE]
        self.back = [pygame.K_ESCAPE, pygame.K_z]
        
        self.user_data = self.user_json.data
        SFX.change_audio(self.user_data["sound"])
        MUSIC.change_audio(self.user_data["music"])

        MUSIC.channel1.play(MUSIC.music2, -1)


    def level_select(self):
        self.in_main_menu = False
        self.in_game = False
        self.in_level_select = True
        self.confirm_exit = False
        self.confirm_reset = False
        self.update_states()
        self.level_select_menu = LevelSelect(self.level_json, self.level_id, self.user_json)
        
    def start_game(self, level_id):
        MUSIC.channel1.stop()
        self.in_game = True
        self.in_main_menu = False
        self.in_level_select = False
        self.confirm_exit = False
        self.confirm_reset = False
        if self.user_json.data["first_run"] == True:
            self.user_json.data["first_run"] = False
            self.user_json.dump_data()
        self.update_states()
        self.level = Level(self.level_json, SCREEN, self.user_json, level_id)
        MUSIC.channel2.play(MUSIC.music, -1)
        MUSIC.channel3.play(MUSIC.ambience, -1)

    def return_to_main(self):
        self.in_main_menu = True
        self.in_game = False
        self.in_level_select = False
        self.confirm_exit = False
        self.confirm_reset = False
        self.update_states()
        self.menu = Menu(self.user_json, self.level_json)

    def exit_confirmation(self):
        self.confirm_exit = True
        self.update_states()
        self.confirm_exit_menu = ConfirmExit()

    def reset_confirmation(self):
        self.confirm_reset = True
        self.update_states()
        self.confirm_reset_menu = ConfirmReset()

    def menu_select(self):
        if self.in_main_menu == True:
            if self.menu.in_options == False and self.menu.in_leaderboards == False:
                if self.menu.selection == 1:
                    self.level_select()  # Start Game
                elif self.menu.selection == 2:
                    self.menu.option_menu()  # Options
                elif self.menu.selection == 3:
                    self.menu.leaderboards_menu() #Leaderboards
                elif self.menu.selection == 4:
                    self.exit_confirmation()
                    # self.exit()  # Exit

            elif self.menu.in_options == True:
                if self.menu.selection == 3:
                    self.reset_confirmation()
                elif self.menu.selection == 4:
                    self.menu.return_to_menu_from_options()
            
            else:
                self.menu.return_to_menu_from_leaderboards()

            SFX.confirm.play()

    def exit_program(self):
        self.running = False

    def level_reset(self):
        del self.level
        self.level = None
        level_id = self.level_id
        self.level = Level(self.level_json, SCREEN, self.user_json, level_id)

    def pause_menu_select(self):
        selection = self.level.pause_menu.selection
        if selection == 1:
            self.level.is_paused = False #Continue
        elif selection == 2:
            self.level_reset() #Restart
        elif selection == 3:
            MUSIC.channel2.stop()
            MUSIC.channel3.stop()
            MUSIC.channel1.play(MUSIC.music2, -1)
            self.level_select()  # Quit

        SFX.confirm.play()

    def victory_menu_select(self):
        selection = self.level.victory_menu.selection
        if selection == 1:
            self.next_level() # Next Level
        elif selection == 2:
            self.level_reset()  # Restart
        elif selection == 3:
            MUSIC.channel2.stop()
            MUSIC.channel3.stop()
            MUSIC.channel1.play(MUSIC.music2, -1)
            self.level_select()  # Quit

        SFX.confirm.play()

    def level_menu_select(self):
        level_id = self.level_select_menu.selection
        if self.in_level_select == True and self.user_json.data[f"level_{level_id}_status"]["unlocked"]:
            self.start_game(level_id)

        SFX.confirm.play()

    def next_level(self):
        SFX.confirm.play()
        self.level_id += 1
        if self.level_id < len(self.level_json.data):
            del self.level
            self.start_game(self.level_id)
        else:
            self.level_id = len(self.level_json.data) - 1
            MUSIC.channel2.stop()
            MUSIC.channel3.stop()
            MUSIC.channel1.play(MUSIC.music2, -1)
            self.level_select()

    def reset_data(self):
        SFX.confirm.play()
        self.user_json.data = self.default_json.data
        self.user_json.dump_data()
        del self.menu
        self.confirm_reset = False
        self.user_json.reload_data()
        self.menu = Menu(self.user_json, self.level_json)



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.confirm_exit == True:
                    if event.key == pygame.K_LEFT and self.confirm_exit_menu.selection != 0:
                        self.confirm_exit_menu.selection -= 1
                        SFX.move_arrow.play()
                    elif event.key == pygame.K_RIGHT and self.confirm_exit_menu.selection != 1:
                        self.confirm_exit_menu.selection += 1
                        SFX.move_arrow.play()
                    elif event.key in self.confirm and self.confirm_exit_menu.selection == 0:
                        self.exit_program()
                        SFX.confirm.play()
                    elif event.key in self.confirm and self.confirm_exit_menu.selection == 1 or event.key in self.back:
                        self.return_to_main()
                        SFX.cancel.play()

                elif self.confirm_reset == True:
                    if event.key == pygame.K_LEFT and self.confirm_reset_menu.selection != 0:
                        self.confirm_reset_menu.selection -= 1
                        SFX.move_arrow.play()
                    elif event.key == pygame.K_RIGHT and self.confirm_reset_menu.selection != 1:
                        self.confirm_reset_menu.selection += 1
                        SFX.move_arrow.play()
                    elif event.key in self.confirm and self.confirm_reset_menu.selection == 0:
                        self.reset_data()
                        SFX.confirm.play()
                    elif event.key in self.confirm and self.confirm_reset_menu.selection == 1 or event.key in self.back:
                        self.return_to_main()
                        SFX.cancel.play()


                elif self.in_game == True:
                    player = self.level.player_group.sprite
                    if self.level.is_paused == False and self.level.victory == False:
                        if player.dead == False:
                            if event.key == pygame.K_z:
                                player.change_state()
                            if event.key == pygame.K_SPACE:
                                player.jump()
                            if event.key == pygame.K_ESCAPE:
                                self.level.pause_menu.selection = 1
                                self.level.is_paused = True # Pause Game
                                self.level.hud.store_time()
                                SFX.confirm.play()
                        elif player.dead == True:
                            if event.key == pygame.K_z:
                                self.level_reset() # Level reset self.level_select_menu.selection
                                SFX.confirm.play()
                            elif event.key == pygame.K_ESCAPE:
                                MUSIC.channel2.stop()
                                MUSIC.channel3.stop()
                                MUSIC.channel1.play(MUSIC.music2, -1)
                                self.level_select() # Quit Level
                                SFX.cancel.play()

                    elif self.level.is_paused:
                        if event.key in self.back:
                            self.level.is_paused = False
                            SFX.cancel.play()
                        elif event.key == pygame.K_LEFT and self.level.pause_menu.selection != 1:
                            self.level.pause_menu.selection -= 1
                            SFX.move_arrow.play()
                        elif event.key == pygame.K_RIGHT and self.level.pause_menu.selection != 3:
                            self.level.pause_menu.selection += 1
                            SFX.move_arrow.play()
                        if event.key in self.confirm:
                            self.pause_menu_select()

                    elif self.level.victory:
                        if event.key in self.back:
                            self.level_select()
                        elif event.key == pygame.K_LEFT and self.level.victory_menu.selection != 1:
                            self.level.victory_menu.selection -= 1
                            SFX.move_arrow.play()
                        elif event.key == pygame.K_RIGHT and self.level.victory_menu.selection != 3:
                            self.level.victory_menu.selection += 1
                            SFX.move_arrow.play()
                        if event.key in self.confirm:
                            self.victory_menu_select()


                elif self.in_main_menu == True:
                    if event.key == pygame.K_UP and self.menu.selection != 1:
                        self.menu.selection -= 1
                        SFX.move_arrow.play()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2 and self.menu.selection != 4:
                        self.menu.selection += 1
                        SFX.move_arrow.play()
                    elif event.key in self.confirm:
                        self.menu_select()
                        break

                    if self.menu.in_options == False and self.menu.in_leaderboards == False:
                        if event.key == pygame.K_ESCAPE:
                            self.exit_confirmation()

                    if self.menu.in_options and self.menu.selection != 3:
                        if event.key in self.back:
                            self.menu.return_to_menu_from_options()
                            SFX.change_audio(self.user_data["sound"])
                            MUSIC.change_audio(self.user_data["music"])
                            SFX.cancel.play()
                            
                        if self.menu.selection == 1:
                            if event.key == pygame.K_LEFT:
                                self.menu.reduce_sound()
                            elif event.key == pygame.K_RIGHT:
                                self.menu.increase_sound()
                            SFX.move_arrow.play()
                            SFX.change_audio(self.menu.sound/10)
                        if self.menu.selection == 2:
                            if event.key == pygame.K_LEFT:
                                self.menu.reduce_music()
                            elif event.key == pygame.K_RIGHT:
                                self.menu.increase_music()
                            SFX.move_arrow.play()
                            MUSIC.change_audio(self.menu.music/10)
                    
                    if self.menu.in_leaderboards:
                        if event.key == pygame.K_LEFT and self.menu.selection != 1:
                            self.menu.selection -= 1
                            SFX.move_arrow.play()
                        elif event.key == pygame.K_RIGHT and self.menu.selection != len(self.level_json.data):
                            self.menu.selection += 1
                            SFX.move_arrow.play()
                        elif event.key in self.back:
                            self.menu.return_to_menu_from_leaderboards()
                            SFX.cancel.play()

                            
                
                elif self.in_level_select == True:
                    if event.key == pygame.K_LEFT and self.level_select_menu.selection != 0:
                        self.level_select_menu.selection -= 1
                        SFX.move_arrow.play()
                    elif event.key == pygame.K_RIGHT and self.level_select_menu.selection != len(self.level_json.data) - 1:
                        self.level_select_menu.selection += 1
                        SFX.move_arrow.play()
                    elif event.key in self.back:
                        self.return_to_main()
                        SFX.cancel.play()
                        break
                    elif event.key in self.confirm:
                        self.level_menu_select()
                        SFX.confirm.play()
                        break



    def draw_screen(self):
        SCREEN.fill(BLACK) 
        if self.in_main_menu == True:
            self.menu.draw()
        if self.in_level_select == True:
            self.level_select_menu.draw()
        if self.confirm_exit == True:
            self.confirm_exit_menu.draw()
        if self.confirm_reset == True:
            self.confirm_reset_menu.draw()
        if self.in_game == True:
            self.level.update()
        pygame.display.update()


    def update_states(self):
        if self.in_main_menu == False and self.menu != None:
            del self.menu
            self.menu = None
        if self.in_level_select == False and self.level_select_menu != None:
            self.level_id = self.level_select_menu.selection
            del self.level_select_menu
            self.level_select_menu = None
        if self.confirm_exit == False and self.confirm_exit_menu != None:
            del self.confirm_exit_menu
            self.confirm_exit_menu = None
        if self.confirm_reset == False and self.confirm_reset_menu != None:
            del self.confirm_reset_menu
            self.confirm_reset_menu = None
        if self.in_game == False and self.level != None:
            del self.level
            self.level = None

    def main_loop(self):
        while self.running:
            self.clock.tick(FPS)
            if self.in_game == True:
                self.level.camera.update(self.level.player_group.sprite) # Change this
            self.check_events()
            self.draw_screen()

        pygame.quit()
        sys.exit()
