import pygame
from functions import load_image, load_sound
from config.settings import FPS

pygame.init()
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
menu_width, menu_height = 0.75 * screen_width, 0.75 * screen_height
clock = pygame.time.Clock()
screen = pygame.display.set_mode((menu_width, menu_height))
pygame.display.set_caption('Game menu')
background = load_image('background_folder.jpg')


class Button:
    def __init__(self, x, y, width, height, text, image_name, hover_image_name=None, sound_name=None):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.text = text
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(hover_image_name), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = load_sound(sound_name) if sound_name else None
        self.is_hovered = False

    def draw(self, surface):
        top_image = self.hover_image if self.is_hovered else self.image
        surface.blit(top_image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * menu_width))

        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def hovered_checker(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()


def main_window():
    running = True
    buttons = []
    titles = ['PLAY', 'SETTINGS', 'EXIT']
    w, h = 0.2 * menu_width, 0.1 * menu_height
    button_x, button_y = (menu_width - w) / 2, (menu_height - h * len(titles)) / 2
    for i in range(len(titles)):
        buttons.append(Button(x=button_x, y=button_y + i * (h + 0.2 * h), image_name='green_button.jpg',
                              width=w, height=h, text=titles[i], sound_name='click.wav'))
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(ev)
        screen.blit(background, (0, 0))
        for button in buttons:
            button.hovered_checker(pygame.mouse.get_pos())
            button.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main_window()
