# Pymunk for Mobile Robot Simulation

This repository is intended to be a starting place for (relatively) quickly
spinning up a two-dimensional physics-based simulation of a robotic system.

[Pymunk Docs](https://www.pymunk.org/en/latest/pymunk.html)

## Getting started

### Dependencies

See [the PyProject manifest](./pyproject.toml).

Can install dependencies with:

```code
pip install -e .
```

### Running Simulator

Run `python run_sim.py`. This will cause an animation to pop up while the
simulator is running. You can disable the visualization by setting `VIZ =
False` at the top of `run_sim.py`. Either way, the script will log data in
the `data/` folder.

Once you have run the simulator, you can run `python replay_sim.py`. This will
also cause a box to pop up, re-visualizing the simulation. If you change the
variable `SAVE_VID` within `replay_sim.py` to true, the program will save a
video to the `videos` folder (requires ffmpeg).

Check out `configs/global_config.yaml` to change some simulation parameters.

## Design Choices

We have separated generation of the simulation (`run_sim.py`) from
visualization of the simulation (`replay_sim.py`). While pymunk is pretty
efficient, at larger numbers of agents or more complex environments, the simulation
cannot render in real time while also solving for the physics and interactions involved.

In `replay_sim.py`, we've included trails to see where robots have been.
