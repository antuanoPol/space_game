import pygame
from os import path
import random

WIDTH = 640
HEIGHT = 480
FPS = 60

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 247, 0)
# iniclaizacja gry i utworzenie okna
pygame.init()  # inicjalizuje cała bibliotekę
pygame.mixer.init()  # inicjalizuje dzwięki

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")

# Dodawanie grafik
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "skeleton-01_fly_11.png")).convert()
background = pygame.image.load(path.join(img_dir, "spacefield.png")).convert()
background_rect = background.get_rect()
background = pygame.image.load(path.join(img_dir, "tilesetOpenGameBackground.png")).convert()
background_good = pygame.transform.scale(background, (WIDTH, HEIGHT))

#Dodawanie muzyki
pygame.mixer.music.load(path.join(snd_dir, "floppy-disks.mp3"))

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10


    def update(self):
        self.speedy = 0
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = - 8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        if self.rect.left < -20:
            self.rect.left = -20
        if self.rect.right > 650:
            self.rect.right = 650



class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y ):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey = BLACK
        self.rect = self.image.get_rect()
        self.speedy = -10
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        last_update = pygame.time.get_ticks()
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()


    # Update
    all_sprites.update()

    screen.fill(BLACK)
    screen.blit(background_good, background_rect)
    all_sprites.draw(screen)
    # draw_text(screen, str("My game"), 18, WIDTH / 2, 10)
    pygame.display.flip()

pygame.quit()
