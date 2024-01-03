import pygame
import menu
from functions import load_settings, load_image, terminate
from objects import Button, MouseChecking, ScrollBar


class ScoreApp:
    def __init__(self, parent=None):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0 — Score')
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(load_image('background_folder.jpg'), (self.width, self.height))
        self.titles = ['BACK']
        self.buttons = []
        self.objects = []
        self.mouse_checking = MouseChecking(self.objects)
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = (0.95 * (self.width - self.button_width * len(self.titles)),
                                        0.95 * (self.height - self.button_height))
        self.curr_fps = self.fps
        self.scroll_offset = 0
        self.scroll_speed = 0.005 * self.width
        self.scores_data = [("Playeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer1", 100), ("Player2", 95), ("Player3", 85),
                            ("Player4", 75), ("Player5", 60), ("Player6", 50),
                            ("Player7", 40), ("Player8", 30), ("Player9", 20),
                            ("Player10", 10), ("Player11", 8), ("Player12", 6), ("Player13", 3), ('Player14', 3),
                            ("Player15", 3), ("Player16", 3), ('Player17', 2), ('Player18', 1)]
        self.scroll_bar = ScrollBar(image_height=0.09 * self.height * len(self.scores_data),
                                    screen_height=self.screen.get_height(), screen_width=self.screen.get_width())
        print(0.09 * self.height * len(self.scores_data))
        print(self.height)

    def updates(self, width, height):
        self.objects = []
        self.width, self.height = width, height
        if width < self.min_width:
            self.width = self.min_width
        if height < self.min_height:
            self.height = self.min_height
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = (0.95 * (self.width - self.button_width * len(self.titles)),
                                        0.95 * (self.height - self.button_height))
        for i in range(len(self.titles)):
            self.buttons[i].update(self.screen, self.button_x + i * (self.button_width + 0.2 * self.button_width),
                                   self.button_y, self.button_width, self.button_height)
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.scroll_speed = 0.005 * self.width
        self.draw()

    def draw(self):
        font = pygame.font.Font(None, int(0.07 * self.width))
        max_text_width = self.width - 2 * 10
        line_height = 0.09 * self.height
        y = 0
        for index, (username, score) in enumerate(self.scores_data):
            text = f'{username} - {score}'
            if font.size(text)[0] > max_text_width:
                text = text[:int(0.6 * len(text))] + '...'
            score_text = font.render(text, True, 'white')
            self.screen.blit(score_text, (10, y - self.scroll_offset))
            y += line_height

        for button in self.buttons:
            button.hovered_checker(pygame.mouse.get_pos())
            button.draw(self.screen)
        text_area = load_image("instruments.png")
        text_area = pygame.transform.scale(text_area, (self.width, y))
        self.screen.blit(text_area, (0, self.scroll_bar.y_axis), pygame.rect.Rect(0, 0, 0, 0))
        self.scroll_bar.draw(self.screen)

    def run(self):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x + i * (self.button_width + self.button_width * 0.2),
                                       y=self.button_y, image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_volume,
                                       screen_width=self.width, sound_name='click1.ogg'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking.change_objects(self.objects)
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.VIDEORESIZE:
                    self.updates(ev.w, ev.h)
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "BACK":
                        menu_app = menu.MenuApp(parent=self.screen)
                        menu_app.run()
                for button in self.buttons:
                    button.handle_event(ev)
                self.scroll_bar.event_handler(ev)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.scroll_offset = (self.scroll_offset if self.scroll_offset + self.scroll_speed > self.height
                                      else self.scroll_offset + self.scroll_speed)
            elif keys[pygame.K_UP]:
                self.scroll_offset = (self.scroll_offset if self.scroll_offset - self.scroll_speed < 0
                                      else self.scroll_offset - self.scroll_speed)
            self.scroll_bar.update()
            self.draw()
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = ScoreApp()
    app.run()
