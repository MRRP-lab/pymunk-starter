import numpy as np
import pandas as pd
import random
import math
import time
import os
import pymunk
import pymunk.pygame_util
import pygame

# custom imports
import utils
from robot import *

## PARAMETERS

tag = "test" # change to save data under unique name
VIZ = True

## GLOBAL STATE

# track global time to enable time-varying vector field
sim_state = {
    "time": 0.0
}

## METHODS

# custom vector field velocity forcing function
# arguments are fixed by pymunk
def vector_field(body, gravity, damping, dt):
    x,y = body.position
    force_x = 0
    # make force dependent on location and time
    t = sim_state["time"]
    force_y = 200*math.sin(t*y)

    # apply standard damping to stabilize movement
    body.velocity = body.velocity * damping

    # calculate and apply acceleration
    acceleration = pymunk.Vec2d(force_x, force_y) / body.mass
    body.velocity += acceleration*dt

def run():
    # Initialize parameters
    global_filename = "configs/global_config.yaml"
    e_filename = "configs/env_config.yaml"

    datadir = './data'
    if not os.path.exists(datadir):
        os.mkdir(datadir)

    # load configs
    gparams = utils.load_config(global_filename)
    sim_time, ss, FPS = gparams["sim_time"], gparams["screen_size"], gparams["FPS"]
    obs = utils.load_env(e_filename)

    # set up environment
    space = pymunk.Space()
    space.gravity = 0, 0 # no gravity: top-down view
    for poly in obs:
        # shift coordinates to be centered at zero
        polynp = np.array(poly)
        center = polynp.mean(axis=0)
        genpoly = (polynp - center).tolist()
        shape = pymunk.Poly(space.static_body, genpoly)
        # shift polygon body back to intended location
        shape.body.position = center.tolist()
        space.add(shape)

    # spawn robots
    robot = Robot(global_filename)
    robot.body.velocity = [gparams["robot_vel"],0.] # initial velocity vector
    robot.body.velocity_func = vector_field # set custom velocity function
    space.add(robot.body, robot.shape)

    # set up sim and vizualization
    sim_data = [] # for logging data
    if VIZ:
        pygame.init()
        screen = pygame.display.set_mode((ss,ss))
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        clock = pygame.time.Clock()

    # timing
    dt = 1.0 / FPS

    ### Simulation Loop

    for t in range(int(sim_time/dt)):

        # update robot positions
        space.step(dt)
        sim_state["time"] += dt
        robot.update_state()

        # log position data for replay_sim
        sim_data.append([robot.coords[0], robot.coords[1], robot.angle])

        if VIZ:
            # fill the background with white
            screen.fill((255,255,255))
            space.debug_draw(draw_options)
            c = robot.coords
#            # draw a solid blue circle in the center
#            pygame.draw.circle(screen, (0,0,255), np.ceil(c), 5)
#            # draw a line to show orientation
#            pygame.draw.line(screen, (0,0,255), np.ceil(c), np.ceil(c+15*np.array([np.cos(robot.angle),np.sin(robot.angle)])), 3)
            # update the display
            pygame.display.flip()
            clock.tick(FPS)

    data = pd.DataFrame(data = sim_data, columns = ["x","y","theta"])
    outdat = os.path.join(datadir, tag+".csv")
    data.to_csv(outdat)

if __name__ == '__main__':
    run()
