import pygame
from functions import load_settings, load_image, terminate
from objects import MouseChecking, Button, InGameMenu


class CityApp:

    def __init__(self, parent=None, player=None):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        if parent is None:
            pygame.init()
        else:
            pygame.quit()
            pygame.init()
        self.player = player
        self.menu_flag = False
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.mixer.music.load('./music/city_soundtrack.wav')
        pygame.mixer.music.set_volume(0.05 * self.curr_volume / 100)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption('Card-chests v1.0')
        self.menu = InGameMenu(self.width, self.height)
        self.menu_objects = self.menu.return_objects()
        self.clock = pygame.time.Clock()
        self.bank = Button(x=0.045 * self.width, y=0.148 * self.height, image_name='bank.png', width=0.44 * self.width,
                           height=0.64 * self.height, text=' ', volume=self.curr_volume, screen_width=self.width,
                           sound_name='click.wav', hover_image_name='bank_hovered.png', color_key=-1)
        self.casino = Button(x=0.55 * self.width, y=0.175 * self.height, image_name='casino.png',
                             width=0.45 * self.width, height=0.64 * self.height, text='  ',
                             volume=self.curr_volume, screen_width=self.width, sound_name='click.wav',
                             hover_image_name='casino_hovered.png', color_key=-1)
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.089 * self.width,
                           height=0.1 * self.height, text='   ', volume=self.curr_volume, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        self.buildings = []
        self.buildings.append(self.bank)
        self.buildings.append(self.casino)
        self.buildings.append(self.exit)
        self.objects = []
        self.objects.append((self.bank.__class__.__name__, self.bank.rect))
        self.objects.append((self.casino.__class__.__name__, self.casino.rect))
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        self.mouse_checking = MouseChecking(self.objects)
        self.background = pygame.transform.scale(load_image('city_background_2.jpg'), (self.width, self.height))
        self.curr_fps = self.fps

    def updates(self, width, height):
        self.objects = []
        self.width, self.height = width, height
        if width < self.min_width:
            self.width = self.min_width
        if height < self.min_height:
            self.height = self.min_height
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.bank = Button(x=0.045 * self.width, y=0.148 * self.height, image_name='bank.png', width=0.44 * self.width,
                           height=0.64 * self.height, text=' ', volume=self.curr_volume, screen_width=self.width,
                           sound_name='click.wav', hover_image_name='bank_hovered.png', color_key=-1)
        self.casino = Button(x=0.55 * self.width, y=0.175 * self.height, image_name='casino.png',
                             width=0.45 * self.width,
                             height=0.64 * self.height, text='  ', volume=self.curr_volume, screen_width=self.width,
                             sound_name='click.wav', hover_image_name='casino_hovered.png', color_key=-1)
        self.exit = Button(x=0.006 * self.width, y=0.01 * self.height, image_name='exit.png', width=0.089 * self.width,
                           height=0.1 * self.height, text='   ', volume=self.curr_volume, screen_width=self.width,
                           sound_name='click.wav', color_key=-1)
        self.objects.append((self.bank.__class__.__name__, self.bank.rect))
        self.objects.append((self.casino.__class__.__name__, self.casino.rect))
        self.objects.append((self.exit.__class__.__name__, self.exit.rect))
        self.mouse_checking.change_objects(self.objects)

    def run(self):
        self.fps, self.curr_volume, self.width, self.height, self.min_width, self.min_height = load_settings()
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.VIDEORESIZE:
                    self.updates(ev.w, ev.h)
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        pass
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "   ":
                        self.menu_flag = True
                    elif ev.button.text == "  ":  # CASINO
                        pass
                    elif ev.button.text == " ":  # BANK
                        pass
                for building in self.buildings:
                    building.handle_event(ev)
            for building in self.buildings:
                building.hovered_checker(pygame.mouse.get_pos())
                building.draw(self.screen)
            if self.menu_flag:
                self.mouse_checking.change_objects(self.menu_objects)
                while True:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            terminate()
                        elif ev.type == pygame.VIDEORESIZE:
                            self.updates(ev.w, ev.h)
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_ESCAPE:
                                pass
                        elif ev.type == pygame.USEREVENT:
                            if ev.button.text == "   ":
                                self.menu_flag = True
                            elif ev.button.text == "  ":  # CASINO
                                pass
                            elif ev.button.text == " ":  # BANK
                                pass
                        for button in self.menu.return_buttons():
                            button.handle_event(ev)
                    for button in self.menu.return_buttons():
                        button.hovered_checker(pygame.mouse.get_pos())
                        self.menu.draw(self.screen)
                    pygame.display.flip()
                    self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
                    self.clock.tick(self.fps)

            else:
                self.mouse_checking.change_objects(self.objects)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = CityApp()
    app.run()
