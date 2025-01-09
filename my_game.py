import pygame
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")

FPS = 60
clock = pygame.time.Clock()

BG_COLOR = (135, 206, 235)

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (255, 0, 0)
PLAYER_SPEED = 5
JUMP_STRENGTH = 15
GRAVITY = 0.5

PLATFORM_COLOR = (0, 255, 0)
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
ENEMY_COLOR = (0, 0, 255)
ENEMY_SPEED = 2

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.lives = 3

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_STRENGTH

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        if self.rect.y + self.rect.height >= HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.vel_y = 0
            self.on_ground = True

    def update(self, platforms):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.apply_gravity(platforms)

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)

    def lose_life(self):
        self.lives -= 1
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - PLAYER_HEIGHT

    def is_alive(self):
        return self.lives > 0

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, PLATFORM_COLOR, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.vel_x = ENEMY_SPEED

    def update(self):
        self.rect.x += self.vel_x

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel_x = -self.vel_x

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)

player = Player(WIDTH // 2, HEIGHT - PLAYER_HEIGHT)
platforms = [
    Platform(200, 500),
    Platform(400, 400),
    Platform(600, 300),
    Platform(300, 200),
    Platform(100, 100),
]

enemies = [
    Enemy(100, HEIGHT - PLAYER_HEIGHT - 50),
    Enemy(500, HEIGHT - PLAYER_HEIGHT - 150),
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player.handle_input()
    player.update(platforms)

    if player.rect.top <= 0:
        print("Вітаємо! Ви перемогли")
        running = False

    for enemy in enemies:
        enemy.update()
        if player.rect.colliderect(enemy.rect):
            player.lose_life()
            if not player.is_alive():
                print("Гра закінчена")
                running = False

    screen.fill(BG_COLOR)
    player.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
