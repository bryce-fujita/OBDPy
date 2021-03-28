#evo_gui.py
import config, ecu, time, datetime, sys
import pygame, time, os
from pygame.locals import *

#Helper function used to display strings on screen
def drawText(string, x, y):
    text = pyfont.render(string, True, config.WHITE)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx + x
    textRect.centery = windowSurface.get_rect().centery + y
    windowSurface.blit(text, textRect)

def drawGauge(x, y, val, xmin, xmax):
    ##Get Window dimensions
    pos = windowSurface.get_rect()
    ##Draw background to gauge
    gaugeBg = pygame.Surface((config.GWIDTH,config.GHEIGHT))
    gaugeBg.fill(config.GBGCOLOR)
    rectBg = gaugeBg.get_rect(center = (pos.centerx + x, pos.centery + y))
    ##Bar to show how full the gauge is
    perc = val/xmax
    if perc > 1:
        perc = 1
    gaugeC = pygame.Surface((config.GWIDTH*perc,config.GHEIGHT))
    gaugeC.fill(config.GCOLOR)
    rectC = gaugeBg.get_rect(center = (pos.centerx + x, pos.centery + y))
    ##Gauge Border
    gaugeB = pygame.Surface((config.GWIDTH,config.GHEIGHT))
    rectB = gaugeB.get_rect(center = (pos.centerx + x, pos.centery + y))
    windowSurface.blit(gaugeBg,rectBg)
    windowSurface.blit(gaugeC,rectC)
    pygame.draw.rect(windowSurface,config.WHITE,rectB,2)

#Setup Clock
clock = pygame.time.Clock()

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
    pygame.init()

#Setup Fonts
pyfont = pygame.font.Font('/home/pi/fonts/HighlandGothicFLF.ttf',30)

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
    drawText("Speed: " +str(ecu.speed) + " mph",250,0)

    #Coolant Temp#
    drawText(str(ecu.coolantTemp) + "\xb0C", 250,50)

    #Engine Load#
    drawText(str(ecu.engineLoad) + " %", -250,0)

    #Boost#
    drawText(str(ecu.boost) + " psi", 0, 200)
    drawGauge(0,225,ecu.boost,0,30)
    
    dt = clock.tick()

    pygame.display.update()

    
