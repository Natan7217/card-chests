import pygame
import menu
import city
import game
import json
from functions import load_image, load_settings, terminate
from objects import MouseChecking, Button, InGameMenu, LoadingScreen, TextInput


class CasinoApp:
    def __init__(self, parent=None, player='Natan'):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            self.lang_json = json.load(lang_file)
            lang_json_dict = self.lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            self.start_text = lang_json_dict["START_BUTTON"]
            self.play_text = lang_json_dict["PLAY_BUTTON"]
            self.back_text = lang_json_dict["BACK_BUTTON"]
            self.continue_text = lang_json_dict["CONTINUE_BUTTON"]
            self.back_menu_text = lang_json_dict["BACK_MENU_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
            self.loading_text = lang_json_dict["LOADING_TEXT"]
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if parent is None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = parent
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.player = player
        self.menu_flag = False
        pygame.mixer.music.load('./music/casino_soundtrack.wav')
        pygame.mixer.music.set_volume(0.03 * self.curr_vol / 100)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_icon(load_image('icon.png'))
        pygame.display.set_caption(self.win_title)
        self.menu = InGameMenu(self.width, self.height)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.objects = []
        self.buttons = []
        self.titles = [self.play_text, self.back_text]
        self.button_width, self.button_height = 0.2 * self.width, 0.12 * self.height
        self.button_x, self.button_y = 0.25 * self.width, 0.6 * self.height
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.07 * self.width,
                           height=0.098 * self.height, text=' ', volume=self.curr_vol, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x + i * (self.button_width + 0.2 * self.button_width),
                                       y=self.button_y,
                                       image_name='bank_button.png', width=self.button_width, height=self.button_height,
                                       text=self.titles[i], volume=self.curr_vol, screen_width=self.width,
                                       sound_name='click.wav', color_key=-1))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.buttons.append(self.exit)
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        self.text_x, self.text_y = 0.01 * self.width, 0.495 * self.height
        self.text_width, self.text_height = 0.4 * self.width, 0.075 * self.height

        self.text_input = None
        self.mouse_checking = MouseChecking(self.objects)

        self.background = pygame.transform.scale(load_image('casino_background.jpg'), (self.width, self.height))
        self.table = pygame.transform.scale(load_image('table.jpg', color_key=-1), (self.width, self.height))
        self.curr_fps = self.fps
        self.bet = 100

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.table, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == " ":
                        self.menu_flag = True
                        break
                    elif ev.button.text == self.play_text:
                        self.buttons, self.objects = [], []
                        self.text_input = TextInput(x=self.text_x, y=self.text_y, width=self.text_width,
                                                    height=self.text_height, image_name='text_input.jpg',
                                                    screen_width=self.width, only_digits=True)
                        start_button = Button(x=0.21 * self.width, y=self.button_y, image_name='green_button.jpg',
                                              width=self.button_width, height=self.button_height, text=self.start_text,
                                              volume=self.curr_vol, screen_width=self.width,
                                              sound_name='click.wav')
                        self.buttons.append(start_button)
                        self.buttons.append(self.exit)
                        self.objects.append((start_button.__class__.__name__, start_button.rect))
                        self.objects.append((self.text_input.__class__.__name__, self.text_input.rect))
                        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
                        self.mouse_checking.change_objects(self.objects)
                    elif ev.button.text == self.back_text:
                        city_app = city.CityApp(player=self.player)
                        city_app.run()
                    elif ev.button.text == self.start_text:
                        game_app = game.GameApp(player=self.player, bet=self.bet)
                        game_app.run()
                for button in self.buttons:
                    button.handle_event(ev)
                if self.text_input:
                    text = self.text_input.handle_event(ev)
                    if text is not None:
                        self.bet = int(text)
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
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            if self.text_input:
                self.text_input.draw(self.screen)
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = CasinoApp()
    app.run()
