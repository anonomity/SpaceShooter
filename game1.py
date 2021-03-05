import pygame
import random

ship = Actor('spaceship', (500,600))
rocket_fire = Actor('rocket', (ship.x,ship.y))
bomb = Actor('start',(random.randint(10,900),10))
alien = Actor('zombie', center=(100,150))
heart1 = Actor('heart', center=(850,40))
heart2 = Actor('heart', center=(890,40))
heart3 = Actor('heart', center=(930,40))
poke = Actor('poke', center=(random.randint(10,900),-10))


WIDTH = 1000
HEIGHT = 700
hearts = [heart1, heart2, heart3]
heart = 3
score = 0
gameOver = False
restart = False
timer = 1000
level = 1
win = False

def draw():
    global score
    screen.clear()
    global gameOver
    global timer

    if(gameOver == True):
        screen.clear()
        screen.fill((0,0,0))
        screen.blit('over', (-200,0))
    if((gameOver is False) and (win is True)):
        screen.clear()
        screen.fill((0,0,0))
        screen.draw.text("Press Space to go to next level", (250,10), color="white",fontname="sharetechmono-regular", fontsize=40, lineheight=1.5)
    elif((gameOver is False) and (level is 1)):
        screen.blit('space', (0,200))
        ship.draw()
        rocket_fire.draw()
        alien.draw()
        bomb.draw()
        hearts[0].draw()
        hearts[1].draw()
        hearts[2].draw()
        poke.draw()
        screen.draw.text("score: "+str(score), (100, 10), color="white", fontsize=40)
        screen.draw.text("Timer "+str(timer), (100, 40), color="white", fontsize=40)
        screen.draw.text("Zombie Boom Boom Level 1", (250,10), color="white",fontname="sharetechmono-regular", fontsize=40, lineheight=1.5)
    elif((gameOver is False) and (level is 2)):
        alien.draw()
        bomb.draw()
        screen.blit('space', (0,200))
        screen.draw.text("Zombie Boom Boom Level 2", (250,10), color="white",fontname="sharetechmono-regular", fontsize=40, lineheight=1.5)
        rocket_fire.draw()
        ship.draw()
        hearts[0].draw()
        hearts[1].draw()
        hearts[2].draw()



####################################################### ALIEN / STAR FUNCTIONS  #######################################################################################

def move_alien(alien):
    global heart
    if(heart < 3):
        poke.y += 10

    if(poke.y > HEIGHT):
        poke.y =0
        poke.x = random.randint(10,900)
    pokehit = poke.colliderect(ship)
    if(pokehit == True):
        clock.schedule_unique(add_heart,0.2)
    alien.right += 1
    if alien.left > WIDTH:
        alien.right = 0


    if bomb.y > HEIGHT:
        bomb.y = 10
        bomb.x = random.randint(10,900)
    bomb.y +=4
    collide = rocket_fire.colliderect(alien)


    hit = bomb.colliderect(ship)

    hit_bomb = rocket_fire.colliderect(bomb)
    if collide == True:
        set_alien_hurt()
    if hit == True:
        ship.image = 'boom'
        rocket_fire.image = 'boom'
        clock.schedule_unique(drop_heart,0.2)
        clock.schedule_unique(set_ship_normal, 1.0)
    if(hit_bomb == True):
        bomb.y = 10
        bomb.x = random.randint(10,900)


def set_alien_hurt():

    clock.schedule_unique(add_hit, 0.2)
    alien.image = 'boom'
    sounds.ouch.play()
    clock.schedule_unique(set_alien_normal, 1.0)


def set_alien_normal():
    alien.image = 'zombie'


####################################################### ROCKET FUNCTIONS  #######################################################################################


def move_rocket(ship):

    offset = 0
    if keyboard.lshift:
       offset = 15


    if keyboard.left:
        ship.x -= 10 + offset
        rocket_fire.x -=10 + offset

    elif keyboard.right:
        ship.x += 10 + offset
        rocket_fire.x +=10 + offset
    elif ((keyboard.space) & (rocket_fire.y == ship.y)):
        animate(rocket_fire, pos =(ship.x, 0))
        sounds.shoot.play()
        clock.schedule_unique(reset_rocket, 1)
        screen.clear()
    if ship.x > WIDTH:
        ship.x = 0
        rocket_fire.x = 0

    if ship.x < 0 :
        ship.x = WIDTH
        rocket_fire.x = WIDTH

def set_ship_normal():
        ship.image = 'spaceship'
        rocket_fire.image = 'rocket'

def reset_rocket():
        rocket_fire.x = ship.x
        rocket_fire.y = ship.y


####################################################### HEART FUNCTIONS  #######################################################################################


def drop_heart():

    global heart
    global hearts
    global gameOver

    heart -=1

    if(heart ==2):
        hearts[2].x = WIDTH+100
    elif(heart ==1):
        hearts[1].x = WIDTH+100
    elif(heart ==0):
        hearts[0].x = WIDTH+100
        gameOver = True
        sounds.gameover.play()

def add_heart():
    global heart
    global hearts
    heart +=1
    if(heart ==3):
        hearts[2].x = 930
        poke.y = -10
    elif(heart == 2):
        hearts[1].x = 890
        poke.y = -10



#############################################################################

def add_hit():
    global score
    score += 1


def restart():
    global heart
    global hearts
    global gameOver
    global score
    score = 0
    global win
    win = False
    gameOver = False
    hearts[0].x = 850
    hearts[1].x = 890
    hearts[2].x = 930
    heart = 3

def update():
    global timer
    global gameOver
    global score
    global level
    global win

    if(score == 3):
        win = True
    if((win == True) and (keyboard.space)):
        level =2
        restart()

    if(gameOver is False):
        move_alien(alien)
        move_rocket(ship)
        timer -=1
    draw()

    if(timer < 0):
            gameOver = True
    if((keyboard.r) & (gameOver == True)):
           restart()