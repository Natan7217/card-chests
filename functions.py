import os
import pygame
import json
from typing import Optional, Union

pygame.init()


def load_image(name, color_key=None) -> Optional[Union[pygame.Surface, None]]:
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as e:
        print('Cannot open image', e)
        return None

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        if color_key == -2:
            color_key = "white"
            image.set_colorkey(color_key)
            image = pygame.transform.flip(image.copy(), True, False)
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_sound(name) -> Optional[Union[pygame.mixer.Sound, None]]:
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as e:
        print('Cannot open sound', e)
        return None
    else:
        return sound


def load_settings() -> tuple[int, int, int, int, str, str, str, str, int, int, int, int]:
    base_screen_width, base_screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    with open("config/settings.json", encoding="utf-8") as file:
        file = json.load(file)
        fps, curr_fps = file["FPS"], file["CURR_FPS"]
        volume, curr_volume = file["VOLUME"], file["CURR_VOLUME"]
        dif, curr_dif = file["DIFFICULT"], file["CURR_DIFFICULT"]
        lang, curr_lang = file["LANGUAGE"], file["CURR_LANGUAGE"]
        screen_width, screen_height = file["SCREEN_WIDTH"], file["SCREEN_HEIGHT"]
        min_width, min_height = file["MIN_WIDTH"], file["MIN_HEIGHT"]
    return (fps, curr_fps, volume, curr_volume, dif, curr_dif, lang, curr_lang, base_screen_width * screen_width,
            base_screen_height * screen_height, min_width, min_height)


def update_settings(fps_update=None, volume_update=None, diff_update=None, lang_update=None):
    with open('config/settings.json', encoding="utf-8") as file:
        data = json.load(file)
<<<<<<< Updated upstream
    if fps_update:
        data["CURR_FPS"] = fps_update
    if volume_update:
=======
    if fps_update is not None:
        data["CURR_FPS"] = fps_update
    if volume_update is not None:
>>>>>>> Stashed changes
        data["CURR_VOLUME"] = volume_update
    if lang_update is not None:
        data["CURR_LANGUAGE"] = lang_update
    if lang_update is not None and diff_update is not None:
        data["CURR_DIFFICULT"] = diff_update
    with open('config/settings.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
<<<<<<< Updated upstream
=======


def load_data(queue=''):
    try:
        conn = sqlite3.connect('score.sqlite')
        cur = conn.cursor()
        data = cur.execute(queue).fetchall()
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    else:
        return data


def insert_data(username, score):
    try:
        conn = sqlite3.connect('score.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO scores (user, score) VALUES (?, ?)', (username, score))
        conn.commit()
    except Exception as e:
        print(e)
    else:
        return None


def terminate():
    pygame.time.wait(500)
    pygame.quit()
    sys.exit()


def search_player_data(username=''):
    try:
        all_data = sorted(load_data('SELECT user, score FROM scores'), key=lambda x: x[0])
        all_data = sorted(all_data, key=lambda x: x[1])
    except Exception as e:
        print(e)
    else:
        usernames = [i[0] for i in all_data]
        result = None
        name = username
        if name == '':
            name = 'Player'
            for i in range(0, 10000):
                if name + str(i) not in usernames:
                    name = name + str(i)
                    break
        if name not in usernames:
            insert_data(name, 100)
            result = (name, 100)
        elif name in usernames:
            score = 0
            for data in all_data:
                if name == data[0]:
                    score = data[1]
                    break
            result = (name, score)
        if result is None:
            print('TypeError in sqlite3')
            terminate()
        return result
>>>>>>> Stashed changes
