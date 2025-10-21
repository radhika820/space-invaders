import pygame
import random
import math
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Make sure audio works

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paths
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
SOUNDS_PATH = os.path.join(ASSETS_PATH, "sounds")
IMAGES_PATH = os.path.join(ASSETS_PATH, "images")

# Load Sounds
laser_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "laser.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "explosion.wav"))
pygame.mixer.music.load(os.path.join(SOUNDS_PATH, "background.wav"))
pygame.mixer.music.play(-1)  # loop background music

# Player
player_img = pygame.image.load(os.path.join(IMAGES_PATH, "player.png"))
player_x = 370
player_y = 480
player_speed = 5

def player(x, y):
    screen.blit(player_img, (x, y))

# Bullet
bullet_img = pygame.image.load(os.path.join(IMAGES_PATH, "bullet.png"))
bullet_x = 0
bullet_y = 480
bullet_speed = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))
    laser_sound.play()

# Enemies
enemy_img = pygame.image.load(os.path.join(IMAGES_PATH, "enemy.png"))
num_of_enemies = 6
enemy_x = []
enemy_y = []
enemy_speed_x = []
enemy_speed_y = []

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_speed_x.append(3)
    enemy_speed_y.append(40)

def enemy(x, y, i):
    screen.blit(enemy_img, (x[i], y[i]))

# Score
score = 0
font = pygame.font.Font(None, 32)
game_over_font = pygame.font.Font(None, 64)

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 32))

# Collision detection
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    player_x = max(0, min(player_x, 736))

    # Bullet movement
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    # Enemy movement and collision
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_speed_x[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= 736:
            enemy_speed_x[i] *= -1
            enemy_y[i] += enemy_speed_y[i]

        # Game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # move enemies off screen
            game_over_text()
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
            break

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        # Draw enemy
        enemy(enemy_x, enemy_y, i)

    # Draw player and score
    player(player_x, player_y)
    show_score()

    pygame.display.update()

# Quit
pygame.quit()
sys.exit()
