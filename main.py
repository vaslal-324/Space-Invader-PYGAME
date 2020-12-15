import pygame
import random
import math

# after loading , blit the image

# initialise pygame
pygame.init()  # important

# create screen
screen = pygame.display.set_mode((800, 600))  # anything inside the box except the caption and icon should be
# done with screen.

# Title/Caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('project.png')  # IMAGE RESIZING CAN BE DONE IN PYGAME
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.jpg')
pygame.mixer.music.load('background.wav')  # from pygame import mixer and then use mixer. instead of pygame.mixer.
pygame.mixer.music.play(-1)

# Player
playerimg = pygame.image.load('space-ship.png')
playerX = 370  # almost half of 800
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numb_of_enemies = 6

# enemyimg = pygame.transform.scale(enemyimg, (32,32))

for i in range(numb_of_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)  # by default when not hitting the boundaries
    enemyY_change.append(40)  # need not use append for enemyX and enemyY

# Bullet
# Ready - bullet is not seen
# Fire - bullet is seen
bulletimg = pygame.image.load('Freshbullet.png')
bulletX = 0  # depends on the player
bulletY = 480  # same as that of player..reset condition
bulletX_change = 0
bulletY_change = 2
bullet_state = "Ready"

# Scoring
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # creating a font object.. other fonts should be downloaded
# from website : dafonts.com

textX = 10
textY = 10

# GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 70)

def game_over_text():
    Over_font = over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(Over_font, (200, 250))


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (0, 255, 255))  # first you have to render
    screen.blit(score, (x, y))  # and then blit


def player(x, y):
    screen.blit(playerimg, (x, y))  # screen is an identifier which we have used here


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))  # for printing in the centre of the spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyY - bulletY, 2) + math.pow(enemyX - bulletX, 2))
    if distance <= 27:
        return True
    return False


# Game loop
running = True
while running:  # closes only by pressing the red cross mark
    # RGB - Red, Green , Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # key pressed
            if event.key == pygame.K_LEFT:  # check if the pressed key is left or right arrow key
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    # storing the x coorinate of the player
                    bullet_sound = pygame.mixer.Sound('laser.wav')  # Sound is for a short time not like music
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)  # firing bullet when key is pressed down does not update position

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # left or right is released
                playerX_change = 0

    playerX += playerX_change  # updating the player coordinate change
    # after updating the player_X check if the new position is within the boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:  # the size of spaceship is 64 pixels ..thus 800 - 64 = 736
        playerX = 736

    # movement of many enemies
    for i in range(numb_of_enemies):
        if enemyY[i] > 440:
            for j in range(numb_of_enemies):
                enemyY[j] = 2000  # collecting all the enemies and moving out of screen
                #enemy(enemyX[j], enemyY[j], j)
            game_over_text()
            break
    for i in range(numb_of_enemies):
        enemyX[i] += enemyX_change[i]  # updating the enemy coordinate change
        # after updating the check if the enemy is within the boundaries
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]  # y coordinate changed only when the enemy hits left or right..here by 40px
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound('explosion.wav')  # Sound is for a short time not like music
            explosion_sound.play()
            bulletY = 480  # reset condition
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)  # call for blit function / drawing

    # bullet movement
    if bulletY <= 0:  # when the bullet crosses the 0 only then the other bullet is shot
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state is "Fire":  # after the state is changed to fire the function is called with updations
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change  # updations/propogations

    # bullet(bulletX,bulletY)  the bullet is displayed only when blit is called which is inside thus function
    player(playerX, playerY)  # finally calling the player and the enemy function
    show_score(textX, textY)

    pygame.display.update()  # important - pasting the changes onto the screen
