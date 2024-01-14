import pygame
import menu
import bank
import casino
import json
from functions import load_settings, load_image, terminate, search_player_data
from objects import MouseChecking, Button, InGameMenu, LoadingScreen


class CityApp:

    def __init__(self, parent=None, player='Natan'):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            self.lang_json = json.load(lang_file)
            lang_json_dict = self.lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            self.continue_text = lang_json_dict["CONTINUE_BUTTON"]
            self.back_menu_text = lang_json_dict["BACK_MENU_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
            self.loading_text = lang_json_dict["LOADING_TEXT"]
        self.player, self.score = search_player_data(player)
        if parent is None:
            pygame.init()
        else:
            pygame.quit()
            pygame.init()
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.menu_flag = False
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.mixer.music.load('./music/city_soundtrack.wav')
        pygame.mixer.music.set_volume(0.05 * self.curr_vol / 100)
        pygame.mixer.music.play(loops=-1)

        pygame.display.set_icon(load_image('icon.png'))
        pygame.display.set_caption(self.win_title)

        self.menu = InGameMenu(self.width, self.height)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.bank = Button(x=0.045 * self.width, y=0.148 * self.height, image_name='bank.png', width=0.44 * self.width,
                           height=0.64 * self.height, text=' ', volume=self.curr_vol, screen_width=self.width,
                           sound_name='click.wav', hover_image_name='bank_hovered.png', color_key=-1)
        self.casino = Button(x=0.55 * self.width, y=0.175 * self.height, image_name='casino.png',
                             width=0.43 * self.width, height=0.64 * self.height, text='  ',
                             volume=self.curr_vol, screen_width=self.width, sound_name='click.wav',
                             hover_image_name='casino_hovered.png', color_key=-1)
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.089 * self.width,
                           height=0.1 * self.height, text='   ', volume=self.curr_vol, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        self.buildings = []
        self.buildings.append(self.bank)
        self.buildings.append(self.casino)
        self.buildings.append(self.exit)
        self.objects = []
        self.objects.append((self.bank.__class__.__name__, self.bank.rect))
        self.objects.append((self.casino.__class__.__name__, self.casino.rect))
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        self.mouse_checking = MouseChecking(self.objects)
        self.background = pygame.transform.scale(load_image('city_background_2.jpg'), (self.width, self.height))
        self.curr_fps = self.fps

    def run(self):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "   ":
                        self.menu_flag = True
                    elif ev.button.text == "  ":  # CASINO
                        casino_app = casino.CasinoApp(player=self.player)
                        casino_app.run()
                    elif ev.button.text == " ":  # BANK
                        bank_app = bank.BankApp(player=self.player)
                        bank_app.run()
                for building in self.buildings:
                    building.handle_event(ev)
            for building in self.buildings:
                building.hovered_checker(pygame.mouse.get_pos())
                building.draw(self.screen)
            if self.menu_flag:
                self.mouse_checking.change_objects(self.menu_objects)
                while True:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            terminate()
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_ESCAPE:
                                self.menu_flag = False
                                break
                        elif ev.type == pygame.USEREVENT:
                            if ev.button.text == self.continue_text:
                                self.menu_flag = False
                                break
                            elif ev.button.text == self.back_menu_text:
                                loading_screen = LoadingScreen(asleep=10, titles=[self.loading_text], key_flag=False)
                                screen = loading_screen.run()
                                menu_app = menu.MenuApp(parent=screen)
                                menu_app.run()
                            elif ev.button.text == self.exit_text:
                                terminate()
                        for button in self.menu.buttons:
                            button.handle_event(ev)
                    for button in self.menu.buttons:
                        button.hovered_checker(pygame.mouse.get_pos())
                        self.menu.draw(self.screen)
                    pygame.display.flip()
                    self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
                    self.clock.tick(self.fps)
                    if not self.menu_flag:
                        break
            else:
                self.mouse_checking.change_objects(self.objects)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = CityApp()
    app.run()
