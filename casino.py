import pygame
from functions import load_image, load_settings, terminate
from objects import MouseChecking, Button, InGameMenu, LoadingScreen
import menu
import city


class CasinoApp:
    def __init__(self, parent=None, player='Natan'):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if parent is None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = parent
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.player = player
        self.menu_flag = False
        pygame.mixer.music.load('./music/casino_soundtrack.wav')
        pygame.mixer.music.set_volume(0.03 * self.curr_volume / 100)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption('Card-chests v1.0')
        self.menu = InGameMenu(self.width, self.height)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.objects = []
        self.buttons = []
        self.titles = ['PLAY', 'BACK']
        self.button_width, self.button_height = 0.2 * self.width, 0.12 * self.height
        self.button_x, self.button_y = 0.25 * self.width, 0.6 * self.height
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.07 * self.width,
                           height=0.098 * self.height, text=' ', volume=self.curr_volume, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=self.button_x + i * (self.button_width + 0.2 * self.button_width),
                                       y=self.button_y,
                                       image_name='bank_button.png', width=self.button_width, height=self.button_height,
                                       text=self.titles[i], volume=self.curr_volume, screen_width=self.width,
                                       sound_name='click.wav', color_key=-1))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        self.buttons.append(self.exit)
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        self.mouse_checking = MouseChecking(self.objects)

        self.background = pygame.transform.scale(load_image('casino_background.jpg'), (self.width, self.height))
        self.table = pygame.transform.scale(load_image('table.jpg', color_key=-1), (self.width, self.height))
        self.curr_fps = self.fps

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.table, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == " ":
                        self.menu_flag = True
                        break
                    elif ev.button.text == 'PLAY':
                        pass
                    elif ev.button.text == 'BACK':
                        city_app = city.CityApp(player=self.player)
                        city_app.run()
                for button in self.buttons:
                    button.handle_event(ev)
            if self.menu_flag:
                self.mouse_checking.change_objects(self.menu_objects)
                while True:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            terminate()
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_ESCAPE:
                                self.menu_flag = False
                                break
                        elif ev.type == pygame.USEREVENT:
                            if ev.button.text == "CONTINUE":
                                self.menu_flag = False
                                break
                            elif ev.button.text == "BACK TO MAIN MENU":
                                loading_screen = LoadingScreen(asleep=10, titles=['Game loading...'], key_flag=False)
                                screen = loading_screen.run()
                                menu_app = menu.MenuApp(parent=screen)
                                menu_app.run()
                            elif ev.button.text == 'EXIT':
                                terminate()
                        for button in self.menu.buttons:
                            button.handle_event(ev)
                    for button in self.menu.buttons:
                        button.hovered_checker(pygame.mouse.get_pos())
                        self.menu.draw(self.screen)
                    pygame.display.flip()
                    self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
                    self.clock.tick(self.fps)
                    if not self.menu_flag:
                        break
            else:
                self.mouse_checking.change_objects(self.objects)
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = CasinoApp()
    app.run()
