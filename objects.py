import sys
import time

import pygame
from functions import load_image, load_sound, load_settings


class Button:
    def __init__(self, x, y, width, height, text, image_name, volume, screen_width, hover_image_name=None,
                 sound_name=None):
        self.x, self.y, self.width, self.height, self.volume = x, y, width, height, volume
        self.screen_width = screen_width
        self.text = text
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        self.hover_image_name = hover_image_name
        if self.hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(self.hover_image_name), (width, height))
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
                self.sound.set_volume(self.volume)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class TextInput:
    def __init__(self, x, y, width, height, image_name, screen_width):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.screen_width = screen_width
        self.text = ''
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.counter = 0
        self.text_input_flag = False
        self.is_hovered = False

    def draw(self, surface):
        self.counter += 1
        surface.blit(self.image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * self.screen_width))
        self.text = (self.text.replace('|', '') if self.text_input_flag and self.counter == 5 and '|' in self.text
                     else self.text + "|" if self.text_input_flag and self.counter < 5 and '|' not in self.text
                     else self.text)
        self.counter = self.counter if self.counter < 100 else 0

        text_surface = font.render(self.text, True, 'black')
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
            else:
                self.text = self.text.replace('|', '')
                self.text += event.unicode
                self.text += "|"
        return None


class LoadingScreen:  # RED FLAG
    def __init__(self, asleep=-1, parent=None, titles=None, image_name='background_folder.jpg'):
        if titles is None:
            self.titles = ['Press any button to continue']
        else:
            self.titles = titles + ['Press any button to continue']
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Loading')
        self.time = asleep
        self.background = pygame.transform.scale(load_image(image_name), (self.width, self.height))
        self.rect = self.background.get_rect(topleft=(0, 0))
        self.font_size = int(0.03 * self.width)
        self.clock = pygame.time.Clock()

    def updates(self, width, height):
        self.width, self.height = width, height
        if width < self.min_width:
            self.width = self.min_width
        if height < self.min_height:
            self.height = self.min_height
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.font_size = int(0.03 * self.width)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, self.font_size)
        y_0 = (self.height - len(self.titles) * self.font_size) / 2
        for i, title in enumerate(self.titles):
            text_surface = font.render(title, True, 'white')
            text_rect = text_surface.get_rect(center=(self.width // 2, y_0 + i * self.font_size))
            self.screen.blit(text_surface, text_rect.topleft)

    def run(self):
        ellapsed_time = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN:
                    print('HEHE')
                    self.time = -1
                elif ev.type == pygame.VIDEORESIZE:
                    self.updates(ev.w, ev.h)
            self.draw()
            if self.time > 0:
                print(self.time)
                delta_time = pygame.time.get_ticks() / 1000
                self.time -= delta_time - ellapsed_time
                ellapsed_time = delta_time
            if -1 < self.time <= 0:
                self.exit()
                break
            pygame.display.flip()
            self.clock.tick(self.fps)

    def exit(self):
        return self.screen


class MouseChecking:
    def __init__(self, objects: list):
        """
        :param objects:
        The MouseChecking class to check the location of the mouse to change the cursor.

        When called, it accepts list of objects in the screen and returns nothing.
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
