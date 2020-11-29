import arcade
import random
import os
import pathlib
import math
import numpy

FILE_PATH = pathlib.Path(__file__)
PATH = FILE_PATH.parent

SCREEN_WIDTH = 1600#500*3
SCREEN_HEIGHT = 720#240*3
SCREEN_TITLE = "Shoot Test"
UPDATE_RATEHz = 1/90.1

# How big the particle
PARTICLE_RADIUS = 1

# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5

# How fast to fade the particle
PARTICLE_FADE_RATE = 8

# Chance we'll flip the texture to white and make it 'sparkle'
PARTICLE_SPARKLE_CHANCE = 0.04

# How fast the particle will accelerate down. Make 0 if not desired
PARTICLE_GRAVITY = 0.05

# Chance we leave smoke trail
SMOKE_CHANCE = 0.05

# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.20
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5

# Possible particle colors
PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON,
                           arcade.color.COQUELICOT,
                           arcade.color.LAVA,
                           arcade.color.KU_CRIMSON,
                           arcade.color.DARK_TANGERINE,
                           arcade.color.BANANA_YELLOW]    

# Choose a random color
#color = random.choice(PARTICLE_COLORS)