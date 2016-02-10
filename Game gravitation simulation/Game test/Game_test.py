import pygame
import sys, os
import globalvars
import fps
import PlanetClass
import math
import random

pygame.init()

white = (255,255,255)

fonty = pygame.font.SysFont("None", 30)
textrender = fonty.render("",0,white)

fpscounter = fps.fps()
Rect_posx = 0
Rect_posy = 250
last_posx = 0

global animationfactor
animationfactor = 1
global currentanimation
currentanimation = 0

global planetlist
planetlist = []
#for i in range(1):
#    planetlist.append(PlanetClass.planet(0.01, 500, 400+(i), 10, 0, color = (0,255,0)))
#planetlist.append(PlanetClass.planet(4, 500, 400, 10, 0, color = (255,0,0)))
planetlist.append(PlanetClass.planet(1, 500, 500, 0, 0,  color = (0,0,255), notsubject = True, size = 10))
#planetlist.append(PlanetClass.planet(1, 700, 500, 0, 0,  color = (0,0,255), notsubject = False, size = 10))

changedgrav = False

def render():
    #print("Render" + str(globalvars.nextrendertime))
    global currentanimation
    global animationfactor
    global currentanimation

    globalvars.GameScreen.fill((0,0,0))


    for i in planetlist:
        i.draw(currentanimation, animationfactor)





            

            
    globalvars.GameScreen.blit(textrender, (0,0))
    globalvars.GameScreen.blit(textrender2, (0,30))
    pygame.display.update()

    globalvars.nextrendertime += globalvars.framespeed  #sets the time the next render is supposed to happen
    fpscounter.addvalue(pygame.time.get_ticks())    #adds the time the render was done to the fps counter.
    currentanimation+=1         #updates the animation tick

while True:
    while pygame.time.get_ticks() > globalvars.nextticktime:       # if there is a new physics tick due
        if pygame.time.get_ticks() > globalvars.nextticktime+globalvars.tickspeed:
            print("Currently " + str(int((pygame.time.get_ticks()-globalvars.nextticktime)/globalvars.tickspeed)) + " ticks behind.")
            
        if len(planetlist) < 25:
            planetlist.append(PlanetClass.planet(0, 500, 400, 10, 0, color = (0,255,0)))
        elif changedgrav == False:
            planetlist.append(PlanetClass.planet(0.1, 600, 500, 0, 10, color = (0,255,120), size = 5))
            planetlist.append(PlanetClass.planet(0.1, 400, 500, 0, -10, color = (0,255,120), size = 5))
            changedgrav = True
            for i in planetlist:
                if i.color == (0,255,0):
                    i.gravity = 0.01



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    render()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    globalvars.tickspersec *=2
                    globalvars.tickspeed = 1000/globalvars.tickspersec
                if event.button == 5:
                    globalvars.tickspersec /=2
                    globalvars.tickspeed = 1000/globalvars.tickspersec
            if event.type == pygame.QUIT:
                sys.exit
        for i in planetlist:
            for j in planetlist:
                x = i.calculatevelchange(j)
        poppedlist = []
        for i in range(len(planetlist)):
            for j in range(len(planetlist)):
                if i != j:
                    if planetlist[i].collision(planetlist[j]):
                        poppedlist = [j] + poppedlist

        for i in poppedlist:
            planetlist.pop(i)
                        



        for i in planetlist:
            i.move()

        textrender = fonty.render("FPS: " + str(fpscounter.give_fps()),0,white)   #creates the text render for the fps
        textrender2 = fonty.render("Ticks per sec: " + str(globalvars.tickspersec), 0, white)

        #print("tick" + str(globalvars.nextticktime))
        #print(pygame.time.get_ticks())

        animationfactor = fpscounter.give_fps()/globalvars.tickspersec  #calculates how many times you render per tick. Is used in rendering sprites
        currentanimation = 0    #set the counter for the animation to 0

        globalvars.nextticktime += globalvars.tickspeed
    
    if pygame.time.get_ticks() > globalvars.nextrendertime or globalvars.UnlimitedFPS:        # if there is a new render due
        if not pygame.time.get_ticks() > globalvars.nextrendertime+globalvars.framespeed or globalvars.UnlimitedFPS: #if the render is not a frame behind where it is supposed to be
            render()
        else:                                                       #if the render is a frame behind schedule, skip render and set next rendertime
            print("Skipping rendering of " + str(int((pygame.time.get_ticks()-globalvars.nextrendertime)/globalvars.framespeed)) + " frames.")
            globalvars.nextrendertime = pygame.time.get_ticks() + globalvars.framespeed