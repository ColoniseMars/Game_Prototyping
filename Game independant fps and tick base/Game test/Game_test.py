import pygame
import sys, os
import globalvars
import fps

pygame.init()


white = (255,255,255)

fpsTime = pygame.time.Clock()
GameScreen = pygame.display.set_mode((globalvars.window_width, globalvars.window_height))
pygame.display.set_caption(globalvars.gamename)

fonty = pygame.font.SysFont("None", 30)
textrender = fonty.render("",0,white)

fpscounter = fps.fps()
Rect_posx = 0
Rect_posy = 250
last_posx = 0

animationfactor = 1 #is 1 to prevent division by zero, gets corrected in tick calculation
currentanimation = 0

while True:
    while pygame.time.get_ticks() > globalvars.nextticktime:       # if there is a new physics tick due
        if pygame.time.get_ticks() > globalvars.nextticktime+globalvars.tickspeed:
            print("Currently " + str(int((pygame.time.get_ticks()-globalvars.nextticktime)/globalvars.tickspeed)) + " ticks behind.")
        
        last_posx = Rect_posx       #moves the dot
        Rect_posx += 10
        if Rect_posx >1000:
            Rect_posx = 0

        textrender = fonty.render("FPS: " + str(fpscounter.give_fps()),0,white)   #creates the text render for the fps
            
        print("tick" + str(globalvars.nextticktime))
        print(pygame.time.get_ticks())

        animationfactor = fpscounter.give_fps()/globalvars.tickspersec  #calculates how many times you render per tick. Is used in rendering sprites
        currentanimation = 0    #set the counter for the animation to 0

        globalvars.nextticktime += globalvars.tickspeed
    
    if pygame.time.get_ticks() > globalvars.nextrendertime or globalvars.UnlimitedFPS:        # if there is a new render due
        if not pygame.time.get_ticks() > globalvars.nextrendertime+globalvars.framespeed or globalvars.UnlimitedFPS: #if the render is not a frame behind where it is supposed to be
            print("Render" + str(globalvars.nextrendertime))

            GameScreen.fill((0,0,0))

            pygame.draw.rect(GameScreen, white, (last_posx + ((Rect_posx-last_posx)/animationfactor)*currentanimation, Rect_posy, 5, 5))    #Calculates the diffence in position based on last tick position

            GameScreen.blit(textrender, (0,0))
            pygame.display.update()

            globalvars.nextrendertime += globalvars.framespeed  #sets the time the next render is supposed to happen
            fpscounter.addvalue(pygame.time.get_ticks())    #adds the time the render was done to the fps counter.
            currentanimation+=1         #updates the animation tick
        else:                                                       #if the render is a frame behind schedule, skip render and set next rendertime
            print("Skipping rendering of " + str(int((pygame.time.get_ticks()-globalvars.nextrendertime)/globalvars.framespeed)) + " frames.")
            globalvars.nextrendertime = pygame.time.get_ticks() + globalvars.framespeed