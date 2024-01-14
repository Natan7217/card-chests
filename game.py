from functions import load_image, load_settings, terminate, load_sound
from objects import MouseChecking, Button, InGameMenu, LoadingScreen, Entity, Card, RestartMenu
import pygame
import menu
import random

CARD_VALUES = ["A", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
FACE_DOWN_IMAGE = "cards/cardBack_red2.png"


class GameApp:
    def __init__(self, parent=None, player='Natan', *, bet: int):
        self.fps, self.curr_fps, self.vol, self.curr_vol, self.diff, self.curr_diff, self.lang, self.curr_lang, \
            self.width, self.height, self.min_width, self.min_height = load_settings()
        with open("config/lang.json", encoding="utf-8") as lang_file:
            self.lang_json = json.load(lang_file)
            lang_json_dict = self.lang_json[self.curr_lang]
            self.win_title = lang_json_dict["WIN_TITLES"]["GAME"]
            self.continue_text = lang_json_dict["CONTINUE_BUTTON"]
            self.back_menu_text = lang_json_dict["BACK_MENU_BUTTON"]
            self.exit_text = lang_json_dict["EXIT_BUTTON"]
            self.restart_text = lang_json_dict["RESTART_BUTTON"]
            self.loading_text = lang_json_dict["LOADING_TEXT"]
            self.no_button, self.yes_button = lang_json_dict["NO_BUTTON"], lang_json_dict["YES_BUTTON"]
            self.come_back_text, self.main_menu_text = lang_json_dict["COME_BACK"], lang_json_dict["MAIN_MENU"]
            self.diff_ind = lang_json_dict["SETTINGS_MENU"]["DIFFICULT"].index(self.curr_diff)
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        if parent is None:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = parent
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.player = player
        self.menu_flag, self.restart_flag = False, False
        pygame.mixer.music.load('./music/gameplay_music.wav')
        pygame.mixer.music.set_volume(0.3 * self.curr_volume / 1000)
        pygame.mixer.music.play(loops=-1)
        pygame.display.set_caption('Card-chests v1.0')
        self.menu = InGameMenu(self.width, self.height)
        self.restart_menu = RestartMenu(self.width, self.height)
        self.menu_objects = self.menu.objects
        self.clock = pygame.time.Clock()
        self.objects = []
        self.buttons = []
        self.titles = ['RESTART']
        self.crab = Entity(load_image("crab_idle.png"), 4, 1, self.width // 1.001 - self.width * 0.7,
                           - self.height * 0.13, self.width * 0.4, self.height * 0.95)
        self.crabby_cards = Entity(load_image("crab_attack.png"), 5, 1,
                                   self.width // 1.001 - self.width * 0.7,
                                   - self.height * 0.13, self.width * 0.4, self.height * 0.95)
        self.button_width, self.button_height = 0.2 * self.width, 0.12 * self.height
        self.button_x, self.button_y = 0.08 * self.width, 0.00001 * self.height
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
        self.background = pygame.transform.scale(load_image('casino_background.jpg'), (self.width, self.height))
        self.table = pygame.transform.scale(load_image('table.jpg', color_key=-1), (self.width, self.height))
        self.curr_fps = self.fps
        self.counter_for_animation = 0
        self.animation = True
        self.tables = [pygame.transform.scale(load_image('cards_table.jpg'),
                                              (0.8 * self.width, 0.25 * self.height)),
                       pygame.transform.scale(load_image('cards_table_for_enemy.jpg'),
                                              (0.35 * self.width, 0.1 * self.height))]
        self.card_list = []
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, self.curr_volume, width=0.07 * self.width, height=0.2 * self.height)
                self.card_list.append(card)
        random.shuffle(self.card_list)
        self.crab_cards = []
        self.player_cards = []
        for i in range(8):
            self.crab_cards.append(self.card_list.pop(random.randint(0, len(self.card_list) - 1)))
            self.player_cards.append(self.card_list.pop(random.randint(0, len(self.card_list) - 1)))
        self.cards_sorter()
        self.dict_of_player, self.dict_of_crab = {}, {}

        self.current_player = True  # True - player / False - crab
        self.crab_score, self.player_score = 0, 0

        self.mouse_checking = MouseChecking(self.objects)

    def cards_sorter(self):
        self.player_cards = sorted(self.player_cards, key=lambda k: k.value)
        spacer = 0
        repetitions = {}
        for i in range(len(self.player_cards)):
            if self.player_cards[i].value not in repetitions.keys():
                if i != 0:
                    spacer += 1
                repetitions[self.player_cards[i].value] = 1
                y = 0.725 * self.height
                self.player_cards[i].active = True if (repetitions[self.player_cards[i].value] ==
                                                       sum(1 for j in self.player_cards
                                                           if j.value == self.player_cards[i].value)) else False
            else:
                upper = repetitions[self.player_cards[i].value]
                y = 0.725 * self.height - upper * self.height * 0.02
                repetitions[self.player_cards[i].value] += 1
                self.player_cards[i].active = True if (repetitions[self.player_cards[i].value] ==
                                                       sum(1 for j in self.player_cards
                                                           if j.value == self.player_cards[i].value)) else False
            self.player_cards[i].position = (0.088 * self.width + 0.08 * self.width * spacer, y)
            self.objects.append(("Button", self.player_cards[i].rect))
        self.dict_of_player = {}
        self.dict_of_crab = {}
        for i in self.player_cards:
            self.dict_of_player[i.value] = sum(1 for j in self.player_cards if j.value == i.value)
        for g in self.crab_cards:
            self.dict_of_crab[g.value] = sum(1 for y in self.crab_cards if g.value == y.value)

    @staticmethod
    def voice_play(person='player', action='attack', asking=False):
        if asking:
            load_sound(f'{person}_ask_cards.ogg').play()
            pygame.time.wait(1850)
        load_sound(f'{person}_{action}.ogg').play()
        pygame.time.wait(1850)

    def random_card_search(self):
        if self.card_list:
            random_card = self.card_list.pop(random.randint(0, len(self.card_list) - 1)) if self.diff_ind else \
                self.card_list.pop()
            if self.current_player:
                self.player_cards.append(random_card)
                self.cards_sorter()
                self.current_player = not self.current_player
            else:
                self.crab_cards.append(random_card)
                self.current_player = not self.current_player
        if self.current_player is False:
            self.animation = not self.animation

    def cards_in_crab_checker(self, value):
        steal_cards = [card for card in self.crab_cards if value == card.value]
        if len(steal_cards) > 0:
            for each_steal in steal_cards:
                self.player_cards.append(each_steal)
                self.crab_cards.remove(each_steal)
            self.cards_sorter()
            self.animation = not self.animation
        else:
            self.voice_play(person='crab', action='attack', asking=False)
            self.random_card_search()
            self.cards_sorter()
            self.animation = not self.animation

    def crab_ai(self):
        if not self.crab_cards:
            self.random_card_search()
        random_crab_card = random.choice(self.crab_cards)
        self.voice_play(person='crab',
                        action=random_crab_card.value, asking=True)
        self.cards_in_player_checker(random_crab_card.value)

    def cards_in_player_checker(self, value):
        steal_cards = [card for card in self.player_cards if value == card.value]
        if len(steal_cards) > 0:
            for each_steal in steal_cards:
                self.crab_cards.append(each_steal)
                self.player_cards.remove(each_steal)
            self.cards_sorter()
            self.animation = not self.animation
        else:
            self.voice_play(person='player', action='attack', asking=False)
            self.random_card_search()
            self.animation = not self.animation

    def chest_checker(self):
        deleted_list_crab, deleted_list_player = [], []
        a_list, b_list = [], []
        if 4 in self.dict_of_player.values():
            for key in self.dict_of_player.keys():
                if self.dict_of_player[key] == 4:
                    self.player_score += 1
                    deleted_list_player.append(key)

        if 4 in self.dict_of_crab.values():
            for kkey in self.dict_of_crab.keys():
                if self.dict_of_crab[kkey] == 4:
                    self.crab_score += 1
                    deleted_list_crab.append(kkey)
        for card in self.player_cards:
            if card.value not in deleted_list_player:
                b_list.append(card)
        for card in self.crab_cards:
            if card.value not in deleted_list_crab:
                a_list.append(card)
        self.player_cards, self.crab_cards = b_list, a_list

    def score_render(self):
        text = f'{self.player_score}:{self.crab_score}'
        font = pygame.font.Font(None, int(0.11 * self.width))
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect(topleft=(0.089 * self.width, 0.12 * self.height))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        attack_timer = 0
        while True:
            self.screen.blit(self.background, (0, 0))
            if self.animation:
                self.crab.draw(self.screen)
            else:
                self.crabby_cards.draw(self.screen)
            self.screen.blit(self.table, (0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.menu_flag = True
                    elif ev.key == pygame.K_SPACE:
                        self.animation = not self.animation
                elif ev.type == pygame.USEREVENT:
                    if ev.button.text == " ":
                        self.menu_flag = True
                        break
                    elif ev.button.text == 'RESTART':
                        self.restart_flag = True
                    else:
                        if self.current_player:
                            self.voice_play(person='player' if self.current_player else 'crab',
                                            action=ev.button.text.split(':')[1], asking=True)
                            self.cards_in_crab_checker(value=ev.button.text.split(':')[1])
                for button in self.buttons:
                    button.handle_event(ev)
                for card in self.player_cards:
                    card.handle_event(ev)

            self.screen.blit(self.tables[0], (0.07 * self.width, 0.7 * self.height))
            self.screen.blit(self.tables[1], (0.34 * self.width, 0.4 * self.height))

            self.mouse_checking.hovered_checker(pygame.mouse.get_pos())

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
            elif self.restart_flag:
                self.mouse_checking.change_objects(self.restart_menu.objects)
                while True:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            terminate()
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_ESCAPE:
                                self.restart_flag = False
                                break
                        elif ev.type == pygame.USEREVENT:
                            if ev.button.text == "NO":
                                self.restart_flag = False
                                break
                            elif ev.button.text == 'YES':
                                restart_app = GameApp(player=self.player)
                                restart_app.run()
                        for button in self.restart_menu.buttons:
                            button.handle_event(ev)
                    for button in self.restart_menu.buttons:
                        button.hovered_checker(pygame.mouse.get_pos())
                    self.restart_menu.draw(self.screen)
                    pygame.display.flip()
                    self.mouse_checking.hovered_checker(pygame.mouse.get_pos())
                    self.clock.tick(self.fps)
                    if not self.restart_flag:
                        break
            else:
                self.mouse_checking.change_objects(self.objects)
            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)

            if self.current_player is False:
                self.crab_ai()

            for card in self.player_cards:
                if self.current_player:
                    card.hovered_checker(pygame.mouse.get_pos())
                card.draw(self.screen)
                self.cards_sorter()
            self.chest_checker()

            if self.counter_for_animation > 10:
                self.counter_for_animation = 0
                if self.animation:
                    self.crab.update()
                else:
                    self.crabby_cards.update()
                    if attack_timer > 5:
                        self.animation = not self.animation
                        attack_timer = 0
                    else:
                        attack_timer += 1
            else:
                self.counter_for_animation += 1
            if ((len(self.player_cards) == 0 or len(self.crab_cards) == 0) and len(self.card_list) == 0
                    or self.player_score == 5 or self.crab_score == 5 or self.card_list == 0):
                self.game_exit()
            self.score_render()
            self.clock.tick(self.fps)
            pygame.display.flip()

    def game_exit(self):
        pass  # WinWindow


if __name__ == '__main__':
    app = GameApp()
    app.run()
