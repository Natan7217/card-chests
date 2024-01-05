import sys
import pygame
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

        text_surface = font.render(self.text[:11] if len(self.text) <= 11 else self.text[len(self.text) - 11:],
                                   True, 'black')
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


class LoadingScreen:
    def __init__(self, key_flag=True, asleep=-1, parent=None, titles=None, image_name='loading_screen.jpg'):
        self.titles = [] if titles is None else titles
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        self.key_flag = key_flag
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Loading')
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
        ellapsed_time = 0
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
                self.time -= delta_time - ellapsed_time
                ellapsed_time = delta_time
            if -1 < self.time <= 0:
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


class ScrollBar(object):
    def __init__(self, image_height, screen_width, screen_height):
        self.screen_width, self.screen_height = screen_width, screen_height
        self.y_axis = 0
        self.image_height = image_height
        self.change_y = 0

        bar_height = int((self.screen_height - 40) / (image_height / (self.screen_height * 1.0)))
        self.bar_rect = pygame.Rect(self.screen_width - 20, 20, 20, bar_height)
        self.bar_up = pygame.Rect(self.screen_width - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(self.screen_width - 20, self.screen_height - 20, 20, 20)

        self.bar_up_image = load_image('up.png')
        self.bar_down_image = load_image('down.png')

        self.on_bar = False
        self.mouse_diff = 0

    def update(self):
        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.image_height) < self.screen_height:
            self.y_axis = self.screen_height - self.image_height

        height_diff = self.image_height - self.screen_height

        scroll_length = self.screen_height - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.screen_height - 20):
                self.bar_rect.bottom = self.screen_height - 20

            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery = scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5

        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_y = 5
            elif event.key == pygame.K_DOWN:
                self.change_y = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.change_y = 0
            elif event.key == pygame.K_DOWN:
                self.change_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, 'gray', self.bar_rect)

        screen.blit(self.bar_up_image, (self.screen_width - 20, 0))
        screen.blit(self.bar_down_image, (self.screen_width - 20, self.screen_height - 20))
