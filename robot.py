import numpy as np
import random
import pymunk

import utils
import environment

class Robot():
    def __init__(self, filename):

        # load parameters
        rconfig = utils.load_config(filename)
        self.ss = int(rconfig["screen_size"])
        self.env = environment.Environment(self.ss)

        # set up coordinates
        rng = np.random.default_rng()
        coords = rng.choice(np.arange(self.ss),size=2)
        self.coords = np.array(coords, dtype=float)
        self.disp_coords = np.array(coords, dtype=int)
        self.v = rconfig["robot_vel"]
        self.angle = np.random.random()*2*np.pi

        # robot design parameters
        self.max_vel            = float(rconfig["robot_vel"])
        self.noise_factor       = float(rconfig["noise_factor"])


        # body physics
        self.mass = 1
        self.radius = 5
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        body = pymunk.Body(mass=self.mass, moment=self.moment)
        body.position = self.coords[0], self.coords[1]
        self.body = body
        self.shape = pymunk.Circle(self.body, radius=self.radius)

    def update_state(self):
        self.coords = (self.body.position.x, self.body.position.y)
        self.angle = self.body.angle


