# Time parameters
# Set time-step width in seconds, simulation time and
# calculate simulation steps
dt = 0.05
drive_time = 1.0
brake_time = 0.5
simulation_horizon = drive_time + brake_time
sim_steps = int(simulation_horizon / dt)


# Map parameters
# data paths
map_location = "map_data/garage_map_1.npy"
path_location = 'map_data/garage_map_paths_slim_1.csv'

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
# Define pedestrian's speed mean value and standard deviation and
# fastest imaginable person
ped_speed_mean = 1.65
ped_spd_std_dev = 1.0
fastest_person = 44/3.6

# Define density distribution
pedestrians_per_sqm = 0.04

# Auxiliary parameters
# neighborhood range
neighborhood_range = 1

# Safety metric
# ASIL C
safety_threshold = 10e-7  # collisions per hour

# Use memory from previous calculation step
memory = 1

# Visualization & (print) output
show_map_init = 0
show_assessment = 0
show_empty_static = 0
show_memory_merge = 0
output = 1
