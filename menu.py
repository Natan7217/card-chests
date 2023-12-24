import sys

import pygame
from functions import load_image, load_settings
import settings
from objects import Button


def main_window(fps, volume, width, height, min_width, min_height, parent=None):
    if parent is None:
        pygame.init()
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    else:
        screen = parent
    clock = pygame.time.Clock()
    pygame.display.set_caption('Card-chests v1.0')
    background = load_image('background_folder.jpg')
    buttons = []
    titles = ['PLAY', "SCORE", 'SETTINGS', 'EXIT']
    w, h = 0.2 * width, 0.1 * height
    button_x, button_y = (width - w) / 2, (height - h * len(titles)) / 2
    for i in range(len(titles)):
        buttons.append(Button(x=button_x, y=button_y + i * (h + 0.2 * h), image_name='green_button.jpg',
                              width=w, height=h, text=titles[i], volume=volume, screen_width=width,
                              sound_name='click1.ogg'))
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.VIDEORESIZE:
                width, height = ev.size
                if ev.w < min_width:
                    width = min_width
                if ev.h < min_height:
                    height = min_height
                w, h = 0.2 * width, 0.1 * height
                button_x, button_y = (width - w) / 2, (height - h * len(titles)) / 2
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for i in range(len(titles)):
                    buttons[i].update(screen, button_x, button_y + i * (h + 0.2 * h), w, h)
            elif ev.type == pygame.USEREVENT:
                if ev.button.text == "EXIT":
                    pygame.time.wait(400)
                    pygame.quit()
                    sys.exit()
                elif ev.button.text == "SETTINGS":
                    settings_app = settings.SettingsApp(screen)
                    settings_app.run()
                elif ev.button.text == "SCORE":
                    pass
                else:
                    pass
            for button in buttons:
                button.handle_event(ev)
        screen.blit(background, (0, 0))
        for button in buttons:
            button.hovered_checker(pygame.mouse.get_pos())
            button.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT, MIN_WIDTH, MIN_HEIGHT = load_settings()
    main_window(CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT, MIN_WIDTH, MIN_HEIGHT)
