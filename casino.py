import pygame
from functions import load_image, terminate
from objects import MouseChecking, Button, InGameMenu, LoadingScreen
import menu


class CasinoApp:

    def __init__(self, parent=None, player=None, width=1690, height=890, volume=100, fps=60):
        self.fps, self.curr_volume = fps, volume
        self.width, self.height = width, height
        if parent is None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = parent
        self.player = player
        self.menu_flag = False
        pygame.mixer.music.load('./music/casino_soundtrack.wav')
        pygame.mixer.music.set_volume(0.03 * self.curr_volume / 100)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption('Card-chests v1.0')
        self.menu = InGameMenu(pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.objects = []
        self.mouse_checking = MouseChecking(self.objects)

        self.background = pygame.transform.scale(load_image('casino_background.jpg'), (self.width, self.height))
        self.curr_fps = self.fps

    def updates(self, width, height):
        pass

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.time.wait(500)
                    terminate()
                elif ev.type == pygame.VIDEORESIZE:
                    self.updates(ev.w, ev.h)
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
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
                                pygame.time.wait(500)
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
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = CasinoApp()
    app.run()
