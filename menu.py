import pygame
from functions import load_settings, load_image, terminate
from objects import Button, MouseChecking
import settings
import game_start
import score


class MenuApp:

    def __init__(self, parent=None):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.load('./music/main_menu_music.wav')
            pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.05 * self.curr_volume / 100)
        pygame.display.set_caption('Card-chests v1.0')
        self.clock = pygame.time.Clock()
        self.titles = ['PLAY', "SCORE", 'SETTINGS', 'EXIT']
        self.buttons = []
        self.objects = []
        self.button_width, self.button_height = 0.2 * self.width, 0.1 * self.height
        self.button_x, self.button_y = ((self.width - self.button_width) / 2,
                                        (self.height - self.button_height * len(self.titles)) / 2)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x,
                                       y=self.button_y + i * (self.button_height + 0.2 * self.button_height),
                                       image_name='green_button.jpg', width=self.button_width,
                                       height=self.button_height, text=self.titles[i], volume=self.curr_volume,
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
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.VIDEORESIZE:
                    self.buttons_update(ev.w, ev.h)
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "EXIT":
                        terminate()
                    elif ev.button.text == "SETTINGS":
                        settings_app = settings.SettingsApp(parent=self.screen)
                        settings_app.run()
                    elif ev.button.text == "SCORE":
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


if __name__ == '__main__':
    app = MenuApp()
    app.run()
