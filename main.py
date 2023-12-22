import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as e:
        print('Cannont open image', e)
        raise SystemExit(e)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
FPS = 50
tile_images = {'wall': load_image('box.png', colorkey=-1), 'empty': load_image('grass.png', colorkey=-1)}
player_image = load_image('mar.png', colorkey=-1)
tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "images/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '@'):
            y -= 1
    elif movement == 'down':
        if y < max_y - 1 and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '@'):
            y += 1
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@'):
            x -= 1
    elif movement == 'right':
        if x < max_x - 1 and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@'):
            x += 1
    hero.move(x, y)


start_screen()
level_map = load_level('map.txt')
hero, max_x, max_y = generate_level(level_map)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, 'up')
            elif event.key == pygame.K_DOWN:
                move(hero, 'down')
            elif event.key == pygame.K_LEFT:
                move(hero, 'left')
            elif event.key == pygame.K_RIGHT:
                move(hero, 'right')
    screen.fill('black')
    sprite_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()