import pygame
from functions import load_image, load_sound, load_settings
from settings import SettingsApp


class Button:
    def __init__(self, x, y, width, height, text, image_name, volume, screen_width, hover_image_name=None,
                 sound_name=None):
        self.x, self.y, self.width, self.height, self.volume = x, y, width, height, volume
        self.screen_width = screen_width
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
        font = pygame.font.Font(None, int(0.03 * self.screen_width))

        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def hovered_checker(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.set_volume(self.volume)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


def main_window(fps, volume, width, height, parent=None):
    if parent is None:
        pygame.init()
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    else:
        screen = parent
    clock = pygame.time.Clock()
    pygame.display.set_caption('Card-chests v1.0')
    background = load_image('background_folder.jpg')
    running = True
    buttons = []
    titles = ['PLAY', "SCORE", 'SETTINGS', 'EXIT']
    w, h = 0.2 * width, 0.1 * height
    button_x, button_y = (width - w) / 2, (height - h * len(titles)) / 2
    for i in range(len(titles)):
        buttons.append(Button(x=button_x, y=button_y + i * (h + 0.2 * h), image_name='green_button.jpg',
                              width=w, height=h, text=titles[i], volume=volume, screen_width=width,
                              sound_name='click1.ogg'))
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.VIDEORESIZE:
                width, height = ev.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif ev.type == pygame.USEREVENT:
                if ev.button.text == "EXIT":
                    running = False
                    pygame.time.wait(400)
                elif ev.button.text == "SETTINGS":
                    settings_app = SettingsApp(screen)
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
    pygame.quit()


if __name__ == '__main__':
    CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT = load_settings()
    main_window(CURR_FPS, CURR_VOLUME, WIDTH, HEIGHT)
