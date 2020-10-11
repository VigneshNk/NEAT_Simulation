# Asteroid_Simulation_AI
An AI that controls a spaceship and dodges incoming asteroids using a genetic algorithm that creates a neural network.

Download all files in the repository and run asteroid_simulator.py to start simulation.

## Required Python Modules:
Pygame, NEAT, Matplotlib, NumPy, Graphviz

## Simulation:

![Screenshot](image1.png)

## Simulation Mechanics:
     - Asteroids are spawned on to screen at random positions
  
     - Asteroids hurtle towards spaceship at random speed
  
     - Depending on which asteroids the spaceship is in between, the NEAT neural network calculates when to jump
     
     - Spaceship attempts to stay in between 2 closest asteroids so it can pass through

![Screenshot](image2.png)
