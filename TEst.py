import pygame
from os import path

WIDTH = 640
HEIGHT = 480
FPS = 60

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 247, 0)

pygame.init()  # inicjalizuje cała bibliotekę
pygame.mixer.init()  # inicjalizuje dzwięki

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")

# Grupy

all_sprites = pygame.sprite.Group()

# Dodawanie grafik
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_image_orig = pygame.transform.scale(player_img, (50, 38))
background = pygame.image.load(path.join(img_dir, "spacefield.png")).convert()
background_rect = background.get_rect()
rock_img = pygame.image.load(path.join(img_dir, "blocks.png")).convert()
rock_orig_img = pygame.transform.scale(rock_img, (410, 30))


# Dodawanie muzyki
pygame.mixer.music.load(path.join(snd_dir, "02 Quit Being Cute.mp3"))
pygame.mixer.music.set_volume(0.2)

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, obrot):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_orig_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        if obrot == True:
            pygame.sprite.Sprite.__init__(self)
            self.image = rot_center(rock_orig_img, 180)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rot_center(player_image_orig, 90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT /2
        self.speedx = 0


#Dodawanie do grup
player = Player()
all_sprites.add(player)

x = 1
for i in range(4):
     all_sprites.add(Rock(x*130, HEIGHT - 10, False))
     x += 1
     x += 1


x = 1
for i in range(4):
     all_sprites.add(Rock(x*130, HEIGHT - 465, True))
     x += 1
     x += 1


pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
