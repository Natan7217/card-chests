from menu import main_window
from functions import load_settings


if __name__ == '__main__':
    CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT = load_settings()
    main_window(CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT)
