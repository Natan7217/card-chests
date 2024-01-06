import pygame
import menu
from functions import load_settings, load_image, update_settings, terminate
from objects import Button, MouseChecking


class SettingsApp:
    fps, volume, width, height, min_width, min_height = load_settings()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    # Параметры для слайдера
    fps_slider_x = 100
    fps_slider_y = 57
    fps_slider_width = 300
    fps_slider_height = 20
    fps_slider_circle_radius = 10

    curr_volume = volume
    min_volume, max_volume = 0, 100
    volume_slider_x = 100
    volume_slider_y = 157
    volume_slider_width = 300
    volume_slider_height = 20
    volume_slider_circle_radius = 10

    curr_volume_slider_x = (volume_slider_x +
                            int((curr_volume - min_volume) / (max_volume - min_volume) * volume_slider_width))
    volume_dragging = False

    def __init__(self, parent=None):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Settings')

        self.curr_volume_slider_x = self.volume_slider_x + int(
            (self.curr_volume - self.min_volume) / (self.max_volume - self.min_volume) * self.volume_slider_width)

        self.background = pygame.transform.scale(load_image('background_folder.jpg'), (self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.curr_fps = self.fps
        self.titles = ['SAVE', 'BACK']
        self.buttons = []
        self.objects = []
        self.volume_slider_rect = pygame.rect.Rect(self.volume_slider_x, self.volume_slider_y,
                                                   self.volume_slider_width, self.volume_slider_height)
        self.fps_slider_rect = pygame.rect.Rect(self.fps_slider_x, self.fps_slider_y,
                                                self.fps_slider_width, self.fps_slider_height)
        self.objects.append(("Scroll", self.volume_slider_rect))
        self.objects.append(("Scroll", self.fps_slider_rect))

        self.slider_circle_x = self.fps_slider_x + int((self.curr_fps - 30) / 120 * self.fps_slider_width)
        self.dragging = False
        self.mouse_checking = MouseChecking(self.objects)

    @staticmethod
    def draw_text(screen, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def buttons_update(self):
        self.objects = []
        w, h = 0.2 * self.width, 0.1 * self.height
        button_x, button_y = 0.9 * (self.width - w * len(self.titles)), 0.95 * (self.height - h)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        for i in range(len(self.titles)):
            self.buttons[i].update(self.screen, button_x + i * (w + 0.2 * w), button_y, w, h)
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.objects.append(("Scroll", self.volume_slider_rect))
        self.objects.append(("Scroll", self.fps_slider_rect))
        self.mouse_checking.change_objects(self.objects)

    def run(self):
        w, h = 0.2 * self.width, 0.1 * self.height
        button_x, button_y = 0.9 * (self.width - w * len(self.titles)), 0.95 * (self.height - h)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=button_x + i * (w + 0.2 * w), y=button_y, image_name='green_button.jpg',
                                       width=w, height=h, text=self.titles[i], volume=self.curr_volume,
                                       screen_width=self.width,
                                       sound_name='click1.ogg'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking.change_objects(self.objects)

        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.slider_circle_x - self.fps_slider_circle_radius <= mouse_x <= self.slider_circle_x + \
                            self.fps_slider_circle_radius and \
                            self.fps_slider_y <= mouse_y <= self.fps_slider_y + self.fps_slider_height:
                        self.dragging = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (self.curr_volume_slider_x - self.volume_slider_circle_radius <= mouse_x <=
                            self.curr_volume_slider_x +
                            self.volume_slider_circle_radius and
                            self.volume_slider_y <= mouse_y <= self.volume_slider_y + self.volume_slider_height):
                        self.volume_dragging = True
                elif ev.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                    self.volume_dragging = False
                elif ev.type == pygame.VIDEORESIZE:
                    if ev.w < self.min_width:
                        self.width = self.min_width
                    else:
                        self.width = ev.w
                    if ev.h < self.min_height:
                        self.height = self.min_height
                    else:
                        self.height = ev.h
                    self.background = pygame.transform.scale(self.background, (self.width, self.height))
                    self.buttons_update()
                elif ev.type == pygame.MOUSEMOTION and self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.slider_circle_x = min(max(mouse_x, self.fps_slider_x),
                                               self.fps_slider_x + self.fps_slider_width)
                    self.curr_fps = int(((self.slider_circle_x - self.fps_slider_x) / self.fps_slider_width) * 120 + 30)

                elif ev.type == pygame.MOUSEMOTION and self.volume_dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.curr_volume_slider_x = min(max(mouse_x, self.volume_slider_x),
                                                    self.volume_slider_x + self.volume_slider_width)
                    self.curr_volume = int(
                        ((self.curr_volume_slider_x - self.volume_slider_x) / self.volume_slider_width) * (
                                    self.max_volume - self.min_volume) + self.min_volume)

                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "BACK":
                        menu_app = menu.MenuApp(parent=self.screen)
                        menu_app.run()
                    elif ev.button.text == "SAVE":
                        self.fps = self.curr_fps
                        self.volume = self.curr_volume
                        update_settings(fps_update=self.curr_fps, volume_update=self.curr_volume)
                for button in self.buttons:
                    button.handle_event(ev)

            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.draw_text(self.screen, "Настройки", self.font, self.WHITE, 10, 10)
            self.draw_text(self.screen, f"FPS: {self.curr_fps}", self.small_font, self.WHITE, 20, 60)
            self.draw_text(self.screen, f"Vol: {self.curr_volume}", self.small_font, self.WHITE, 20, 160)

            pygame.draw.rect(self.screen, self.GRAY, (self.fps_slider_x, self.fps_slider_y, self.fps_slider_width,
                                                      self.fps_slider_height))
            pygame.draw.circle(self.screen, self.BLACK, (self.slider_circle_x,
                                                         self.fps_slider_y + self.fps_slider_height // 2),
                               self.fps_slider_circle_radius)

            pygame.draw.rect(self.screen, self.GRAY,
                             (self.volume_slider_x, self.volume_slider_y, self.volume_slider_width,
                              self.volume_slider_height))
            pygame.draw.circle(self.screen, self.BLACK,
                               (self.curr_volume_slider_x, self.volume_slider_y + self.volume_slider_height // 2),
                               self.volume_slider_circle_radius)

            pygame.display.flip()


if __name__ == "__main__":
    app = SettingsApp()
    app.run()
