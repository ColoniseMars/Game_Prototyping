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

planetlist.append(PlanetClass.planet(1, 400, 500, 0, 0))
planetlist.append(PlanetClass.planet(1, 500, 500, 0, 0))


#planetlist.append(PlanetClass.planet(1, 500, 500, 0, 0,  color = (0,0,255), notsubject = True, size = 10))
#planetlist.append(PlanetClass.planet(0.1, 200, 500, 0, math.sqrt(1500), color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), size = 5))
#planetlist.append(PlanetClass.planet(0.1, 500, 500, 0, 0, color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), size = 5))
#planetlist.append(PlanetClass.planet(0.001, 200, 450, math.sqrt(5), math.sqrt(1500), color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))

center_of_force = PlanetClass.planet(0, 0, 0, 0, 0)

planetsspawned = False

go=True

newsimulation = True

def render():
    #print("Render" + str(globalvars.nextrendertime))
    global currentanimation
    global animationfactor

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
            
        #if len(planetlist) < 25 and not planetsspawned:
        #    planetlist.append(PlanetClass.planet(0.01, 500, 400, 10, 0, color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))
        #else:
        #    planetsspawned = True
        #elif changedgrav == False:

        #    changedgrav = True
        #    for i in planetlist:
        #        if i.gravity == 0:
        #            i.gravity = 0.01



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    go = True
                if event.key == pygame.K_SPACE:
                    render()
                if event.key == pygame.K_s:
                    planetlist.append(PlanetClass.planet(0.01, 500, 400, 10, 0, color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    globalvars.tickspersec *=2
                    globalvars.tickspeed = 1000/globalvars.tickspersec
                if event.button == 5:
                    globalvars.tickspersec /=2
                    globalvars.tickspeed = 1000/globalvars.tickspersec
            if event.type == pygame.QUIT:
                os._exit
        
        if newsimulation:        
            sumgravposx = 0
            sumgravposy = 0
            sumgravity = 0
            for i in planetlist:
                sumgravposx += i.positionX*i.gravity
                sumgravposy += i.positionY*i.gravity
                sumgravity += i.gravity
            
            center_of_force.positionX = sumgravposx/sumgravity
            center_of_force.positionY = sumgravposy/sumgravity
            center_of_force.gravity = sumgravity



            if go:
                for i in planetlist:
                    i.calculatevelchange(center_of_force)
        else:
            if go:
                for i in planetlist:
                    for j in planetlist:
                        i.calculatevelchange(j)


        for i in range(len(planetlist)):
            for j in range(len(planetlist)):
                if i != j:
                    planetlist[i].collision(planetlist[j])

        newlist = []
        for i in planetlist:
            if i.popped == False:
                newlist.append(i)
                        
        planetlist = newlist

        if go:
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
            render()