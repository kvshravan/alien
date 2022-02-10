import pygame,sys
import random

# init pygame
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

size = (800,600)

# create screen
screen = pygame.display.set_mode(size)

# background
BLACK = (0,40,60)
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1)

#tile and logo
pygame.display.set_caption("Alien invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)


#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x,y))

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 5
for i in range(num_enemies):    
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(25, 100))
    enemyX_change.append(1.5)
    enemyY_change.append(70)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))


# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 7
bulletState = "ready"

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x+16,y+10))

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)
textX = textY = 5

def show_score(x,y):
    local_score = font.render("Score : "+ str(score),True, (255,255,255))
    screen.blit(local_score, (x,y))
# Game over
gameover_f = pygame.font.Font('freesansbold.ttf', 64)
def gameOver():
    local_score = gameover_f.render("Game Over :(",True,(255,255,255))
    screen.blit(local_score, (200,100))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    if (enemyX > bulletX and enemyX < bulletX+32) or (bulletX > enemyX and bulletX < enemyX+64):
        if (enemyY > bulletY and enemyY < bulletY+32) or (bulletY > enemyY and bulletY < enemyY+64):
            return True
    return False


# spacebg
spaceImg = pygame.image.load('universe.png')
spaceX = 250
spaceY = 250
def space(x,y):
    screen.blit(spaceImg, (x,y))

# game loop
running = True
while running:

    # fill screen with black
    screen.fill(BLACK)
    space(spaceX,spaceY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = pygame.mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):
        # Game Over
        if enemyY[i] > 420:
            for j in range(num_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i]<= 0:
            enemyX[i] = 0
            enemyX_change[i] = 1.5
            enemyY[i]  += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Collison
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            monsterSound = pygame.mixer.Sound('monster.wav')
            monsterSound.play()
            bulletY = 500
            bulletState = "ready"
            score +=1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(25, 100)
        enemy(enemyX[i],enemyY[i],i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 500
        bulletState = "ready"

    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX,textY)

    pygame.display.update()
