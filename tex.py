from objects import Entity
from functions import load_image
import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Ракета')
    size0 = w, h = 450, 450
    surface = pygame.display.set_mode(size0)
    running = True
    all_sprites = pygame.sprite.Group()

    crab = Entity(load_image("crab_idle.png"), 4, 1, 10, 10, 420, 400)
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        surface.fill('black')
        crab.draw(surface)
        crab.update()
        pygame.display.flip()
        clock.tick(4)
    pygame.quit()

