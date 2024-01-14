import menu
import json
from objects import LoadingScreen


def run_main():
    with open("config/settings.json", encoding="utf-8") as settings_file:
        settings_json = json.load(settings_file)
        lang = settings_json["CURR_LANGUAGE"]
    with open("config/lang.json", encoding="utf-8") as lang_file:
        lang_json = json.load(lang_file)
        title = lang_json[lang]["LOADING_TEXT"]
    loading_screen = LoadingScreen(asleep=10, titles=[title], key_flag=False)
    screen = loading_screen.run()
    app = menu.MenuApp(parent=screen)
    app.run()


if __name__ == '__main__':
    run_main()
