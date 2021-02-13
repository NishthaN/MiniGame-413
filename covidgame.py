import random

import pygame
from pygame.locals import *
import os
import sys
import math

pygame.init()

W, H = 900, 500
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Save Yourself from Corona!')

bg = pygame.image.load(os.path.join('images','rsz_bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,23)]
    jump = [pygame.image.load(os.path.join('images/jump', str(x) + '.png')) for x in range(1,47)]
    slide = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(23,45)]
    fall = pygame.image.load(os.path.join('images','45.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling=False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, self.x, self.y+30)
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: # NEW
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35) # NEW
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) # NE
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
        

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13) # NEW

class virus1(object):
    virus = [pygame.image.load(os.path.join('images/Virus', str(x) + '.png')) for x in range(0,12
                                                                                             )]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)  # Defines the accurate hitbox for our character
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:  # This is what will allow us to animate the saw
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.virus[self.rotateCount//2], (64,64)), (self.x,self.y))  # scales our image down to 64x64 before drawing
        self.rotateCount += 1
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
class virus2(virus1):  # We are inheriting from virus 1
    img = [pygame.image.load(os.path.join('images/Virus', str(x) + '.png')) for x in range(12,24
                                                                                             )]
    def draw(self,win):
        self.hitbox = (
        self.x + 10, self.y + 5, self.width - 20, self.height - 5)  # Defines the accurate hitbox for our character
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        if self.rotateCount >= 8:  # This is what will allow us to animate the saw
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.img[self.rotateCount // 2], (64, 64)),
                 (self.x, self.y))  # scales our image down to 64x64 before drawing
        self.rotateCount += 1
        def collide(self, rect):
            if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
                if rect[1] < self.hitbox[1]:
                    return True

run = True
speed = 30  # NEW
pygame.time.set_timer(USEREVENT+1, 500)
runner = player(40, 200, 64, 64)
pygame.time.set_timer(USEREVENT+4, random.randrange(3000, 7500))
obstacles = []

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30) # Font object
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255)) 
    runner.draw(win)
    # Loops through all obstacles
    for obstacle in obstacles:
        obstacle.draw(win)
    win.blit(text, (700, 10))
    pygame.display.update()

def updateFile():
    f = open('scores.txt','r') # opens the file in read mode
    file = f.readlines() # reads all the lines in as a list
    last = int(file[0]) # gets the first line of the file

    if last < int(score): # sees if the current score is greater than the previous best
        f.close() # closes/saves the file
        file = open('scores.txt', 'w') # reopens it in write mode
        file.write(str(score)) # writes the best score
        file.close() # closes/saves the file

        return score
               
    return last

def endScreen():
    global pause, score, speed, obstacles
    # We need to reset our variables
    pause = 0
    speed = 30
    obstacles = []
                 
    # another game loop  
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # if the user hits the mouse button
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False
        
        # This will draw text displaying the score to the screen.      
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80) # creates a font object
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255)) # We will create the function updateFile later
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0
    runner.falling=False

fallSpeed = 0
pause = 0
       
while run:
    score = speed//5 - 6
    if pause>0:
        pause+=1
        if pause>fallspeed*2:
            endscreen()
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  # If user hits space or up arrow key
        if not (runner.jumping):  # If we are not already jumping
            runner.jumping = True

    if keys[pygame.K_DOWN]:  # If user hits down arrow key
        if not (runner.sliding):  # If we are not already sliding

            runner.sliding = True
    for obstacle in obstacles:
        
        if obstacle.collide(runner.hitbox):
            runner.falling = True
            
            if pause==0:
                fallspeed==speed
                pause = 1
                
        obstacle.x -= 1.4
        if obstacle.x < obstacle.width * -1:  # If our obstacle is off the screen we will remove it
            obstacles.pop(obstacles.index(obstacle))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == USEREVENT + 1:  # Checks if timer goes off
            speed += 1  # Increases speed

        if event.type == USEREVENT + 4:
            r = random.randrange(0, 2)
            if r == 0:
                obstacles.append(virus1(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(virus2(810, 200, 64, 64))
    clock.tick(speed)
    redrawWindow()
