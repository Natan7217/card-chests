import pygame
import menu
import city
import json
from functions import load_image, load_settings, terminate, search_player_data
from objects import MouseChecking, Button, InGameMenu, LoadingScreen


class BankApp:
    def __init__(self, parent=None, player='Natan'):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            self.lang_json = json.load(lang_file)
            lang_json_dict = self.lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            self.back_text = lang_json_dict["BACK_BUTTON"]
            self.continue_text = lang_json_dict["CONTINUE_BUTTON"]
            self.back_menu_text = lang_json_dict["BACK_MENU_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if parent is None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = parent
        pygame.display.set_icon(load_image('icon.png'))
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.player = player
        self.bank_data = search_player_data(self.player)
        self.menu_flag = False
        self.score_flag = False
        pygame.mixer.music.load('./music/bank_soundtrack.wav')
        pygame.mixer.music.set_volume(0.03 * self.curr_vol / 100)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption(self.win_title)
        self.menu = InGameMenu(self.width, self.height)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.objects = []
        self.buttons = []
        self.text = f"{self.bank_data[0]}: {self.bank_data[1]}$"
        self.font = pygame.font.Font(None, int(0.03 * self.width))
        self.char_index = 0
        self.text_x, self.text_y = self.width // 2, 0.16 * self.height
        self.titles = ['$$$', self.back_text]
        self.button_width, self.button_height = 0.2 * self.width, 0.12 * self.height
        self.button_x, self.button_y = 0.04 * self.width, 0.487 * self.height
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.07 * self.width,
                           height=0.098 * self.height, text=' ', volume=self.curr_vol, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        self.buttons.append(self.exit)
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='bank_button.png', width=self.button_width, height=self.button_height,
                                       text=self.titles[i], volume=self.curr_vol, screen_width=self.width,
                                       sound_name='bank_button.wav'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking = MouseChecking(self.objects)
        self.backgrounds = [pygame.transform.scale(load_image('bank_background_0.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_1.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_2.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_1.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_2.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_1.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_2.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_1.jpg'), (self.width, self.height)),
                            pygame.transform.scale(load_image('bank_background_2.jpg'), (self.width, self.height))]
        self.background = 0
        self.refactor_background = 0.0
        self.curr_fps = self.fps

    def run(self):
        current_text = ''
        while True:
            self.screen.blit(self.backgrounds[self.background], (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "$$$":
                        current_text = ''
                        self.score_flag = not self.score_flag
                        self.char_index = 0
                    elif ev.button.text == self.back_text:
                        city_app = city.CityApp(player=self.player)
                        city_app.run()
                    elif ev.button.text == ' ':
                        self.menu_flag = True
                for button in self.buttons:
                    button.handle_event(ev)
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
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
                                loading_screen = LoadingScreen(asleep=4, titles=['Loading...', 'Return to main menu'],
                                                               key_flag=False)
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
            if self.score_flag:
                if int(self.char_index) < len(self.text):
                    current_text += self.text[int(self.char_index)]
                    self.char_index += 1
                else:
                    self.score_flag = not self.score_flag
                    self.char_index = 0

            text_surface = self.font.render(current_text, True, 'green')
            text_rect = text_surface.get_rect(center=(self.text_x, self.text_y))
            self.screen.blit(text_surface, text_rect)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            self.refactor_background = 0.0 if int(self.refactor_background + 0.15) > 8 \
                else self.refactor_background + 0.15
            self.background = int(self.refactor_background)
            pygame.display.flip()


if __name__ == '__main__':
    app = BankApp()
    app.run()
