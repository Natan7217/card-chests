import pygame
<<<<<<< Updated upstream
import sys
import menu
from functions import load_settings, load_image, update_settings
from objects import Button


class SettingsApp:
    fps, CURR_VOLUME, width, height, min_width, min_height = load_settings()
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    # Параметры для слайдера
    slider_x = 50
    slider_y = 150
    slider_width = 300
    slider_height = 20
    slider_circle_radius = 10

    def __init__(self, parent=None):
=======
import main
import menu
import json
from functions import load_settings, load_image, update_settings, terminate
from objects import Button, MouseChecking


class SettingsApp:

    def __init__(self, parent=None):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        self.copy_orig_sett = [self.fps, self.vol, self.diff, self.lang]
        with open("config/lang.json", encoding="utf-8") as lang_file:
            self.lang_json = json.load(lang_file)
            lang_json_dict = self.lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            sett_dict = lang_json_dict["SETTINGS_MENU"]
            self.langs_text = self.lang_json["LANGS"]
            self.sett_text = sett_dict["TEXT"]
            self.fps_text = sett_dict["FPS"]
            self.vol_text = sett_dict["VOLUME"]
            self.diff_list = sett_dict["DIFFICULT"]
            self.save_text = lang_json_dict["SAVE_BUTTON"]
            self.back_text = lang_json_dict["BACK_BUTTON"]
            self.back_sett_text = lang_json_dict["BACK_SETT_BUTTON"]
            self.curr_diff_ind = self.diff_list.index(self.curr_diff)
            self.curr_lang_ind = self.langs_text.index(self.lang_json[self.curr_lang][self.curr_lang])
            self.abr_lang = self.lang_json[self.langs_text[self.curr_lang_ind]]
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        # Параметры для слайдера
        self.fps_slider_x = 100
        self.fps_slider_y = 57
        self.fps_slider_width = 300
        self.fps_slider_height = 20
        self.fps_slider_circle_radius = 10
        self.min_volume, self.max_volume = 0, 100
        self.volume_slider_x = 100
        self.volume_slider_y = 157
        self.volume_slider_width = 300
        self.volume_slider_height = 20
        self.volume_slider_circle_radius = 10
        self.curr_volume_slider_x = (self.volume_slider_x +
                                     int((self.curr_vol - self.min_volume) / (self.max_volume - self.min_volume)
                                         * self.volume_slider_width))

        self.volume = self.curr_vol
        self.volume_dragging = False

>>>>>>> Stashed changes
        if parent is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.screen = parent
            self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        pygame.display.set_icon(load_image('icon.png'))
        pygame.display.set_caption(f'{self.win_title} — {self.sett_text}')

<<<<<<< Updated upstream
        self.background = load_image('background_folder.jpg')
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.curr_fps = self.fps
=======
        self.curr_volume_slider_x = self.volume_slider_x + int(
            (self.curr_vol - self.min_volume) / (self.max_volume - self.min_volume) * self.volume_slider_width)

        self.background = pygame.transform.scale(load_image('background_folder.jpg'), (self.width, self.height))

        self.arrows = []
        arrow_x, arrow_y = 10, 200
        self.arrow_w, self.arrow_space_y = 0.1 * self.height, 0.12 * self.height
        self.lang_left_arrow = Button(x=arrow_x, y=arrow_y, image_name='left_arrow.png',
                                      width=self.arrow_w, height=self.arrow_w, text="", volume=self.curr_vol,
                                      screen_width=self.width, sound_name='click1.ogg', color_key=-1)
        self.lang_right_arrow = Button(x=arrow_x + 350, y=arrow_y, image_name='left_arrow.png',
                                       width=self.arrow_w, height=self.arrow_w, text=" ", volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click1.ogg', color_key=-2)
        self.diff_left_arrow = Button(x=arrow_x, y=arrow_y + self.arrow_space_y, image_name='left_arrow.png',
                                      width=self.arrow_w, height=self.arrow_w, text="  ", volume=self.curr_vol,
                                      screen_width=self.width, sound_name='click1.ogg', color_key=-1)
        self.diff_right_arrow = Button(x=arrow_x + 350, y=arrow_y + self.arrow_space_y, image_name='left_arrow.png',
                                       width=self.arrow_w, height=self.arrow_w, text="   ", volume=self.curr_vol,
                                       screen_width=self.width, sound_name='click1.ogg', color_key=-2)

        self.arrows.append(self.lang_left_arrow)
        self.arrows.append(self.lang_right_arrow)
        self.arrows.append(self.diff_left_arrow)
        self.arrows.append(self.diff_right_arrow)

        self.return_sett_button = Button(x=10, y=0.855 * self.height, image_name='green_button.jpg',
                                         width=0.45 * self.width, height=0.1 * self.height,
                                         text=self.back_sett_text,
                                         volume=self.curr_vol, screen_width=self.width, sound_name='click1.ogg')

        self.big_font = pygame.font.Font(None, 70)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.curr_fps = self.fps
        self.titles = [self.save_text, self.back_text]
        self.buttons = []
        self.objects = []
        self.volume_slider_rect = pygame.rect.Rect(self.volume_slider_x, self.volume_slider_y,
                                                   self.volume_slider_width, self.volume_slider_height)
        self.fps_slider_rect = pygame.rect.Rect(self.fps_slider_x, self.fps_slider_y,
                                                self.fps_slider_width, self.fps_slider_height)
        self.objects.append(("Scroll", self.volume_slider_rect))
        self.objects.append(("Scroll", self.fps_slider_rect))
        self.objects.append((self.return_sett_button.__class__.__name__, self.return_sett_button.rect))
>>>>>>> Stashed changes

        self.slider_circle_x = self.slider_x + int((self.curr_fps - 30) / 120 * self.slider_width)
        self.dragging = False

    @staticmethod
    def draw_text(screen, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

<<<<<<< Updated upstream
=======
    def buttons_update(self):
        self.objects = []
        w, h = 0.2 * self.width, 0.1 * self.height
        button_x, button_y = 0.9 * (self.width - w * len(self.titles)), 0.95 * (self.height - h)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        for i in range(len(self.titles)):
            self.buttons[i].update(self.screen, button_x + i * (w + 0.2 * w), button_y, w, h)
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        for arrow in self.arrows:
            self.objects.append((arrow.__class__.__name__, arrow.rect))
        self.return_sett_button.update(self.screen, 10, 0.855 * self.height, 0.45 * self.width, h)
        self.objects.append(("Scroll", self.volume_slider_rect))
        self.objects.append(("Scroll", self.fps_slider_rect))
        self.objects.append((self.return_sett_button.__class__.__name__, self.return_sett_button.rect))
        self.mouse_checking.change_objects(self.objects)

>>>>>>> Stashed changes
    def run(self):
        titles = ['SAVE', 'BACK']
        buttons = []
        w, h = 0.2 * self.width, 0.1 * self.height
<<<<<<< Updated upstream
        button_x, button_y = 0.9 * (self.width - w * len(titles)), 0.95 * (self.height - h)
        for i in range(len(titles)):
            buttons.append(Button(x=button_x + i * (w + 0.2 * w), y=button_y, image_name='green_button.jpg',
                                  width=w, height=h, text=titles[i], volume=self.CURR_VOLUME, screen_width=self.width,
                                  sound_name='click1.ogg'))
=======
        button_x, button_y = 0.9 * (self.width - w * len(self.titles)), 0.95 * (self.height - h)
        for i in range(len(self.titles)):
            self.buttons.append(Button(x=button_x + i * (w + 0.2 * w), y=button_y, image_name='green_button.jpg',
                                       width=w, height=h, text=self.titles[i], volume=self.curr_vol,
                                       screen_width=self.width,
                                       sound_name='click1.ogg'))
            self.objects.append((self.buttons[i].__class__.__name__, self.buttons[i].rect))
        for arrow in self.arrows:
            self.objects.append((arrow.__class__.__name__, arrow.rect))
        self.mouse_checking.change_objects(self.objects)
>>>>>>> Stashed changes

        while True:
            self.screen.blit(self.background, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.slider_circle_x - self.slider_circle_radius <= mouse_x <= self.slider_circle_x + \
                            self.slider_circle_radius and \
                            self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                        self.dragging = True
                elif ev.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif ev.type == pygame.VIDEORESIZE:
                    if ev.w < self.min_width:
                        self.width = self.min_width
                    else:
                        self.width = ev.w
                    if ev.h < self.min_height:
                        self.height = self.min_height
                    else:
                        self.height = ev.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                elif ev.type == pygame.MOUSEMOTION and self.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
<<<<<<< Updated upstream
                    self.slider_circle_x = min(max(mouse_x, self.slider_x), self.slider_x + self.slider_width)
                    self.curr_fps = int(((self.slider_circle_x - self.slider_x) / self.slider_width) * 120 + 30)
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == "BACK":
                        menu.main_window(fps=self.fps, volume=self.CURR_VOLUME, min_width=self.min_width,
                                         min_height=self.min_height, width=self.width, height=self.height,
                                         parent=self.screen)
                    elif ev.button.text == "SAVE":
                        self.fps = self.curr_fps
                        update_settings(fps_update=self.curr_fps)
                for button in buttons:
=======
                    self.slider_circle_x = min(max(mouse_x, self.fps_slider_x),
                                               self.fps_slider_x + self.fps_slider_width)
                    self.curr_fps = int(((self.slider_circle_x - self.fps_slider_x) / self.fps_slider_width) * 120 + 30)

                elif ev.type == pygame.MOUSEMOTION and self.volume_dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.curr_volume_slider_x = min(max(mouse_x, self.volume_slider_x),
                                                    self.volume_slider_x + self.volume_slider_width)
                    self.curr_vol = int(
                        ((self.curr_volume_slider_x - self.volume_slider_x) / self.volume_slider_width) * (
                                self.max_volume - self.min_volume) + self.min_volume)

                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == self.back_text:
                        menu_app = menu.MenuApp(parent=self.screen)
                        menu_app.run()
                    elif ev.button.text == self.save_text:
                        self.fps = self.curr_fps
                        self.volume = self.curr_vol
                        self.abr_lang = self.lang_json[self.langs_text[self.curr_lang_ind]]
                        self.curr_diff = self.lang_json[self.abr_lang]["SETTINGS_MENU"]["DIFFICULT"][self.curr_diff_ind]
                        update_settings(fps_update=self.curr_fps, volume_update=self.curr_vol,
                                        diff_update=self.curr_diff, lang_update=self.abr_lang)
                    elif ev.button.text == "":
                        self.curr_lang_ind = (self.curr_lang_ind if self.curr_lang_ind > 0 else
                                              len(self.langs_text)) - 1
                    elif ev.button.text == " ":
                        self.curr_lang_ind = (self.curr_lang_ind if self.curr_lang_ind < len(self.langs_text) - 1
                                              else -1) + 1
                    elif ev.button.text == "  ":
                        self.curr_diff_ind = (self.curr_diff_ind if self.curr_diff_ind > 0 else
                                              len(self.diff_list)) - 1
                    elif ev.button.text == "   ":
                        self.curr_diff_ind = (self.curr_diff_ind if self.curr_diff_ind < len(self.diff_list) - 1
                                              else -1) + 1
                    elif ev.button.text == self.back_sett_text:
                        update_settings(fps_update=self.copy_orig_sett[0], volume_update=self.copy_orig_sett[1],
                                        diff_update=self.copy_orig_sett[2], lang_update=self.copy_orig_sett[3])
                        main.run_main()
                for button in self.buttons:
>>>>>>> Stashed changes
                    button.handle_event(ev)
                for arrow in self.arrows:
                    arrow.handle_event(ev)
                self.return_sett_button.handle_event(ev)

            for button in buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)
<<<<<<< Updated upstream
            self.draw_text(self.screen, "Настройки", self.font, self.BLACK, 10, 10)
            self.draw_text(self.screen, f"FPS: {self.curr_fps}", self.small_font, self.BLACK, 20, 60)
=======
            for arrow in self.arrows:
                arrow.hovered_checker(pygame.mouse.get_pos())
                arrow.draw(self.screen)
            self.return_sett_button.hovered_checker(pygame.mouse.get_pos())
            self.return_sett_button.draw(self.screen)
            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
            self.draw_text(self.screen, self.sett_text, self.font, self.WHITE, 10, 10)
            self.draw_text(self.screen, f"{self.fps_text}: {self.curr_fps}", self.small_font, self.WHITE, 20, 60)
            self.draw_text(self.screen, f"{self.vol_text}: {self.curr_vol}", self.small_font, self.WHITE, 20, 160)

            self.draw_text(self.screen, self.langs_text[self.curr_lang_ind], self.big_font, self.WHITE,
                           self.arrow_w + 10, 205)
            self.draw_text(self.screen, self.diff_list[self.curr_diff_ind], self.big_font, self.WHITE,
                           self.arrow_w + 10, 205 + self.arrow_space_y)
            pygame.draw.rect(self.screen, self.GRAY, (self.fps_slider_x, self.fps_slider_y, self.fps_slider_width,
                                                      self.fps_slider_height))
            pygame.draw.circle(self.screen, self.BLACK, (self.slider_circle_x,
                                                         self.fps_slider_y + self.fps_slider_height // 2),
                               self.fps_slider_circle_radius)

            pygame.draw.rect(self.screen, self.GRAY,
                             (self.volume_slider_x, self.volume_slider_y, self.volume_slider_width,
                              self.volume_slider_height))
            pygame.draw.circle(self.screen, self.BLACK,
                               (self.curr_volume_slider_x, self.volume_slider_y + self.volume_slider_height // 2),
                               self.volume_slider_circle_radius)
>>>>>>> Stashed changes

            pygame.draw.rect(self.screen, self.GRAY, (self.slider_x, self.slider_y, self.slider_width,
                                                      self.slider_height))
            pygame.draw.circle(self.screen, self.BLACK, (self.slider_circle_x, self.slider_y + self.slider_height // 2),
                               self.slider_circle_radius)
            pygame.display.flip()


if __name__ == "__main__":
    app = SettingsApp()
    app.run()
