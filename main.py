import mp440 as mp
import time
import sys
import os
import random
import threading
import math

# External libraries 
import pygame
import numpy
import matplotlib

av = 0
TARGET_LOCATION = (0, 0)
TARGET_OBSERVED_LOCATION = (0, 0)
TARGET_ESTIMATED_LOCATION = (0, 0)

'''
Prepare UI
'''
PG_BACKGROUND = (0, 0, 0)
PG_CELL_SIZE = 5
PG_GRID_SIZE = 100
PG_SCREEN = None
PG_IMAGE_SIZE = 25
PG_TARGET_IMAGE = None
PG_GAME_EXIT = False
PG_UI_UPDATED = False

PG_LASER_IMAGE_WIDTH = 10
PG_LASER_IMAGE_HEIGHT = 500
PG_LASER_IMAGE = None
PG_LASER_ON = False
PG_LASER_ON_COUNTER = 0

def _setup_ui():
    global PG_SCREEN
    global PG_TARGET_IMAGE
    global PG_TARGET_OBSERVED_IMAGE
    global PG_LASER_IMAGE

    # Initialize pygame    
    pygame.init()
    screen_width = PG_CELL_SIZE * PG_GRID_SIZE
    PG_SCREEN = pygame.display.set_mode((screen_width, screen_width),
        pygame.DOUBLEBUF|pygame.HWSURFACE)
    PG_SCREEN.fill(PG_BACKGROUND)
    pygame.display.set_caption("ghost hunt")
    pygame.display.update()

    # Load the target image
    PG_TARGET_IMAGE = pygame.transform.scale(pygame.image.load("target-actual.png"), 
            (PG_IMAGE_SIZE,PG_IMAGE_SIZE))
    PG_TARGET_OBSERVED_IMAGE = pygame.transform.scale(pygame.image.load("target-observed.png"), 
            (PG_IMAGE_SIZE,PG_IMAGE_SIZE))
    PG_LASER_IMAGE = pygame.transform.scale(pygame.image.load("laser.png"),
            (PG_LASER_IMAGE_WIDTH,PG_LASER_IMAGE_HEIGHT))                                
                                        

'''
The main UI loop that processes messages and drawing 
'''
def _ui_loop():
    global PG_GAME_EXIT
    global TARGET_LOCATION
    global TARGET_OBSERVED_LOCATION
    global TARGET_ESTIMATED_LOCATION
    global PG_TARGET_IMAGE
    global PG_TARGET_OBSERVED_IMAGE
    global PG_UI_UPDATED
    global PG_SCREEN
    global PG_LASER_IMAGE_WIDTH

    global PG_LASER_IMAGE
    global PG_LASER_ON

    while not PG_GAME_EXIT:
        # Poll events
        event = pygame.event.poll()

        # Process events

        # NOEVENT, simply continue
        if event.type == pygame.NOEVENT:
            pass
        
        # QUIT events
        elif event.type == pygame.QUIT:
            PG_GAME_EXIT = True

        # Update UI
        if PG_UI_UPDATED == True:
            # Redraw the screen
            PG_SCREEN.fill(PG_BACKGROUND)
            (rx, ry) = PG_SCREEN.get_rect().topleft

            # Draw the target
            if PG_LASER_ON:
                (ex, ey) = TARGET_ESTIMATED_LOCATION
                PG_SCREEN.blit(PG_LASER_IMAGE, (rx + ex + PG_LASER_IMAGE_WIDTH/2 + 2, 0))

                (x, y) = TARGET_LOCATION
                PG_SCREEN.blit(PG_TARGET_IMAGE, (rx + x, ry + y))

            # Draw observed
            if not PG_LASER_ON:
                (ox, oy) = TARGET_OBSERVED_LOCATION
                PG_SCREEN.blit(PG_TARGET_OBSERVED_IMAGE, (rx + ox, ry + oy))

            # Draw estimated
            #(ex, ey) = TARGET_ESTIMATED_LOCATION
            #PG_SCREEN.blit(PG_TARGET_IMAGE, (rx + ex, ry + ey))

            pygame.display.update()
            PG_UI_UPDATED = False

    pygame.quit()


'''
Background process for driving 
'''
START_TIME = time.time()
def _background_logic():
    global START_TIME
    global LAST_ELAPSED_TIME
    global PG_UI_UPDATED
    global TARGET_LOCATION
    global TARGET_OBSERVED_LOCATION
    global TARGET_ESTIMATED_LOCATION
    global PG_LASER_ON

    # Nose matrices
    cov_t = [[2, 0.5], [0.5, 2]]
    cov_o = [[200, 50], [50, 300]]

    # Runs as long as program does not quite
    first_iteration = True
    while not PG_GAME_EXIT:
        # Sleep a bit
        time.sleep(0.2)
        
        # Retrieve elapsed time
        elapsed_time = time.time() - START_TIME

        # Compute x, y location assuming the target tries to follow a cycle
        (x, y) = (150*math.cos(elapsed_time/4) + PG_CELL_SIZE * PG_GRID_SIZE * 0.5 - PG_IMAGE_SIZE/2 + random.randint(-4, 4), 
                 100*math.sin(elapsed_time/4) + PG_CELL_SIZE * PG_GRID_SIZE * 0.3 - PG_IMAGE_SIZE/2 + random.randint(-3, 3))
        (oldx, oldy) = TARGET_LOCATION
        if (x != oldx or y != oldy) and (not PG_LASER_ON):
            ux = x - oldx
            uy = y - oldy

            # Compute x, y location assuming the target follows a cycle
            uxn, uyn = numpy.random.multivariate_normal([0,0], cov_t, 1).T
            TARGET_LOCATION = (x + uxn[0], y + uyn[0])
            
            oxn, oyn = numpy.random.multivariate_normal([0,0], cov_o, 1).T
            TARGET_OBSERVED_LOCATION = (x + oxn[0], y + oyn[0])

            # Calling the shots... 
            (ex, ey, shoot) = mp.kalman2d_shoot(ux, uy, x + oxn[0], y + oyn[0], first_iteration)
            if first_iteration == True:
                first_iteration = False

            TARGET_ESTIMATED_LOCATION = (ex, ey)
            if shoot == True:
                PG_LASER_ON = True
                print "Shot fired!"
                print "Actual target location is (" + str(TARGET_LOCATION[0]) + "," + str(TARGET_LOCATION[1])
                print "Estimated target location is (" + str(ex) + "," + str(ey)
                print "Off target center by " + str(ex - TARGET_LOCATION[0])
                global av
                av +=math.fabs(ex - TARGET_LOCATION[0])
            PG_UI_UPDATED = True
    return

'''
Load data 
'''
def _load_data():
    lines = [line.rstrip('\n') for line in open("data.txt")]
    data = []
    for line in range(0, len(lines)):
        data.append(map(float, lines[line].split(' ')))
    return data


if __name__ == "__main__":

    # This is for part a of the MP. Comment this when you want to work on part b of the MP
    data = _load_data()
    output = mp.kalman2d(data)
    mp.plot(data, output)

    # This is for part b of the MP. Uncomment when you work on this part of the MP
    
    #Remove the block comment to work on part b of the the MP 

    # Setup the UI
    for x in range(0,50):
        _setup_ui()

        # Start main logic thread
        thread = threading.Thread(target=_background_logic)
        thread.start()

        # Enter UI loop
        _ui_loop()
    print(av/50)
