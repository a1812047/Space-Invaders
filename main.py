import math
import random

import pygame
from pygame import mixer

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

WIDTH = 600
HEIGHT = 600

mixer.music.load("background.wav")
mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# background image
back_image = pygame.image.load("background_image.png")
back_image = pygame.transform.scale(back_image, (WIDTH, HEIGHT))

# score
score = 0
scorefont = pygame.font.SysFont("Arial", 24)

# icon
icon_image = pygame.image.load("spaceRocket.jpeg")
pygame.display.set_icon(icon_image)
pygame.display.set_caption("Save our Ship")

# saviour
saviour_image = pygame.image.load("space-ship.png")
saviour_image = pygame.transform.scale(saviour_image, (64, 64))
# player
playerX = 270
playerY = 535
player_change_in_X = 0
player_change_in_Y = 0  # for later we can increase this functionality for a player

# bullet
bullet_state = "ready"
bullet_image = pygame.image.load("bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (16, 16))
bulletX = 0
bulletY = 535
bullet_change_in_Y = -10
maximum_bullets_onScreen = 4

# Enemy or alien or ghosts list
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
total_enemies = 5
enemyImg.append(pygame.image.load("alien1.png"))
enemyImg.append(pygame.image.load("alien2.png"))
enemyImg.append(pygame.image.load("alien3.png"))
enemyImg.append(pygame.image.load("alien4.png"))
enemyImg.append(pygame.image.load("notAlien.png"))

speed = [-7, 7]
for i in range(total_enemies):
    enemyX.append(random.randint(0, 535))
    enemyY.append(random.randint(0, 300))
    enemyYchange.append(30)
    z = random.randint(0, 1)
    enemyXchange.append(speed[z])

# gameOver
over_font = pygame.font.SysFont("Arial", 72)


def showGameOver():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (150, 300))
    text = scorefont.render("SCORE: " + str(score), True, (255, 255, 0))
    screen.blit(text, (200, 380))


def showScore():
    text = scorefont.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))


def player(x, y):
    screen.blit(saviour_image, (x, y))


def create_enemies():
    for j in range(total_enemies):
        screen.blit(enemyImg[j], (enemyX[j], enemyY[j]))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 25, y+15))


def isCollision(alienX, alienY, bullX, bullY):
    distance = math.sqrt(math.pow((alienX - bullX), 2) + math.pow((alienY - bullY), 2))
    return distance < 33


run = True
while run:

    fpsClock.tick(FPS)
    screen.fill((0, 0, 0))
    screen.blit(back_image, (0, 0))
    showScore()
    create_enemies()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_in_X = -7
            elif event.key == pygame.K_RIGHT:
                player_change_in_X = 7

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("bullet-sound.mp3")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, 535)
        else:
            player_change_in_X = 0

    for k in range(total_enemies):

        if enemyY[k] >= 472:
            for y in range(total_enemies):
                enemyY[y] = 2000
            showGameOver()
            break

        enemyX[k] += enemyXchange[k]
        if enemyX[k] <= 0 or enemyX[k] >= 536:
            enemyXchange[k] *= -1
            enemyY[k] += enemyYchange[k]

        collision = isCollision(enemyX[k], enemyY[k], bulletX, bulletY)
        if collision:
            score += 1
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            destroying_image = pygame.image.load("boom.png")
            destroying_image = pygame.transform.scale(destroying_image, (80, 80))
            screen.blit(destroying_image, (enemyX[k], enemyY[k]))
            enemyX[k] = random.randint(0, 535)
            enemyY[k] = random.randint(0, 300)
            bullet_state = "ready"
            bulletY = 535

    playerX += player_change_in_X
    if playerX >= 535:
        playerX = 535
    elif playerX <= 0:
        playerX = 0

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 535
    if bullet_state == "fire":
        bulletY += bullet_change_in_Y
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)
    pygame.display.update()
pygame.quit()

