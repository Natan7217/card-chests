import pygame
import menu
from functions import load_settings, load_image, terminate
from objects import Button, TextInput, MouseChecking, LoadingScreen
import city


class StartApp:
    def __init__(self, parent=None):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_caption('Card-chests v1.0')
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(load_image('background_folder.jpg'), (self.width, self.height))
        self.curr_fps = self.fps

        self.titles = ['START', 'BACK']
        self.buttons = []
        self.objects = []
        self.mouse_checking = MouseChecking(self.objects)
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = (0.9 * (self.width - self.button_width * len(self.titles)),
                                        0.95 * (self.height - self.button_height))

        self.text_x, self.text_y = 0.01 * self.width, 0.01 * self.height
        self.text_width, self.text_height = 0.4 * self.width, 0.075 * self.height

        self.text_input = TextInput(x=self.text_x, y=self.text_y, width=self.text_width, height=self.text_height,
                                    image_name='text_input.jpg', screen_width=self.width)
        self.objects.append((self.text_input.__class__.__name__, self.text_input.rect))
        self.username = ''

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
        self.button_x, self.button_y = (0.9 * (self.width - self.button_width * len(self.titles)),
                                        0.9 * (self.height - self.button_height))
        self.text_x, self.text_y = 0.01 * self.width, 0.01 * self.height
        self.text_width, self.text_height = 0.4 * self.width, 0.075 * self.height
        self.text_input.update(new_text_x=self.text_x, new_text_y=self.text_y,
                               new_w=self.text_width, new_h=self.text_height)
        self.objects.append((self.text_input.__class__.__name__, self.text_input.rect))
        for i in range(len(self.titles)):
            self.buttons[i].update(self.screen, self.button_x + i * (self.button_width + 0.2 * self.button_width),
                                   self.button_y, self.button_width, self.button_height)
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.mouse_checking.change_objects(self.objects)

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
                    elif ev.button.text == "START":
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        loading_screen = LoadingScreen(asleep=10, titles=['Game loading...'],
                                                       key_flag=False, parent=self.screen)
                        self.screen = loading_screen.run()
                        game = city.CityApp(parent=self.screen, player=self.username)
                        game.run()
                for button in self.buttons:
                    button.handle_event(ev)
                text = self.text_input.handle_event(ev)
                if text is not None:
                    self.username = text
            self.screen.blit(self.background, (0, 0))
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.text_input.draw(self.screen)
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = StartApp()
    app.run()
