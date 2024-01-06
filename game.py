from functions import load_image, load_settings, terminate
from objects import MouseChecking, Button, InGameMenu, LoadingScreen, Entity, Card
import pygame
import menu
import random


CARD_VALUES = ["A", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
FACE_DOWN_IMAGE = "cards/cardBack_red2.png"


class GameApp:

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
                card = Card(card_suit, card_value, self.curr_volume, width=0.07 * self.width, height=0.20 * self.height)
                self.card_list.append(card)
        random.shuffle(self.card_list)
        self.crab_cards = []
        self.player_cards = []
        for i in range(8):
            self.crab_cards.append(self.card_list.pop(random.randint(0, len(self.card_list) - 1)))
            self.player_cards.append(self.card_list.pop(random.randint(0, len(self.card_list) - 1)))
            self.player_cards[i].position = (0.088 * self.width + 0.08 * self.width * i, 0.725 * self.height)
            self.objects.append(("Button", self.player_cards[i].rect))
        self.player_cards.sort(key=lambda bitch_card: (bitch_card.value, bitch_card.suit))
        self.mouse_checking = MouseChecking(self.objects)
        print([(i.suit, i.value) for i in self.player_cards],
              [(i.suit, i.value) for i in self.crab_cards], sep="\n")

    def run(self):
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
                        pass
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
            else:
                self.mouse_checking.change_objects(self.objects)

            for button in self.buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(self.screen)

            for card in self.crab_cards:
                card.set_persona("crab")

            for card in self.player_cards:
                card.set_persona("player")
                card.hovered_checker(pygame.mouse.get_pos())
                card.draw(self.screen)

            if self.counter_for_animation > 10:
                self.counter_for_animation = 0
                if self.animation:
                    self.crab.update()
                else:
                    self.crabby_cards.update()
            else:
                self.counter_for_animation += 1
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    app = GameApp()
    app.run()