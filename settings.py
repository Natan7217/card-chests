import pygame
import sys
from functions import load_settings, load_image


class SettingsApp:
    CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT = load_settings()
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
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        else:
            self.screen = parent
            self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Settings')

        self.background = load_image('background_folder.jpg')
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.slider_circle_x = self.slider_x + int((self.CURR_FPS - 30) / 120 * self.slider_width)
        self.dragging = False

    @staticmethod
    def draw_text(screen, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.slider_circle_x - self.slider_circle_radius <= mouse_x <= self.slider_circle_x + \
                            self.slider_circle_radius and \
                            self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                        self.dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.slider_circle_x = min(max(mouse_x, self.slider_x), self.slider_x + self.slider_width)
                    self.CURR_FPS = int(((self.slider_circle_x - self.slider_x) / self.slider_width) * 120 + 30)

            # Отображение текста о выбранном FPS и других параметрах
            self.draw_text(self.screen, "Настройки", self.font, self.BLACK, 10, 10)
            self.draw_text(self.screen, f"FPS: {self.CURR_FPS}", self.small_font, self.BLACK, 20, 60)

            # Отображение слайдера
            pygame.draw.rect(self.screen, self.GRAY, (self.slider_x, self.slider_y, self.slider_width,
                                                      self.slider_height))
            pygame.draw.circle(self.screen, self.BLACK, (self.slider_circle_x, self.slider_y + self.slider_height // 2),
                               self.slider_circle_radius)

            # Обновление экрана
            pygame.display.flip()

        # Выход из приложения
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = SettingsApp()
    app.run()
