import os
import pygame
import json


pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as e:
        print('Cannot open image', e)
        return None

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_sound(name):
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as e:
        print('Cannot open sound', e)
    else:
        return sound


def load_settings():
    base_screen_width, base_screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    with open("config/settings.json") as file:
        file = json.load(file)
        fps = file["CURR_FPS"]
        volume = file["CURR_VOLUME"]
        screen_width, screen_height = file["SCREEN_WIDTH"], file["SCREEN_HEIGHT"]
    return fps, volume, base_screen_width * screen_width, base_screen_height * screen_height


def update_settings(fps_update=None, volume_update=None):
    with open('config/settings.json') as file:
        data = json.load(file)
    if fps_update:
        data["CURR_FPS"] = fps_update
    if volume_update:
        data["CURR_VOLUME"] = volume_update
    with open('config/settings.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
