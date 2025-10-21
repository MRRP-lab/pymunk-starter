# Pymunk for robotics simulation

This repository is intended to be a starting place for (relatively) quickly
spinning up a two-dimensional simulation of a robotic system.

[Pymunk Docs](https://www.pymunk.org/en/latest/pymunk.html)

## Getting started

Run `python generate_demo.py`, then run `python play_demo.py`. The second
command should cause a box to pop up, visualizing the simulation. `play_demo.py`
will also save a video to the `videos` folder.

## Design Choices

We have separated generation of the simulation (`generate_demo.py`) from
visualization of the simulation (`play_demo.py`). While pymunk is pretty
efficient, at larger numbers of agents, the simulation cannot render in real
time while also solving for the physics and interactions involved.

We've included trails to see where robots have been and a pointer to show robot
orientation.

Most of the interesting stuff happens in `robots.py`. The robots are set up to
act like Braitenberg vehicles; try changing values in `configs/aggresion.yaml`
and see what happens to the robot behaviors.

The environment is set up to act like a torus (the top and bottom of the screen
are connected to each other, and the left and right are paired as well). TODO:
make the torus geometry more modular so we can switch on and off.

## Dependencies

- yaml
- pygame
- numpy
- pylab
- pandas
