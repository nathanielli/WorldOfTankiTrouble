# imports
import sys
import pygame
import math
import os
import random


# tank player class
class tank(object):
    
    # tank initialization
    def __init__(self, disp, color, x, y, ang, health):
        self.disp = disp
        self.color = color
        self.speed = 0
        self.tempspeed = 0
        self.x = x
        self.y = y
        self.ang = ang
        self.angs = 0
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.health = health
        self.touchx = False
        self.touchy = False
        self.PUspeed = False
        self.PUspeedTime = 0
        
    # move the tank
    def moveTank(self):
        if self.PUspeed:
            self.tempspeed = self.speed * 1.5
            self.PUspeedTime = self.PUspeedTime + 1
        if self.PUspeed == False:
            self.tempspeed = self.speed
        # touching corner so fixate both x and y speeds
        if self.touchx and self.touchy:
            self.ang = self.ang + self.angs
            self.rect = pygame.Rect(self.x, self.y, 40, 40)
        # touching vertical wall so x is fixed
        if self.touchx and self.touchy == False:
            self.ang = self.ang + self.angs
            self.y = self.y + self.tempspeed * math.sin(self.ang)
            self.rect = pygame.Rect(self.x, self.y, 40, 40)
        # touching horizontal wall so y is fixed
        if self.touchx == False and self.touchy:
            self.ang = self.ang + self.angs
            self.x = self.x + self.tempspeed * math.cos(self.ang)
            self.rect = pygame.Rect(self.x, self.y, 40, 40)
        # it's free
        if self.touchx == False and self.touchy == False:
            self.ang = self.ang + self.angs
            self.x = self.x + self.tempspeed * math.cos(self.ang)
            self.y = self.y + self.tempspeed * math.sin(self.ang)
            self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.touchx = False
        self.touchy = False
        
    #check if tank touches wall
    def touchWall(self, w):
        # if it is touching the wall then move so it's not
        if pygame.Rect.colliderect(self.rect, w.rect):
            if w.w == 10:
                if w.x <= self.x:
                    self.x = self.x + 9
                if w.x > self.x:
                    self.x = self.x - 9
            if w.h == 10:
                if w.y < self.y:
                    self.y = self.y + 9
                if w.y >= self.y:
                    self.y = self.y - 9
        # see if it will touch wall if it keeps moving in direction
        ghostx = self.x + self.speed * math.cos(self.ang)
        ghosty = self.y + self.speed * math.sin(self.ang)
        ghostrect = pygame.Rect(ghostx, ghosty, 40, 40)
        # if it does then which wall is it touching and fixate in that direction
        if pygame.Rect.colliderect(ghostrect, w.rect):
            if w.w == 10:
                self.touchx = True
            if w.h == 10:
                self.touchy = True

    # draw the tank
    def drawTank(self, color, sb):
        self.color = color
        # keep angle between 0 and 2pi
        while self.ang > math.pi*2:
            self.ang = self.ang - math.pi*2
        while self.ang < 0:
            self.ang = self.ang + math.pi*2
        # draw box
        pygame.draw.rect(self.disp, self.color, self.rect)
        # turret
        pygame.draw.line(self.disp, self.color, (self.x+20, self.y+20), (self.x+20+40*math.cos(self.ang), self.y+20+40*math.sin(self.ang)), 8)
        pygame.draw.circle(self.disp, (0,0,0), (int(self.x)+20, int(self.y)+20), 15, 3)
        # if it has extra health then draw yellow "health" circle
        if self.health > 1:
            pygame.draw.circle(self.disp, (255,255,0), (int(self.x)+20, int(self.y)+20), 30, 3)
            sb.text(self.disp, str(self.health), self.x+20, self.y+10, (255,255,0), 16)
        # draw 3 lines behind tank to signify it has speed boost
        if self.PUspeed:
            dashx = self.x+20-30*math.cos(self.ang)
            dashy = self.y+20-30*math.sin(self.ang)
            pygame.draw.line(self.disp, self.color, (dashx, dashy), (dashx-9*math.cos(self.ang),dashy-9*math.sin(self.ang)), 3)
            pygame.draw.line(self.disp, self.color, (dashx+8*math.sin(self.ang), dashy+8*math.cos(self.ang)), (dashx-6*math.cos(self.ang)+8*math.sin(self.ang),dashy-6*math.sin(self.ang)+8*math.cos(self.ang)), 3)
            pygame.draw.line(self.disp, self.color, (dashx-8*math.sin(self.ang), dashy-8*math.cos(self.ang)), (dashx-6*math.cos(self.ang)-8*math.sin(self.ang),dashy-6*math.sin(self.ang)-8*math.cos(self.ang)), 3)
            
    # reset tank with givens
    def reset(self, x, y, ang, health):
        self.x = x
        self.y = y
        self.ang = ang
        self.health = health

# speed powerup class
class speed(object):

    # speed powerup initialization
    def __init__(self, disp, blue, x, y):
        self.disp = disp
        self.color = blue
        self.x = x
        self.y = y
        self.time = 0
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.used = False

    # detect if collide with tank
    def collideTank(self, t):
        if pygame.Rect.colliderect(self.rect, t.rect):
            self.used = True
            t.PUspeed = True
            t.PUspeedTime = 0

    # draw the powerup
    def drawSpeed(self):
        pygame.draw.rect(self.disp, self.color, self.rect)
        self.time = self.time + 1

# hp powerup class
class health(object):

    # hp powerup initialization
    def __init__(self, disp, yellow, x, y):
        self.disp = disp
        self.color = yellow
        self.x = x
        self.y = y
        self. time = 0
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.used = False

    # detect if collide with tank
    def collideTank(self, t):
        if pygame.Rect.colliderect(self.rect, t.rect):
            self.used = True
            t.health = t.health + 1

    # draw the powerup
    def drawHealth(self):
        pygame.draw.rect(self.disp, self.color, self.rect)
        self.time = self.time + 1

# tank bullet class
class bullet(object):
    
    # bullet initialization
    def __init__(self, disp, black, x, y, ang):
        self.disp = disp
        self.color = black
        self.x = x
        self.y = y
        self.ang = ang
        self.speedX = 10 * math.cos(self.ang)
        self.speedY = 10 * math.sin(self.ang)
        self.radius = 6
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)
        #self.rect = pygame.Rect(self.x, self.y, 8, 8)
        self.time = 0
        self.score = False
    
    # move the bullet
    def moveBullet(self):
        self.x = self.x + self.speedX
        self.y = self.y + self.speedY
        self.rect = pygame.Rect(self.x, self.y, 8, 8)
        self.time = self.time + 1
    
    # collision with tank?
    def collideTank(self, t, idB, idT, sb):
        if pygame.Rect.colliderect(self.rect, t.rect):
            # put bullet outside to despawn
            self.x = -10
            self.y = -10
            t.health = t.health - 1
            if t.health == 0:
                self.score = True
                #print('dead')
                # remove a point for shooting self
                if idB == idT:
                    if idB == 1:
                        sb.score1 = sb.score1 - 1
                    if idB == 2:
                        sb.score2 = sb.score2 - 1
                # add 2 points for hitting other
                if idB != idT:
                    if idB == 1:
                        sb.score1 = sb.score1 + 2
                    if idB == 2:
                        sb.score2 = sb.score2 + 2
        else:
            self.score = False

    # collision with wall?
    def collideWall(self, w):
        #print('wall?')
        if pygame.Rect.colliderect(self.rect, w.rect):
            if w.h == 10:
                self.speedY = -self.speedY
            if w.w == 10:
                self.speedX = -self.speedX

    # draw the bullet
    def drawBullet(self):
        pygame.draw.circle(self.disp, self.color, (int(self.x), int(self.y)), self.radius, 0)
        #print(self.time)
        #pygame.draw.rect(self.disp, self.color, self.rect)


# maze wall class
class wall(object):
    
    # wall initialization
    def __init__(self, disp, black, x, y, w, h):
        self.disp = disp
        self.color = black
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    
    # draw the wall
    def drawWall(self):
        pygame.draw.rect(self.disp, self.color, self.rect)


# score board class
class score(object):
    
    # score board initialization
    def __init__(self, disp, color1, color2):
        self.disp = disp
        self.score1 = 0
        self.score2 = 0
        self.color1 = color1
        self.color2 = color2
        self.name = pygame.font.match_font('arial')
    
    # draw text
    def text(self, disp, text, x, y, color, size):
        self.font = pygame.font.Font(self.name, size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        disp.blit(text_surface, text_rect)
        

# main thingy
def run():
    
    # some initializations
    pygame.init()
    cl = pygame.time.Clock()
    
    # some colors
    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    purple = (128, 0, 128)
    yellow = (255, 255, 0)
    
    # dimensions of screen
    width = 810
    height = 900

    # set up game screen
    disp = pygame.display.set_mode((width,height))
    pygame.display.set_caption('World of Tanki Trouble Game')

    # make score board
    sb = score(disp, blue, green)
    
    # new variables
    intro1 = True
    intro2 = True
    maze = True
    
    # wasd colors
    c11 = black
    c12 = black
    c13 = black
    c1c = black
    
    # wasd rect
    r11 = pygame.Rect(100, 250, 75, 75)
    r12 = pygame.Rect(200, 250, 75, 75)
    r13 = pygame.Rect(300, 250, 75, 75)
    rw = pygame.Rect(200, 150, 75, 75)
    
    # arrow colors
    c21 = black
    c22 = black
    c23 = black
    c2c = black
    
    # arrow rect
    r21 = pygame.Rect(100, 450, 75, 75)
    r22 = pygame.Rect(200, 450, 75, 75)
    r23 = pygame.Rect(300, 450, 75, 75)
    rup = pygame.Rect(200, 350, 75, 75)

    # number 1 (hard) and 0 (easy) for AI difficulty
    button1 = pygame.Rect(100, 600, 75, 75)
    button0 = pygame.Rect(100, 700, 75, 75)

    # number colors
    color1 = black
    color0 = black

    # maze rects
    bmazeClose = pygame.Rect(450, 700, 75, 75)
    bmazeFar = pygame.Rect(550, 700, 75, 75)
    bmazeNone = pygame.Rect(650, 700, 75, 75)

    # maze colors
    cmazeClose = black
    cmazeFar = black
    cmazeNone = black
    
    # loop for intro
    while (intro1 or intro2) or maze:
        for event in pygame.event.get():
            
            # exit game
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # if a key is pressed
            if event.type == pygame.KEYDOWN:
                
                # player two selection
                if event.key == pygame.K_LEFT:
                    c21 = red
                    c22 = black
                    c23 = black
                    c2c = black
                    color1 = black
                    color0 = black
                    intro1 = True
                if event.key == pygame.K_RIGHT:
                    c21 = black
                    c22 = black
                    c23 = red
                    c2c = black
                    color1 = black
                    color0 = black
                    intro1 = True
                if event.key == pygame.K_DOWN:
                    c21 = black
                    c22 = red
                    c23 = black
                    c2c = black
                    color1 = black
                    color0 = black
                    intro1 = True
                if event.key == pygame.K_UP:
                    c2c = red
                    if c21 == red or c22 == red or c23 == red:
                        intro1 = False

                # player one selection
                if event.key == pygame.K_a:
                    c11 = green
                    c12 = black
                    c13 = black
                    c1c = black
                    intro2 = True
                if event.key == pygame.K_s:
                    c11 = black
                    c12 = green
                    c13 = black
                    c1c = black
                    intro2 = True
                if event.key == pygame.K_d:
                    c11 = black
                    c12 = black
                    c13 = green
                    c1c = black
                    intro2 = True
                if event.key == pygame.K_w:
                    c1c = green
                    if c11 == green or c12 == green or c13 == green:
                        intro2 = False

                # AI selection
                if event.key == pygame.K_1:
                    color1 = blue
                    color0 = black
                    c21 = black
                    c22 = black
                    c23 = black
                    c2c = black
                    intro1 = False
                if event.key == pygame.K_0:
                    color1 = black
                    color0 = blue
                    c21 = black
                    c22 = black
                    c23 = black
                    c2c = black
                    intro1 = False

                # maze selection
                if event.key == pygame.K_7:
                    cmazeClose = yellow
                    cmazeFar = black
                    cmazeNone = black
                    maze = False
                if event.key == pygame.K_8:
                    cmazeClose = black
                    cmazeFar = yellow
                    cmazeNone = black
                    maze = False
                if event.key == pygame.K_9:
                    cmazeClose = black
                    cmazeFar = black
                    cmazeNone = yellow
                    maze = False

        #print(intro1)
        #print(intro2)

        # draw stuff and instructions     
        disp.fill(white)
        sb.text(disp, 'Select:', 140, 180, green, 30)
        sb.text(disp, 'Select:', 140, 380, red, 30)
        sb.text(disp, 'P1', 340, 180, green, 30)
        sb.text(disp, 'P2', 340, 380, red, 30)
        sb.text(disp, 'Players 1 and 2', 240, 30, black, 40)
        sb.text(disp, 'Select your tank', 240, 80, black, 40)
        sb.text(disp, 'Player 1 use WASD to move', 600, 250, green, 30)
        sb.text(disp, 'and Left Shift to shoot', 600, 300, green, 30)
        sb.text(disp, 'Player 2 use Arrow keys to', 600, 400, red, 30)
        sb.text(disp, 'move and "/" to shoot', 600, 450, red, 30)

        # print out classes of tanks
        sb.text(disp, 'Light Tank     Tank Destroyer     Heavy Tank', 590, 70, black, 25)
        pygame.draw.rect(disp, black, (390, 100, 400, 5))
        sb.text(disp, 'Less Health         Less Health         More Health', 590, 110, black, 20)
        sb.text(disp, '   Faster                Slower               Slower', 580, 130, black, 20)
        sb.text(disp, 'Less Bullets        More Bullets        Less Bullets', 590, 170, black, 20)

        # print AI and Maze selections
        sb.text(disp, 'Playing alone?', 270, 625, blue, 25)
        sb.text(disp, 'Aim-Bot or RNG Dummy?', 310, 670, blue, 25)
        sb.text(disp, '(both have buffed stats)', 300, 715, blue, 25)
        sb.text(disp, 'Choose a maze... a clustered one, a', 600, 600, black, 25)
        sb.text(disp, 'more free one, or none whatsoever', 600, 650, black, 25)
        sb.text(disp, 'Press 1 for Hard, 0 for Easy', 230, 800, blue, 25)
        sb.text(disp, 'Choose maze with 7, 8, 9 respectively', 590, 800, black, 25)
        
        # draw wasd
        pygame.draw.rect(disp, c11, r11, 5)
        sb.text(disp, 'Light', 140, 280, green, 20)
        pygame.draw.rect(disp, c12, r12, 5)        
        sb.text(disp, 'Tank', 240, 270, green, 20)
        sb.text(disp, 'Destroyer', 240, 290, green, 20)
        pygame.draw.rect(disp, c13, r13, 5)
        sb.text(disp, 'Heavy', 337, 280, green, 20)
        pygame.draw.rect(disp, c1c, rw, 5)
        sb.text(disp, 'Confirm', 237, 180, green, 20)
        
        # draw arrows
        pygame.draw.rect(disp, c21, r21, 5)
        sb.text(disp, 'Light', 140, 480, red, 20)
        pygame.draw.rect(disp, c22, r22, 5)
        sb.text(disp, 'Tank', 240, 470, red, 20)
        sb.text(disp, 'Destroyer', 240, 490, red, 20)
        pygame.draw.rect(disp, c23, r23, 5)
        sb.text(disp, 'Heavy', 337, 480, red, 20)
        pygame.draw.rect(disp, c2c, rup, 5)
        sb.text(disp, 'Confirm', 237, 380, red, 20)

        # draw numbers
        pygame.draw.rect(disp, color1, button1, 5)
        sb.text(disp, 'Hard AI', 140, 630, blue, 20)
        pygame.draw.rect(disp, color0, button0, 5)
        sb.text(disp, 'Easy AI', 140, 730, blue, 20)

        # draw maze thingies
        pygame.draw.rect(disp, cmazeClose, bmazeClose, 5)
        sb.text(disp, 'Tight', 490, 730, black, 20)
        pygame.draw.rect(disp, cmazeFar, bmazeFar, 5)
        sb.text(disp, 'Open', 590, 730, black, 20)
        pygame.draw.rect(disp, cmazeNone, bmazeNone, 5)
        sb.text(disp, 'None', 690, 730, black, 20)
        
        # update
        pygame.display.flip()
        cl.tick(30)


    # GAME TIME

    
    # p2 light stats
    if c11 == green:
        maxspeed2 = 6
        maxbullet2 = 2
        tankhp2 = 1
    # p2 td stats
    if c12 == green:
        maxspeed2 = 4
        maxbullet2 = 5
        tankhp2 = 1
    # p2 heavy stats
    if c13 == green:
        maxspeed2 = 4
        maxbullet2 = 2
        tankhp2 = 2
    # p1 light stats
    if c21 == red:
        maxspeed1 = 6
        maxbullet1 = 2
        tankhp1 = 1
    # p1 td stats
    if c22 == red:
        maxspeed1 = 4
        maxbullet1 = 5
        tankhp1 = 1
    # p1 heavy stats
    if c23 == red:
        maxspeed1 = 4
        maxbullet1 = 2
        tankhp1 = 2

    # AI hard stats
    if color1 == blue:
        maxspeed1 = 6
        maxbullet1 = 5
        tankhp1 = 2
    # AI easy stats
    if color0 == blue:
        maxspeed1 = 6
        maxbullet1 = 1
        tankhp1 = 2
    
    # make the 2 players
    t1 = tank(disp, blue, 730, 730, -math.pi/2, tankhp1)
    t2 = tank(disp, green, 30, 30, math.pi/2, tankhp2)
    
    # make the player bullets and wall arrays
    bullets1 = []
    bullets2 = []
    walls = []
    PUspeed = []
    PUhealth = []
    angles = []
    aimovetime = 0
    goalang = 3*math.pi/2

    # testing powerups
    """
    speed1 = speed(disp, blue, 440, 440)
    PUspeed.append(speed1)
    health1 = health(disp, yellow, 440, 440)
    PUhealth.append(health1)
    """
    
    # make four sides of maze walls
    wt = wall(disp, black, 0, 0, 810, 10)
    walls.append(wt)
    wm = wall(disp, black, 0, 800, 810, 10)
    walls.append(wm)
    wl = wall(disp, black, 0, 0, 10, 900)
    walls.append(wl)
    wr = wall(disp, black, 800, 0, 10, 900)
    walls.append(wr)
    wb = wall(disp, black, 0, 890, 810, 10)
    walls.append(wb)

    # maze walls far
    if cmazeFar == yellow:
        w1 = wall(disp, black, 200, 200, 200, 10)
        walls.append(w1)
        w2 = wall(disp, black, 600, 0, 10, 200)
        walls.append(w2)
        w3 = wall(disp, black, 200, 600, 400, 10)
        walls.append(w3)
        w4 = wall(disp, black, 0, 400, 200, 10)
        walls.append(w4)
        w5 = wall(disp, black, 400, 200, 10, 200)
        walls.append(w5)
        w6 = wall(disp, black, 600, 400, 200, 10)
        walls.append(w6)

    if cmazeClose == yellow:
        w1 = wall(disp, black, 100, 0, 10, 200)
        walls.append(w1)
        w2 = wall(disp, black, 0, 500, 200, 10)
        walls.append(w2)
        w3 = wall(disp, black, 100, 300, 200, 10)
        walls.append(w3)
        w4 = wall(disp, black, 200, 100, 10, 200)
        walls.append(w4)
        w5 = wall(disp, black, 200, 400, 10, 110)
        walls.append(w5)
        w6 = wall(disp, black, 100, 400, 100, 10)
        walls.append(w6)
        w7 = wall(disp, black, 200, 100, 500, 10)
        walls.append(w7)
        w8 = wall(disp, black, 100, 600, 400, 10)
        walls.append(w8)
        w9 = wall(disp, black, 300, 100, 10, 110)
        walls.append(w9)
        w10 = wall(disp, black, 300, 300, 10, 210)
        walls.append(w10)
        w11 = wall(disp, black, 400, 200, 10, 310)
        walls.append(w11)
        w12 = wall(disp, black, 100, 600, 10, 100)
        walls.append(w12)
        w13 = wall(disp, black, 100, 700, 200, 10)
        walls.append(w13)
        w14 = wall(disp, black, 400, 200, 200, 10)
        walls.append(w14)
        w15 = wall(disp, black, 600, 100, 10, 300)
        walls.append(w15)
        w16 = wall(disp, black, 500, 300, 110,10)
        walls.append(w16)
        w17 = wall(disp, black, 400, 700, 200, 10)
        walls.append(w17)
        w18 = wall(disp, black, 500, 400, 10, 210)
        walls.append(w18)
        w19 = wall(disp, black, 700, 600, 10, 200)
        walls.append(w19)
        w20 = wall(disp, black, 500, 500, 200, 10)
        walls.append(w20)
        w21 = wall(disp, black, 400, 600, 10, 100)
        walls.append(w21)
        w22 = wall(disp, black, 600, 600, 100, 10)
        walls.append(w22)
        w23 = wall(disp, black, 700, 200, 100, 10)
        walls.append(w23)
        w24 = wall(disp, black, 700, 200, 10, 100)
        walls.append(w24)
        w25 = wall(disp, black, 700, 400, 10, 110)
        walls.append(w25)
    
    # game
    while True:
        for event in pygame.event.get():
            
            # exit game
            if event.type == pygame.QUIT:
                pygame.quit()
        
            # if a key is pressed
            if event.type == pygame.KEYDOWN:

                # reset game
                if event.key == pygame.K_SPACE:
                    return
                
                # player two movement
                if event.key == pygame.K_LEFT:
                    #t1.ang = t1.ang - math.pi/12
                    t1.angs = -math.pi/24
                if event.key == pygame.K_RIGHT:
                    #t1.ang = t1.ang + math.pi/12
                    t1.angs = math.pi/24
                if event.key == pygame.K_UP:
                    t1.speed = maxspeed1
                if event.key == pygame.K_DOWN:
                    t1.speed = -1*maxspeed1
                
                # player two shooting
                if event.key == pygame.K_SLASH:
                    if len(bullets1) < maxbullet1:
                        new = bullet(disp, black, t1.x+20+40*math.cos(t1.ang), t1.y+20+40*math.sin(t1.ang), t1.ang)
                        bullets1.append(new)
            
                # player one movement
                if event.key == pygame.K_a:
                    t2.angs = -math.pi/24
                if event.key == pygame.K_d:
                    t2.angs = math.pi/24
                if event.key == pygame.K_w:
                    t2.speed = maxspeed2
                if event.key == pygame.K_s:
                    t2.speed = -1*maxspeed2
        
                # player one shooting
                if event.key == pygame.K_LSHIFT:
                    if len(bullets2) < maxbullet2:
                        new = bullet(disp, black, t2.x+20+40*math.cos(t2.ang), t2.y+20+40*math.sin(t2.ang), t2.ang)
                        bullets2.append(new)
            
            # if key released stop moving
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    t1.speed = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    t2.speed = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    t1.angs = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    t2.angs = 0

        # HARD AI WHEEEE
        if color1 == blue:
            # RANDOM POO AI STUFFS
            pathAng = 0
            pathDist = 0
            alsize = 0
            angles.clear()
            aimovetime = aimovetime + 1
            samefix = True

            # AI MOVING
            # FIRST CHECK SURROUNDING ANGLES AND SEE GOOD PATHS
            for i in range(24):
                testAng = (i/12)*math.pi
                for j in range(30):
                    testDist = j*8
                    testRect = pygame.Rect(t1.x+20+math.cos(testAng)*testDist, t1.y+20+math.sin(testAng)*testDist, 10, 10)
                    br1 = False
                    for w in walls:
                        if pygame.Rect.colliderect(testRect, w.rect):
                            br1 = True
                            break
                    if br1:
                        break
                    # IF GOOD PATH THEN ADD TO ARRAY
                    if testDist > 100:
                        pathDist = testDist
                        angles.append(testAng)
                        alsize = alsize + 1
                        #print(testAng)
                        #print(testDist)

            if aimovetime == 1:
                # CHOOSE DESTINED ANGLE FROM THE PATH
                randompath = random.randint(0,alsize-1)
                goalang = angles[randompath]
                # ADJUST ANGLE OF TURRET TO THAT DIRECTION
                if (t1.ang-goalang+math.pi)>0:
                    t1.angs = 1*math.pi/24
                    #print("pos")
                if (t1.ang-goalang+math.pi)<0:
                    t1.angs = -1*math.pi/24
                    #print("neg")
            
            # RESET AND CHOOSE NEW ANGLE
            elif aimovetime > 30:
                aimovetime = 0
            # IF AT ANGLE THEN MOVE
            if (int)(t1.ang*5) == (int)(goalang*5):
                t1.speed = 1*maxspeed1
                t1.angs = 0
            # IF NOT THEN KEEP MOVING UNTIL RANDOMLY STOPPED
            else:
                randomstop = random.randint(0,5)
                if randomstop == 0:
                    t1.speed = 0
            
            # AI SHOOTING
            # find distance/angle/position in relation to player one
            xDif = t1.x - t2.x
            yDif = t1.y - t2.y
            shootDist = math.sqrt(xDif*xDif+yDif*yDif)
            if t1.x > t2.x:
                shootAng = math.atan(yDif/xDif) - math.pi
            else:
                shootAng = math.atan(yDif/xDif)
                
            # !!!!! V I S U A L S !!!!!
            #"""
            testRect = pygame.Rect(t1.x+20+math.cos(goalang)*pathDist, t1.y+20+math.sin(goalang)*pathDist, 10, 10)
            pygame.draw.rect(disp, black, testRect)
            pygame.draw.line(disp, black, (t1.x+20, t1.y+20), (t1.x+20+math.cos(goalang)*pathDist+5, t1.y+20+math.sin(goalang)*pathDist+5), 2)
            pygame.draw.line(disp, red, (t1.x+20, t1.y+20), (t1.x+20+math.cos(shootAng)*300+5, t1.y+20+math.sin(shootAng)*300+5), 2)
            pygame.display.flip()
            #"""
            
            wontBounce = True
            # see if there's a wall in the way
            for j in range((int)(shootDist/9-1)):
                testDistShoot = j*9
                testRectShoot = pygame.Rect(t1.x+20+math.cos(shootAng)*testDistShoot, t1.y+20+math.sin(shootAng)*testDistShoot, 10, 10)
                br2 = False
                #pygame.draw.rect(disp, red, testRectShoot)
                #pygame.display.flip()
                for w in walls:
                    if pygame.Rect.colliderect(w.rect, testRectShoot):
                        #print("collide")
                        wontBounce = False
                        br2 = True
                        break
                    if br2:
                        break
            # if there's no wall in the way then AUTO-AIM AND SHOOT
            if wontBounce:
                t1.ang = shootAng
                if len(bullets1) < maxbullet1:
                    new = bullet(disp, black, t1.x+20+40*math.cos(t1.ang), t1.y+20+40*math.sin(t1.ang), t1.ang)
                    bullets1.append(new)
        # EASY "AI"
        if color0 == blue:
            # LITERALLY CHOOSE EVERYTHING RANDOMLY
            randomAI = random.randint(1,100)
            if randomAI == 1 or randomAI == 11:
                t1.speed = 0
            if randomAI == 2 or randomAI == 12:
                t1.speed = 1*maxspeed1
            if randomAI == 3 or randomAI == 13:
                t1.speed = -1*maxspeed1
            if randomAI == 4:
                if len(bullets1) < maxbullet1:
                            new = bullet(disp, black, t1.x+20+40*math.cos(t1.ang), t1.y+20+40*math.sin(t1.ang), t1.ang)
                            bullets1.append(new)
            if randomAI == 5 or randomAI == 15:
                t1.angs = 0
            if randomAI == 6 or randomAI == 16:
                t1.angs = math.pi/24
            if randomAI == 7 or randomAI == 17:
                t1.angs = -1*math.pi/24
        
        # generate powerups
        randnum = random.randint(1,1000)
        if randnum == 1 or randnum == 2:
            randx = random.randint(0,7)*100+40
            randy = random.randint(0,7)*100+40
            speed2 = speed(disp, blue, randx, randy)
            PUspeed.append(speed2)
        if randnum == 3:
            randx = random.randint(0,7)*100+40
            randy = random.randint(0,7)*100+40
            health2 = health(disp, yellow, randx, randy)
            PUhealth.append(health2)
        
        # remove the bullets when out of bounds
        for b in bullets1.copy():
            #print(b.time)
            if b.x <= 0 or b.x >= width or b.y >= height or b.y <= 0 or b.time > 300:
                bullets1.remove(b)
        for b in bullets2.copy():
            if b.x <= 0 or b.x >= width or b.y >= height or b.y <= 0 or b.time > 300:
                bullets2.remove(b)

        # remove powerups when used
        # speed
        for PUs in PUspeed:
            if PUs.used:
                PUspeed.remove(PUs)
        # health
        for PUhp in PUhealth:
            if PUhp.used:
                PUhealth.remove(PUhp)

        # remove powerups when decayed
        # speed
        for PUs in PUspeed:
            if PUs.time > 600:
                PUspeed.remove(PUs)
        # health
        for PUhp in PUhealth:
            if PUhp.time > 300:
                PUhealth.remove(PUhp)
        
        # remove powerup effects when timed out
        # speed
        if t1.PUspeed:
            if t1.PUspeedTime >= 300:
                t1.PUspeed = False
        if t2.PUspeed:
            if t2.PUspeedTime >= 300:
                t2.PUspeed = False

        # check if tank and wall touch
        for w in walls:
            t1.touchWall(w)
            t2.touchWall(w)

        # check if powerup picked up
        # speed
        for PUs in PUspeed:
            PUs.collideTank(t1)
            PUs.collideTank(t2)
        # health
        for PUhp in PUhealth:
            PUhp.collideTank(t1)
            PUhp.collideTank(t2)
        
        # move objects
        t1.moveTank()
        t2.moveTank()
        for b in bullets1:
            b.moveBullet()
        for b in bullets2:
            b.moveBullet()
        
        # draw objects
        disp.fill(white)
        # tanks
        t1.drawTank(red, sb)
        t2.drawTank(green, sb)
        # bullets
        for b in bullets1:
            b.drawBullet()
        for b in bullets2:
            b.drawBullet()
        for w in walls:
            w.drawWall()
        # speed powerups
        for PUs in PUspeed:
            PUs.drawSpeed()
        # health powerups
        for PUhp in PUhealth:
            PUhp.drawHealth()

        # update score
        sb.text(disp, 'Player 2 score: ' + str(sb.score1), 600, 815, red, 40)
        sb.text(disp, 'Player 1 score: ' + str(sb.score2), 200, 815, green, 40)
        sb.text(disp, 'P1: WASD to move, Left Shift to shoot; P2: Arrow Keys to move, "/" to shoot', 400, 860, black, 25)
        
        # check bullet collisions for p2
        for b in bullets1:
            b.collideTank(t1, 1, 1, sb)
            # if score then increment score
            if b.score:
                # make black
                t1.drawTank(black, sb)
                pygame.display.flip()
                pygame.time.delay(1000)
                # then reset
                t1.reset(730, 730, -math.pi/2, tankhp1)
                t2.reset(30, 30, math.pi/2, tankhp2)
                bullets1.clear()
                bullets2.clear()
                PUspeed.clear()
                PUhealth.clear()
                t1.PUspeed = False
                t2.PUspeed = False
            b.collideTank(t2, 1, 2, sb)
            # if score then increment score
            if b.score:
                # make black
                t2.drawTank(black, sb)
                pygame.display.flip()
                pygame.time.delay(1000)
                # then reset
                t1.reset(730, 730, -math.pi/2, tankhp1)
                t2.reset(30, 30, math.pi/2, tankhp2)
                bullets1.clear()
                bullets2.clear()
                PUspeed.clear()
                PUhealth.clear()
                t1.PUspeed = False
                t2.PUspeed = False
            for w in walls:
                b.collideWall(w)
                
        # check bullet collisions for p1
        for b in bullets2:
            b.collideTank(t1, 2, 1, sb)
            # if score then increment score
            if b.score:
                # make black
                t1.drawTank(black, sb)
                pygame.display.flip()
                pygame.time.delay(1000)
                # then reset
                t1.reset(730, 730, -math.pi/2, tankhp1)
                t2.reset(30, 30, math.pi/2, tankhp2)
                bullets1.clear()
                bullets2.clear()
                PUspeed.clear()
                PUhealth.clear()
                t1.PUspeed = False
                t2.PUspeed = False
            b.collideTank(t2, 2, 2, sb)
            # if score then increment score
            if b.score:
                # make black
                t2.drawTank(black, sb)
                pygame.display.flip()
                pygame.time.delay(1000)
                # then reset
                t1.reset(730, 730, -math.pi/2, tankhp1)
                t2.reset(30, 30, math.pi/2, tankhp2)
                bullets1.clear()
                bullets2.clear()
                PUspeed.clear()
                PUhealth.clear()
                t1.PUspeed = False
                t2.PUspeed = False
            for w in walls:
                b.collideWall(w)
         
        # update game screen
        pygame.display.flip()
        cl.tick(30)
        
# run stuff
while True:
    run()

# exit
quit()
