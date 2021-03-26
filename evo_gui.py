#evo_gui.py
import config, ecu, time, datetime, sys
import pygame, time, os
from pygame.locals import *

#Helper function used to display strings on screen
def drawText(string, x, y)
    text = pyfont.render(string, TRUE, config.BLACK)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + x
    textRect.centery = windowSurface.get_rect().centery + y
    windowSurface.blit(text, textRect)

#Start ECU thread
ecu.ecuThread()

#Prevents program from progressing until ECU is ready
while not config.ecuReady:
    time.sleep(0.01)

#Set up pi for tablet version, else set up for normal desktop use
if config.piTFT:
    os.putenv('SDL_FBDEV', '/dev/fb1')
    pygame.init()
    pygame.mouse.set_visible(0)
    windowSurface = pygame.display.set_mode(config.RESOLUTION)
else:
    windowSurface = pygame.display.set_mode(config.RESOLUTION,0,32)

#Setup Fonts
pyfont = pygame.font.Font("/home/pi/font/ASL_light.ttf",30)

#Setup the caption for the window
pygame.display.set_caption('Fuji Code\'s Gauge Display')

#Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            ecu.connection.close()
            pygame.quit()
            sys.exit()
            
    ##Fills background to be black
    windowSurface.fill(config.BLACK)

    ##Writing values to display##

    #Rpms#
    drawText("RPMs: "+str(ecu.rpm),0,0)

    #Speed#
    drawText("Speed: " +str(ecu.speed) + " mph",170,0)

    #Coolant Temp#
    drawText(str(ecu.coolantTemp) + "\xb0C", 170,50)

    #Engine Load#
    drawText(str(ecu.engineLoad) + " %", -170,0)

    #Boost#
    drawText(str(ecu.boost) + " psi", 0, 200)

    dt = clock.tick()

    pygame.display.update()

    
