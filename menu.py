import sys

import pygame
<<<<<<< Updated upstream
from functions import load_image, load_settings
import settings
from objects import Button


def main_window(fps, volume, width, height, min_width, min_height, parent=None):
    if parent is None:
        pygame.init()
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    else:
        screen = parent
    clock = pygame.time.Clock()
    pygame.display.set_caption('Card-chests v1.0')
    background = load_image('background_folder.jpg')
    buttons = []
    titles = ['PLAY', "SCORE", 'SETTINGS', 'EXIT']
    w, h = 0.2 * width, 0.1 * height
    button_x, button_y = (width - w) / 2, (height - h * len(titles)) / 2
    for i in range(len(titles)):
        buttons.append(Button(x=button_x, y=button_y + i * (h + 0.2 * h), image_name='green_button.jpg',
                              width=w, height=h, text=titles[i], volume=volume, screen_width=width,
                              sound_name='click1.ogg'))
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.VIDEORESIZE:
                width, height = ev.size
                if ev.w < min_width:
                    width = min_width
                if ev.h < min_height:
                    height = min_height
                w, h = 0.2 * width, 0.1 * height
                button_x, button_y = (width - w) / 2, (height - h * len(titles)) / 2
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for i in range(len(titles)):
                    buttons[i].update(screen, button_x, button_y + i * (h + 0.2 * h), w, h)
            elif ev.type == pygame.USEREVENT:
                if ev.button.text == "EXIT":
                    pygame.time.wait(400)
                    pygame.quit()
                    sys.exit()
                elif ev.button.text == "SETTINGS":
                    settings_app = settings.SettingsApp(screen)
                    settings_app.run()
                elif ev.button.text == "SCORE":
                    pass
                else:
                    pass
            for button in buttons:
                button.handle_event(ev)
        screen.blit(background, (0, 0))
        for button in buttons:
            button.hovered_checker(pygame.mouse.get_pos())
            button.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
=======
import json
import settings
import game_start
import score
from functions import load_settings, load_image, terminate
from objects import Button, MouseChecking


class MenuApp:

    def __init__(self, parent=None):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)
            lang_json_dict = lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            self.play_text = lang_json_dict["PLAY_BUTTON"]
            self.score_text = lang_json_dict["SCORE_BUTTON"]
            self.sett_text = lang_json_dict["SETTINGS_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_icon(load_image('icon.png'))
        if pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.load('./music/main_menu_music.wav')
            pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.05 * self.curr_vol / 100)
        pygame.display.set_caption(self.win_title)
        self.clock = pygame.time.Clock()
        self.titles = [self.play_text, self.score_text, self.sett_text, self.exit_text]
        self.buttons = []
        self.objects = []
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = ((self.width - self.button_width) / 2,
                                        (self.height - self.button_height * len(self.titles)) / 2)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click1.ogg'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking = MouseChecking(self.objects)
        self.background = pygame.transform.scale(load_image('background_folder.jpg'), (self.width, self.height))
        self.buttons_update(self.width, self.height)
        self.curr_fps = self.fps

    def buttons_update(self, width, height):
        self.objects = []
        self.width, self.height = width, height
        if width < self.min_width:
            self.width = self.min_width
        if height < self.min_height:
            self.height = self.min_height
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = ((self.width - self.button_width) / 2,
                                        (self.height - self.button_height * len(self.titles)) / 2)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        for i in range(len(self.titles)):
            self.buttons[i].update(self.screen, self.button_x,
                                   self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                   self.button_width, self.button_height)
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking.change_objects(self.objects)

    def run(self):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.VIDEORESIZE:
                    self.buttons_update(ev.w, ev.h)
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == self.exit_text:
                        terminate()
                    elif ev.button.text == self.sett_text:
                        settings_app = settings.SettingsApp(parent=self.screen)
                        settings_app.run()
                    elif ev.button.text == self.score_text:
                        score_app = score.ScoreApp(parent=self.screen)
                        score_app.run()
                    else:
                        game_app = game_start.StartApp(parent=self.screen)
                        game_app.run()
                for button in self.buttons:
                    button.handle_event(ev)
            self.screen.blit(self.background, (0, 0))
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()
>>>>>>> Stashed changes


if __name__ == '__main__':
    CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT, MIN_WIDTH, MIN_HEIGHT = load_settings()
    main_window(CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT, MIN_WIDTH, MIN_HEIGHT)
