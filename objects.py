import sys
import pygame
import json
from typing import Optional, Union
from functions import load_image, load_sound, load_settings


class Button:
    def __init__(self, x, y, width, height, text, image_name, volume, screen_width, hover_image_name=None,
                 sound_name=None, color_key=None):
        self.x, self.y, self.width, self.height, self.volume = x, y, width, height, volume
        self.screen_width = screen_width
        self.text = text
        self.image = load_image(image_name, color_key=color_key)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        self.hover_image_name = hover_image_name
        if self.hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(self.hover_image_name, color_key=color_key),
                                                      (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = load_sound(sound_name) if sound_name else None
        self.is_hovered = False

    def draw(self, surface):
        top_image = self.hover_image if self.is_hovered else self.image
        surface.blit(top_image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * self.screen_width))

        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def hovered_checker(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def update(self, surface, new_button_x, new_button_y, new_w, new_h):
        self.x, self.y, self.width, self.height = new_button_x, new_button_y, new_w, new_h
        self.screen_width = surface.get_width()
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect(topleft=(new_button_x, new_button_y))
        self.hover_image = self.image
        if self.hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(self.hover_image_name), (new_w, new_h))
        self.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.set_volume(self.volume / 100)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class TextInput:
    def __init__(self, x, y, width, height, image_name, screen_width, only_digits: bool = False):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.screen_width = screen_width
        self.text = ''
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.counter = 0
        self.text_input_flag = False
        self.is_hovered = False
        self.only_digits = only_digits
        self.__color = ""

    def draw(self, surface):
        self.counter += 1
        surface.blit(self.image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * self.screen_width))
        self.text = (self.text.replace('|', '') if self.text_input_flag and self.counter == 5 and '|' in self.text
                     else self.text + "|" if self.text_input_flag and self.counter < 5 and '|' not in self.text
                     else self.text)
        self.counter = self.counter if self.counter < 100 else 0

        color = 'black' if self.text_input_flag else 'green'

        text_surface = font.render(self.text[:11] if len(self.text) <= 11 else self.text[len(self.text) - 11:],
                                   True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, new_text_x, new_text_y, new_w, new_h):
        self.x, self.y, self.width, self.height = new_text_x, new_text_y, new_w, new_h
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect(topleft=(new_text_x, new_text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.text_input_flag = True
            else:
                self.text_input_flag = False
        elif event.type == pygame.KEYDOWN and self.text_input_flag:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text.replace('|', '')
                self.text = self.text[:-1]
                self.text += "|"
            elif event.key == pygame.K_RETURN:
                self.text = self.text.replace('|', '')
                self.text_input_flag = False
                return self.text
            elif self.only_digits is False or event.unicode.isdigit():
                self.text = self.text.replace('|', '')
                self.text += event.unicode
                self.text += "|"
        return None


class LoadingScreen:
    def __init__(self, key_flag=True, asleep=-1, parent=None, titles=None, image_name='loading_screen.jpg'):
        self.titles = [] if titles is None else titles
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)
            win_title_dict = lang_json[self.curr_lang]["WIN_TITLES"]
            game_title, load_title = win_title_dict["GAME"], win_title_dict["LOADING"]
        self.key_flag = key_flag
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            pygame.init()
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption(f'{game_title} — {load_title}')
        pygame.mixer.music.stop()
        self.time = asleep
        self.background = pygame.transform.scale(load_image(image_name), (self.width, self.height))
        self.rect = self.background.get_rect(topleft=(0, 0))
        self.font_size = int(0.07 * self.width)
        self.clock = pygame.time.Clock()

    def updates(self, width, height):
        self.width, self.height = width, height
        if width < self.min_width:
            self.width = self.min_width
        if height < self.min_height:
            self.height = self.min_height
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font_size = int(0.07 * self.width)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, self.font_size)
        y_0 = (self.height - len(self.titles) * self.font_size) / 2
        for i, title in enumerate(self.titles):
            text_surface = font.render(title, True, 'white')
            text_rect = text_surface.get_rect(center=(self.width // 2, y_0 + i * self.font_size))
            self.screen.blit(text_surface, text_rect.topleft)

    def run(self):
        elapsed_time = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.key_flag:
                        self.time = 0
                elif ev.type == pygame.VIDEORESIZE:
                    self.updates(ev.w, ev.h)
            self.draw()
            if self.time > 0:
                delta_time = pygame.time.get_ticks() / 1000
                self.time -= delta_time - elapsed_time
                elapsed_time = delta_time
            if -1 != self.time and self.time <= 0:
                return self.exit()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def exit(self):
        return self.screen


class MouseChecking:
    def __init__(self, objects: list):
        """
        :param objects:
        The MouseChecking class to check the location of the mouse to change the cursor.

        When called, it accepts a list of objects in the screen and returns nothing.
        """
        self.dict_cursors = {"Button": pygame.SYSTEM_CURSOR_HAND, "TextInput": pygame.SYSTEM_CURSOR_IBEAM,
                             "DEFAULT": pygame.SYSTEM_CURSOR_ARROW, "Scroll": pygame.SYSTEM_CURSOR_SIZEWE}
        self.objects = objects

    def hovered_checker(self, mouse_pos):
        for obj in self.objects:
            if obj[1].collidepoint(mouse_pos):
                pygame.mouse.set_cursor(self.dict_cursors[obj[0]])
                return
        pygame.mouse.set_cursor(self.dict_cursors["DEFAULT"])

    def change_objects(self, obj: list):
        self.objects = obj


class InGameMenu:
    def __init__(self, screen_width, screen_height):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)
            lang_json_dict = lang_json[self.curr_lang]
            self.continue_text = lang_json_dict["CONTINUE_BUTTON"]
            self.back_menu_text = lang_json_dict["BACK_MENU_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
        self.width, self.height = screen_width, screen_height
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.titles = [self.continue_text, self.back_menu_text, self.exit_text]
        self.buttons = []
        self.objects = []
        self.button_width, self.button_height = 0.35 * screen_width, 0.15 * screen_height
        self.button_x, self.button_y = ((screen_width - self.button_width) / 2,
                                        (screen_height - self.button_height * len(self.titles)) / 2)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click.wav'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(self.background, (128, 128, 128, 10), self.background.get_rect())
        screen.blit(self.background, (0, 0))
        for i in range(len(self.titles)):
            self.buttons[i].hovered_checker(pygame.mouse.get_pos())
            self.buttons[i].draw(screen)


class Entity(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, width, height):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows, width, height)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

    def cut_sheet(self, sheet, columns, rows, width, height):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, (frame_width, frame_height)))
                frame = pygame.transform.scale(frame, (width, height))
                self.frames.append(frame)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Card(pygame.sprite.Sprite):
    def __init__(self, suit, value, volume, /, x: int = 0, y: int = 0, *, width: Optional[Union[float, int]],
                 height: Optional[Union[float, int]], active=True):
        """ Card sprite """
        super().__init__()
        self.active = active
        self.suit = suit
        self.value = value
        self.volume = volume
        self.text = self.suit + ':' + self.value
        self.width, self.height = width, height
        self.image_file_name = f"cards/card{self.text}.png"
        self.image = load_image(self.image_file_name.replace(':', ''))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.position = x, y
        self.rect = self.image.get_rect()
        self.is_hovered = False
        self.ask_sound, self.card_sound = None, None

    def hovered_checker(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered and self.active:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def draw(self, surface):
        self.rect.topleft = self.position
        surface.blit(self.image, self.rect.topleft)


class RestartMenu:
    def __init__(self, screen_width, screen_height):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)
            lang_json_dict = lang_json[self.curr_lang]
            yes_button, no_button = lang_json_dict["YES_BUTTON"], lang_json_dict["NO_BUTTON"]
            self.ask_restart_text = lang_json_dict["ASK_RESTART"]
        self.width, self.height = screen_width, screen_height
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.titles = [yes_button, no_button]
        self.buttons = []
        self.objects = []
        self.button_width, self.button_height = 0.25 * screen_width, 0.1 * screen_height
        self.button_x, self.button_y = ((screen_width - self.button_width) / 2,
                                        (screen_height - self.button_height * len(self.titles)) / 2)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click.wav'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))

    def draw(self, screen: pygame.surface.Surface):
        text = self.ask_restart_text
        font = pygame.font.Font(None, int(0.05 * self.width))
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect(topleft=(0.12 * self.width, 0.12 * self.height))
        pygame.draw.rect(self.background, (128, 128, 128, 10), self.background.get_rect())
        screen.blit(self.background, (0, 0))
        for i in range(len(self.titles)):
            self.buttons[i].hovered_checker(pygame.mouse.get_pos())
            self.buttons[i].draw(screen)
        screen.blit(text_surface, text_rect)


class WinMenu:
    def __init__(self, screen_width, screen_height):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)
            lang_json_dict = lang_json[self.curr_lang]
            come_back_text, main_menu_text = lang_json_dict["COME_BACK"], lang_json_dict["MAIN_MENU"]
            self.win_text = lang_json_dict["WIN_MENU"]["WIN_TEXT"]
            self.lose_text = lang_json_dict["WIN_MENU"]["LOSE_TEXT"]
            self.tie_text = lang_json_dict["WIN_MENU"]["TIE_TEXT"]
        self.width, self.height = screen_width, screen_height
        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.titles = [come_back_text, main_menu_text]
        self.buttons = []
        self.objects = []
        self.button_width, self.button_height = 0.25 * screen_width, 0.1 * screen_height
        self.button_x, self.button_y = ((screen_width - self.button_width) / 2,
                                        (screen_height - self.button_height * len(self.titles)) / 2)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click.wav'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))

    def draw(self, screen: pygame.surface.Surface, rp: int, game_res: Optional[Union[bool, None]]):
        text = (f'{self.win_text} {rp}$' if game_res else f'{self.lose_text} {rp}$' if game_res is not None
                else self.tie_text)
        font = pygame.font.Font(None, int(0.05 * self.width))
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect(topleft=(0.12 * self.width, 0.12 * self.height))
        pygame.draw.rect(self.background, (242, 202, 24, 10), self.background.get_rect())
        screen.blit(self.background, (0, 0))
        for i in range(len(self.titles)):
            self.buttons[i].hovered_checker(pygame.mouse.get_pos())
            self.buttons[i].draw(screen)
        screen.blit(text_surface, text_rect)
