# import main

# Time parameters
# Set time-step width in seconds, simulation time and
# calculate simulation steps
t_atomic = 0.001  # Atomic unit for simulation in seconds
dt = 50  # Simulation resolution in atomic units
drive_time = 1000
brake_time = 500
simulation_horizon = drive_time + brake_time

sim_steps_drive = int(drive_time / dt)
sim_steps_brake = int(brake_time / dt)
sim_steps = sim_steps_drive + sim_steps_brake


# Map parameters
# data paths
map_location = "map_data/garage_map_1.npy"
path_location = "map_data/garage_map_paths_slim_1.csv"
footprint_location = "map_data/garage_map_paths_footprint_1.csv"


# Define cell states
cell_blocked = -1
cell_empty = 0
cell_occupied = sim_steps
# Provide height, width and cell sizte of the map in meters
width = 50
height = 50
cell_size = 0.5


# Vehicle parameters
# Define vehicle speed through cells
v_vehicle = 10 / 3.6  # speed from km/h to m/s

# Pedestrian parameters
# Define pedestrian speed as a fixed value
fixed_speed = 0
ped_speed_fixed = 2

# Define pedestrian's speed mean value and standard deviation and
# fastest imaginable person
ped_speed_mean = 1.3
ped_spd_std_dev = 0.3
fastest_person = 44 / 3.6

# Define density distribution
pedestrians_per_sqm = 0.04

# Auxiliary parameters
# neighborhood range
neighborhood_range = 1

# Safety metric
# ASIL C
safety_threshold = 10e-7  # collisions per hour

# Use memory from previous calculation step
memory = 0

# Use map slicing for lowering computation time
slicing = 0

# Cut off velocity for pedestrians at ego velocity (ref. to RSS)
v_ego_cut_off = 0

# Visualization & (print) output
show_footprint_map = 0
show_map_init = 1
show_assessment = 1
show_empty_static = 0
show_memory = 0
show_extrapolation = 1
show_memory_merge = 0
show_map_slice = 0
output = 1

# Debug options:
debug_fixed_speed = 0
debug_lattice_propagated = 0
debug_cut_off = 0
debug_likelihood_overlay = 0
debug_lattice_intermediate = 0
debug_show_intermediate_assessment = 0
