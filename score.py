import sqlite3
import pygame
import pygame_menu


class ScoreApp:
    def __init__(self):
        conn = sqlite3.connect('score.sqlite')
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                user TEXT
                balance INTEGER
            )
        ''')
        pygame.init()
        self.surface = pygame.display.set_mode((600, 400))

    def set_difficulty(self, value, difficulty):
        # Do the job here !
        pass

    def start_the_game(self):
        # Do the job here !
        pass

    def run(self):
        menu = pygame_menu.Menu('Welcome', 600, 400,
                                theme=pygame_menu.themes.THEME_ORANGE)

        menu.add.text_input('Name:', default='John Doe')
        menu.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.surface)


if __name__ == '__main__':
    app = ScoreApp()
    app.run()
