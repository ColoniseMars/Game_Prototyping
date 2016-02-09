import math
import pygame
import globalvars

class planet:
    """This class creates planets. Args:Gravity, posx, posy, velocityX, velocityY, color, size"""
    def __init__(self, gravity, positionX, positionY, velocityX, velocityY, color = (255,255,255), size = 2):
        self.gravity = gravity  #in pixels/tick^2
        self.positionX = positionX
        self.positionY = positionY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.color = color
        self.size = size
        self.stationairy = False
        self.lastposX = 0
        self.lastposY = 0


    def calculatevelchange(self, otherbody):
        xdifference = otherbody.positionX - self.positionX
        ydifference = otherbody.positionY - self.positionY
        if xdifference == 0:
            if ydifference == 0:
                return False
            if ydifference<0:
                self.velocityY-= otherbody.gravity
            if ydifference>0:
                self.velocityY+= otherbody.gravity
        elif ydifference == 0:
            if xdifference == 0:
                return False
            if xdifference<0:
                self.velocityX-= otherbody.gravity
            if xdifference>0:
                self.velocityX+= otherbody.gravity
        else:   #Math is broken as fuck. Task: Learn how to calculate with radians
            angle = math.atan(ydifference/xdifference)
            changeY = (math.sin(angle))*otherbody.gravity
            changeX = (math.cos(angle))*otherbody.gravity


            if xdifference<0:
                self.velocityX -= changeX
            else:
                self.velocityX += changeX
            if ydifference<0:
                self.velocityY -= changeY
            else:
                self.velocityY += changeY

            #print(angle)
        print(str(math.sqrt(self.velocityX*self.velocityX+self.velocityY*self.velocityY)))

    def move(self):
        self.lastposX = self.positionX
        self.lastposY = self.positionY
        self.positionX += self.velocityX
        self.positionY += self.velocityY

    def draw(self, currentanimation, animationfactor):
        pygame.draw.circle(globalvars.GameScreen, self.color, (int(self.lastposX + ((self.positionX-self.lastposX)/animationfactor)*currentanimation), int(self.lastposY + ((self.positionY-self.lastposY)/animationfactor)*currentanimation)), 2)
        #pygame.draw.rect(globalvars.GameScreen, self.color, (self.lastposX + ((self.positionX-self.lastposX)/animationfactor)*currentanimation, self.lastposY + ((self.positionY-self.lastposY)/animationfactor)*currentanimation, 5, 5))