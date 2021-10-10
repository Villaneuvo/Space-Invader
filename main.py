import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Initialize Screen
# Need to add another tuple to make its work
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load(
    "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/background.png")

# Background Music
# mixer.music.load(
#     "C:/Users/muham/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/background.wav")
# mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(
    "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/ufo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load(
    "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/player.png")
# Player Coordinates
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(
        "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(30)

# Bullet
# ready -> bullet aren't fired yet/cant see the bullet
# fire -> bullet are fired/can see the bullet moving
bullet_img = pygame.image.load(
    "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 8
bullet_state = "ready"

# Font
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
end_font = pygame.font.Font('freesansbold.ttf', 64)


# Create Function

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    end_text = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(end_text, (200, 250))


def player(x, y):
    # Draw the player
    screen.blit(player_img, (x, y))  # blit == draw


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))  # d draw the enemy


def fire_bullet(x, y):
    global bullet_state  # set the bullet_state to global
    bullet_state = "fire"  # change the value of the bullet state
    # draw the bullet with the coordinates
    screen.blit(bullet_img, (x + 16, y + 10))


def is_Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))

    if distance < 27:
        return True
    else:
        return False


# Algorthym
# Set the game loop
# The game loop is important for game
# Because every asset in the game will be running infinitely
# By giving loop
running = True  # The game set true which means it will open until unkown time
while running:  # The loop of windows
    # Background color
    # RGB - Red , Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the close button is pressed
            running = False  # The Game Changed to false which means the windows will be closed

        # Keystroke checker if right or left arrow key is pressed
        if event.type == pygame.KEYDOWN:  # This Keydown/up func is when user finger still pressed the button it will
            # run this function but
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(
                        "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/laser.wav")
                    bullet_sound.play()
                    # Get the current x coordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # If the finger is released from the button the function of this code will be work
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking For the Boundaries to make it stay in the windows
    # Player Movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Collision Box
        collision = is_Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound(
                "C:/Users/Muhammad Daffa/Documents/Pemrograman/Python/Program/Pygame/Space Invaders/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
