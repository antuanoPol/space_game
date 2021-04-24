import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "Bajki_robotow_projekt_grafika")
snd_dir = path.join(path.dirname(__file__), "Bajki_robotow_projekt_muzyka")
WIDTH = 1900
HEIGHT = 1000
FPS = 60

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'

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
pygame.display.set_caption("Bajki robotow")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")

# Dodawanie grafik
player_img = pygame.image.load(path.join(img_dir, "guardbot3.png")).convert()
player_orig_img = player_img = pygame.transform.scale(player_img, (120, 120))
background = pygame.image.load(path.join(img_dir, "hexagonal_background_1080p.png")).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed05.png")).convert()


# Dodawanie muzyki
pygame.mixer.music.load(path.join(snd_dir, "CleytonRX - Battle RPG Theme Var.ogg"))
pygame.mixer.music.set_volume(0.4)
# shoot_sound =

def rotate(rot, image):
    new_image = pygame.transform.rotate(image, rot)
    return new_image


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = parent.rect.centery
        self.rect.centerx = parent.rect.centerx
        self.speed = 10
        self.direction = parent.direction
        if self.direction == LEFT or self.direction == RIGHT:
            self.image = rotate(90, self.image)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = parent.rect.centery
            self.rect.centerx = parent.rect.centerx
        if self.direction == UP:
            self.rect.bottom = parent.rect.top
        if self.direction == DOWN:
            self.rect.bottom = parent.rect.bottom
        if self.direction == RIGHT:
            self.rect.right = parent.rect.right
        if self.direction == LEFT:
            self.rect.left = parent.rect.left

    def update(self):
        if self.direction == LEFT:
            self.rect.x -= self.speed
        if self.direction == UP:
            self.rect.y -= self.speed
        if self.direction == DOWN:
            self.rect.y += self.speed
        if self.direction == RIGHT:
            self.rect.x += self.speed

        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, player_klawisze, respawn):
        self.player_klawisze1 = player_klawisze
        pygame.sprite.Sprite.__init__(self)
        self.image = player_orig_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if respawn == True:
            self.rect.centerx = WIDTH
            self.rect.bottom = HEIGHT
        else:
            self.rect.centerx = 0
            self.rect.bottom = 0
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 350
        self.direction = UP

    def update(self):
        self.speedx = 0
        self.speedy = 0
        if self.player_klawisze1:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
                self.direction = LEFT
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
                self.direction = RIGHT
            if keystate[pygame.K_UP]:
                self.speedy = -8
                self.direction = UP
            if keystate[pygame.K_DOWN]:
                self.speedy = 8
                self.direction = DOWN
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.right > WIDTH + 55:
                self.rect.right = WIDTH + 55
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > 1000:
                self.rect.bottom = 1000
            if self.rect.top <= 0:
                self.rect.top = 0
        else:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_a]:
                self.speedx = -8
                self.direction = LEFT
            if keystate[pygame.K_d]:
                self.speedx = 8
                self.direction = RIGHT
            if keystate[pygame.K_w]:
                self.speedy = -8
                self.direction = UP
            if keystate[pygame.K_s]:
                self.speedy = 8
                self.direction = DOWN
            if keystate[pygame.K_LSHIFT]:
                self.shoot()
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.right > WIDTH + 55:
                self.rect.right = WIDTH + 55
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > 1000:
                self.rect.bottom = 1000
            if self.rect.top <= 0:
                self.rect.top = 0


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            bullet = Bullet(self)
            all_sprites.add(bullet)
            bullets.add(bullet)
            # shoot_sound.play()
            self.last_shoot = now




pygame.mixer.music.play(loops=-1)

# Tworzymy grupy, sprite
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(True, True)
player1 = Player(False, False)
all_sprites.add(player)
all_sprites.add(player1)

running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()