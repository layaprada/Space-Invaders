import pygame
import random
import math
from pygame import mixer

#intializing to access everything in pygame
pygame.init()

#setting screen with size
screen = pygame.display.set_mode((800,600))

#background 
bcimg = pygame.image.load('background.png')

#background music

mixer.music.load('background.wav')
mixer.music.play(-1) #-1 loops the music

#title and image
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('royal-scots.png')
pygame.display.set_icon(icon)

#image on the screen
img = pygame.image.load('spaceship.png')
imgx = 370 #co-ordinates for the image
imgy = 480
img_change = 0

enemy_img = []
enemy_imgx = []
enemy_imgy =[]
enemyimgX_change = []
enemyimgY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('ufo.png'))
    enemy_imgx.append(random.randint(0,300))
    enemy_imgy.append(random.randint(50,150))
    enemyimgX_change.append(0.2)
    enemyimgY_change.append(30)

bullet_img = pygame.image.load('bullet.png')
bullet_imgx = 0
bullet_imgy = 480
bulletimgX_change = 0
bulletimgY_change = 0.8
bullet_state = "ready"


score_value= 0
font = pygame.font.Font('freesansbold.ttf',32)
text_X = 10
text_Y = 10

over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over(x,y):
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def display_score(x,y):
    score = font.render("Score : "+ str(score_value),True,(255,255,0))
    screen.blit(score,(x,y))

def drawimg(x,y):
    screen.blit(img,(x,y)) #the images are not just loaded but they are drawn as well

def drawimg_enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y)) #the images are not just loaded but they are drawn as well

def fireBullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x + 16,y + 10))

def isCollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt(math.pow((enemy_x-bullet_x),2) + math.pow((enemy_y - bullet_y),2))
    if distance < 27:
        return True
    else:
        return False



#game loop
run = True
while run:
    screen.fill((0,0,0)) #this needs to be on top so that all the other elements comes over the this
    #background
    screen.blit(bcimg,(0,0))
    #imgx += 0.1
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
        
        #keycontrols
        if events.type == pygame.KEYDOWN:
            
            if events.key == pygame.K_LEFT:
                img_change -= 0.3
            if events.key == pygame.K_RIGHT:
                img_change += 0.3
            if events.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav') #here we use sound instead of music its bcoz its a short audio
                    bullet_sound.play()
                    bullet_imgx  = imgx
                    fireBullet(bullet_imgx,bullet_imgy)

        if events.type == pygame.KEYUP:
             if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                img_change = 0
     
     
    imgx += img_change
#these conditions are to make sure that it does'nt crosses the boundry
    if imgx < 0:
        imgx = 0
    elif imgx > 736:#here we are taking it by substracting the pixels of the spaceshipt image
        imgx = 736

    

    for i in range(num_of_enemies):

        if enemy_imgy[i] > 440:
            for j in range(num_of_enemies):
                enemy_imgy[j] = 2000 #this is to make sure that all the enemies are out of the display screen
            game_over(200,250)
            break

        enemy_imgx[i] += enemyimgX_change[i]
        if enemy_imgx[i] < 0:
            enemyimgX_change[i] = 0.2
            enemy_imgy[i] += enemyimgY_change[i]
        elif enemy_imgx[i] >= 736 : 
            enemyimgX_change[i] = -0.2
            enemy_imgy[i] += enemyimgY_change[i]

        collision = isCollision(enemy_imgx[i],enemy_imgy[i],bullet_imgx,bullet_imgy)
        if collision:
            crash_sound = mixer.Sound('explosion.wav') #here we use sound instead of music its bcoz its a short audio
            crash_sound.play()
            bullet_imgy = 480
            bullet_state = "ready"
            score_value+=1
            
            # these below 2 lines are to relocate the enemy after collision
            enemy_imgx[i] = random.randint(0,300)
            enemy_imgy[i] = random.randint(50,150)

        drawimg_enemy(enemy_imgx[i],enemy_imgy[i],i)



    if bullet_imgy <= 0 :
            bullet_imgy = 480
            bullet_state = "ready"

    #movement of bullet
    if bullet_state is "fire":
        fireBullet(bullet_imgx,bullet_imgy)
        bullet_imgy -= bulletimgY_change
        

    

    

    
    display_score(text_X,text_Y)
    
    drawimg(imgx,imgy)    
    
    pygame.display.update() #this line is important to always update the display 

