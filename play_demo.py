from multiprocessing import connection
import numpy as np
import pygame
import random
import pandas as pd
import os
import glob

import utils
from robots import *

########################## PARAMETERS ###########################################

SAVE_VID = True
VIZGRID = False
FPS = 55
tag = "aggression"
type = "dir_omni"
vid_name = tag+"_" + type + ".mp4"
viddir = './videos'
global_filename = "configs/global_config.yaml"
c_filename = "configs/"+tag+".yaml"
e_filename = "configs/env_config.yaml"

metric = np.array([])

########################## SETUP ##########################

if not os.path.exists(viddir):
    os.mkdir(viddir)
vid_out = os.path.join(viddir, vid_name)

# set up folder for saving frames
if SAVE_VID:
    try:
        os.makedirs(tag+"_frames")
    except OSError:
        pass

params = utils.load_config(global_filename)
sim_time, ss, num = params["sim_time"], params["screen_size"], params["num_robots"]
obstacles = utils.load_env(e_filename)
width = ss # for vid
height = ss # for vid

# set up env
pygame.init()
screen = pygame.display.set_mode([ss,ss])
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# import the data
sim_data = pd.read_csv("data/demo.csv",dtype=object)

x_list = []
y_list = []
theta_list = []
stimuli_list = []
for i in range(sim_data['x'].shape[0]):
    x_list.append(list(map(float,sim_data['x'][i][1:-1].replace(" \n", "").split())))
    y_list.append(list(map(float,sim_data['y'][i][1:-1].replace(" \n", "").split())))
    theta_list.append(list(map(float,sim_data['theta'][i][1:-1].replace(" \n", "").split())))
    stimuli_list.append(list(map(float,sim_data['stim'][i][1:-1].replace(" \n", "").split())))


########################## MAIN  ###########################################3

# init robots
robots = Robots(global_filename, c_filename, type)
robots.coords = np.array([x_list,y_list]).T
robots.angles = np.array(theta_list)
robots.stimuli = np.array(stimuli_list)
robots.initGrid()

# sim loop
framenum = 0
running = True

for time in range(sim_time):
    if(not running):
        break
    # did the user click the close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the background with white
    screen.fill((255,255,255))

    for r in range(robots.num):
        c = robots.coords[r,time]
        robotsPerGrid = robots.robotUpdates(c)

    for boxes in robots.robotsPer:
            fade = 10
            concentration = robots.robotsPer[boxes]
            shade = 255 - (5*concentration)
            if shade < 0:
                shade = 0

            # find way to make it stop fading, if robot enters again

            interval = robots.ss/robots.grid_num

            xHold = boxes%robots.grid_num
            yHold = boxes//robots.grid_num

            x = xHold*interval
            y = yHold*interval

            pygame.draw.rect(screen, (255, shade, 255), (x,y,interval,interval), 0)

    # Draws all of the lines needed to make the grid, prints the box numbers (starting at 1)
    # and draws small dots at all of the intersections of the gridlines
    if VIZGRID:
        font = pygame.font.SysFont(None, 15)
        interval = robots.ss/robots.grid_num
        for row in range(robots.grid_num):
            inter = 0
            cornerNum = 1
            pt = float(row*interval)
            # draw grid lines
            pygame.draw.line(screen, (255, 0, 0), (pt, 0), (pt, robots.ss), width=1)
            pygame.draw.line(screen, (255, 0, 0), (0, pt), (robots.ss, pt), width=1)

            for column in range(robots.grid_num):
                corner = int(cornerNum + (inter/interval))
                pygame.draw.circle(screen, (255, 0, 0), (pt, inter), 3)

                img = font.render(str((column*robots.grid_num)+row), True, (255, 0, 0))
                screen.blit(img, (pt +5 , inter +5))
                cornerNum += 1
                inter += interval
            #extra row on the far right
            pygame.draw.circle(screen, (255, 0, 0), (robots.ss, pt), 3)
    ############################################################################

    # update robot positions
    for r in range(robots.num):

        c = robots.coords[r,time]
        l = robots.stimuli[time,r]

        # draw a solid blue circle in the center
        pygame.draw.circle(screen, (0,0,l), np.ceil(c), 5)

        # draw a line to show orientation
        pygame.draw.line(screen, (0,0,l), np.ceil(c), np.ceil(c+15*np.array([np.cos(robots.angles[time,r]),np.sin(robots.angles[time,r])])), 3)

    # update the display
    clock.tick(60)
    pygame.display.flip()

    # save frame to disk
    if SAVE_VID:
        fname = tag + "_frames/%04d.png" % framenum
        pygame.image.save(screen, fname)
        framenum += 1

# quit
pygame.quit()

########################## SAVE TO VID ###########################################

def 
if SAVE_VID:
    cmd = str(f"ffmpeg -r {FPS} -f image2 -i {tag}_frames/%04d.png -y -qscale 0 -s {width}x{height} {vid_out}")
    os.system(cmd)

    # remove frames when done: python should wait...
    # TODO switch to using subprocess lib
    # or maybe pathlib
    files = glob.glob('./'+tag+'_frames/*.png')
    for f in files:
        try:
            os.unlink(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
            pass

    try:
        os.rmdir('./'+tag+'_frames')
    except OSError as e:
        pass
