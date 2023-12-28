import pygame
import sys
import menu
from functions import load_settings, load_image, update_settings
from objects import Button


class SettingsApp:
    fps, CURR_VOLUME, width, height, min_width, min_height = load_settings()
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    # Параметры для слайдера
    slider_x = 50
    slider_y = 150
    slider_width = 300
    slider_height = 20
    slider_circle_radius = 10

    def __init__(self, parent=None):
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Settings')

        self.background = load_image('background_folder.jpg')
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.curr_fps = self.fps

        self.slider_circle_x = self.slider_x + int((self.curr_fps - 30) / 120 * self.slider_width)
        self.dragging = False

    @staticmethod
    def draw_text(screen, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def run(self):
        titles = ['SAVE', 'BACK']
        buttons = []
        w, h = 0.2 * self.width, 0.1 * self.height
        button_x, button_y = 0.9 * (self.width - w * len(titles)), 0.95 * (self.height - h)
        for i in range(len(titles)):
            buttons.append(Button(x=button_x + i * (w + 0.2 * w), y=button_y, image_name='green_button.jpg',
                                  width=w, height=h, text=titles[i], volume=self.CURR_VOLUME, screen_width=self.width,
                                  sound_name='click1.ogg'))

        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.slider_circle_x - self.slider_circle_radius <= mouse_x <= self.slider_circle_x + \
                            self.slider_circle_radius and \
                            self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                        self.dragging = True
                elif ev.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif ev.type == pygame.VIDEORESIZE:
                    if ev.w < self.min_width:
                        self.width = self.min_width
                    else:
                        self.width = ev.w
                    if ev.h < self.min_height:
                        self.height = self.min_height
                    else:
                        self.height = ev.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                elif ev.type == pygame.MOUSEMOTION and self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.slider_circle_x = min(max(mouse_x, self.slider_x), self.slider_x + self.slider_width)
                    self.curr_fps = int(((self.slider_circle_x - self.slider_x) / self.slider_width) * 120 + 30)
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "BACK":
                        menu.MenuApp(parent=self.screen)
                    elif ev.button.text == "SAVE":
                        self.fps = self.curr_fps
                        update_settings(fps_update=self.curr_fps)
                for button in buttons:
                    button.handle_event(ev)

            for button in buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.draw_text(self.screen, "Настройки", self.font, self.BLACK, 10, 10)
            self.draw_text(self.screen, f"FPS: {self.curr_fps}", self.small_font, self.BLACK, 20, 60)

            pygame.draw.rect(self.screen, self.GRAY, (self.slider_x, self.slider_y, self.slider_width,
                                                      self.slider_height))
            pygame.draw.circle(self.screen, self.BLACK, (self.slider_circle_x, self.slider_y + self.slider_height // 2),
                               self.slider_circle_radius)
            pygame.display.flip()


if __name__ == "__main__":
    app = SettingsApp()
    app.run()
