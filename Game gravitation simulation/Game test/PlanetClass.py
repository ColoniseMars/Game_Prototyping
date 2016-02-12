import math
import pygame
import globalvars

global file
file = open("filenewmethode", mode = "w")
global x
x=0

class planet:
    """This class creates planets. Args:Gravity, posx, posy, velocityX, velocityY, color, size"""
    def __init__(self, gravity, positionX, positionY, velocityX, velocityY, color = (255,255,255), size = 2, notsubject = False):
        self.gravity = gravity  #in pixels/tick^2
        self.positionX = positionX
        self.positionY = positionY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.color = color
        self.size = size
        self.notsubject = notsubject
        self.lastposX = 0
        self.lastposY = 0
        self.popped = False


    def calculatevelchange(self, otherbody):
        if self.notsubject:
            return False

        xdifference = otherbody.positionX - self.positionX
        ydifference = otherbody.positionY - self.positionY
        #print(self.gravity)
        #print(xdifference)
        #print(ydifference)
        #print("/n")
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


        else:
            angle = math.atan(ydifference/xdifference)
            changeY = abs((math.sin(angle))*otherbody.gravity)  #Its absolute because sometimes it gives the positive and sometimes the negative result for whatever reason.
            changeX = abs((math.cos(angle))*otherbody.gravity)


            if xdifference>0:               #looks if the change should be in the positive or negative direction
                self.velocityX += changeX
            else:
                self.velocityX -= changeX
            if ydifference>0:
                self.velocityY += changeY
            else:
                self.velocityY -= changeY
            

        return True

    def move(self):
        self.lastposX = self.positionX
        self.lastposY = self.positionY
        self.positionX += self.velocityX
        self.positionY += self.velocityY

    def draw(self, currentanimation, animationfactor):
        pygame.draw.circle(globalvars.GameScreen, self.color, (int(self.lastposX + ((self.positionX-self.lastposX)/animationfactor)*currentanimation), int(self.lastposY + ((self.positionY-self.lastposY)/animationfactor)*currentanimation)), int(self.size))
        #pygame.draw.rect(globalvars.GameScreen, self.color, (self.lastposX + ((self.positionX-self.lastposX)/animationfactor)*currentanimation, self.lastposY + ((self.positionY-self.lastposY)/animationfactor)*currentanimation, 5, 5))

    def collision(self, other):
        global x
        global file
        if x == 10000:
            file.close()
        else:
            file.writelines(str(self.positionX) + " " + str(self.positionY) + "\n")
            x+=1
        if self.popped == False and other.popped == False:
            if other.notsubject or self.notsubject:
                return False
            if abs(self.positionX-other.positionX) < self.size and abs(self.positionY-other.positionY) < self.size:
                self.size = math.sqrt(self.size**2 + other.size**2)    # A = r**2 * pi,  r = sqrt(A/pi) -> newsize = sqrt(( (self.size**2 * pi) + (other.size**2 * pi) )/pi). Pi can be crossed out to get resulting formula
                self.velocityX = (self.velocityX*self.gravity + other.velocityX*other.gravity)/(self.gravity + other.gravity)
                self.velocityY = (self.velocityY*self.gravity + other.velocityY*other.gravity)/(self.gravity + other.gravity)
                self.color = ((self.color[0]*self.gravity + other.color[0] * other.gravity)/(self.gravity+other.gravity), (self.color[1]*self.gravity + other.color[1] * other.gravity)/(self.gravity+other.gravity), (self.color[2]*self.gravity + other.color[2] * other.gravity)/(self.gravity+other.gravity))
                self.gravity += other.gravity

                other.popped = True
                return True
        return False