import os
import sys

# Game properties
scale = 1.5
fps = 60
volume = 0.5
clouds = True
delta_time = 1 / fps

# Get the current script's directory
script_dir = os.path.abspath(os.path.dirname(__file__))

# Navigate one directory up
parent_dir = os.path.dirname(script_dir)

# Get the base directory of the executable
base_dir = getattr(sys, "_MEIPASS", parent_dir)

# Tile properties
tile_size = int(32 * scale)

# Screen properties
screen_width = int(800 * scale)
screen_height = tile_size * 16

def initLevel():
    global active_level
    active_level = 0