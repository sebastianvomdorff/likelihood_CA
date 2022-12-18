import numpy as np
from ca import cellular_automaton
from likelihood_binning import likelihood_binning
from count_to_speed_conversion import count_to_speed
from count_to_likelihood_mapping import likelihood_mapping
from pedestrian_density_overlay import ped_density_overlay
from raycast import ray_cast
import matplotlib.pyplot as plt
import time

# Import map data
lattice = np.load("map_data/garage_map_1.npy")
lattice = lattice.astype(int)

print("Show empty, static map:")
plt.imshow(lattice)
plt.show()

# Set time-step width in seconds, simulation time and
# calculate simulation steps
dt = 0.01
simulation_time = 1.5
sim_steps = int(simulation_time / dt)

# Define cell states
cell_blocked = -1
cell_empty = 0
cell_occupied = sim_steps


# Provide height, width and cell sizte of the map in meters
width = 50
height = 50
cell_size = 0.5

# Get total number of rows and columns in lattice
[rows_total, columns_total] = lattice.shape

# Record start time
start = time.time()

# Caluclate field of view in map from given ego positon
fov_map = ray_cast(lattice, 60, 90, cell_blocked)

print("Show field of view:")
plt.imshow(fov_map)
plt.show()

# Mark cells that are not blocked but outside of field of view as occupied
lattice[lattice == cell_empty] = cell_occupied

# Mark all cells within the FOV as empty
lattice[fov_map == 1] = cell_empty

print("Show field of view in static map:")
plt.imshow(lattice)
plt.show()

# neighborhood range
neighborhood_range = 1

# Calculate speed equivalents to count
speed_list = count_to_speed(sim_steps, cell_size, simulation_time)

print("the speed list: ", speed_list)

# Define pedestrian's speed mean value and standard deviation
ped_speed_mean = 1.5
ped_spd_std_dev = 0.25

# Define dummy density distribution
pedestrians_per_sqm = 0.01
pedestrians_dens_cell = pedestrians_per_sqm * cell_size * cell_size
ped_density_dist = np.ones([rows_total, columns_total]) * pedestrians_dens_cell

# Calculate likelihood bins
likelihhood_bins = likelihood_binning(
                    speed_list, sim_steps, ped_speed_mean, ped_spd_std_dev)

""" This part is only necessary for experiments on an empty map
# Create lattice from parameters
#lattice = np.zeros([rows_total, columns_total])

# Set occupation status
#lattice[width, height] = sim_steps
#lattice[round(width / 4), round(height)] = sim_steps
#lattice[round(2*width - 1), round(1.5 * height)] = sim_steps
"""
# Propagate the occupied space with the cellular automaton
lattice_propagated = cellular_automaton(sim_steps, lattice.copy(), neighborhood_range, cell_blocked)

print(likelihhood_bins)
# Calculate the likelihood distribution of pedestrians
# considering their speed distribution
lattice_lklh_eval = likelihood_mapping(likelihhood_bins, lattice_propagated.copy())

# Calculate the expected pedestrians per cell
# considering the density distribution
lattice_ped_eval = ped_density_overlay(lattice_lklh_eval.copy(), ped_density_dist)

total_collisions = np.sum(lattice_ped_eval[87:93, 60:70])
collisions_per_second = total_collisions / simulation_time

safety_threshold = 10e-7
collisions_per_hour = collisions_per_second * 3600

safety_evaluation = "unsafe"
if collisions_per_hour < safety_threshold:
    safety_evaluation = "safe"

# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds")

print("Total estimated collisions: ", total_collisions, " in ", simulation_time, "seconds.")
print("Equaling ", collisions_per_hour, " 1/hr.")
print("The maneuver is ", safety_evaluation, " considering a threshold of ", safety_threshold, " 1/hr (ASIL C for random faults).")

# Show raw lattice
print("Showing the raw propagation of the cellular automaton:")
plt.imshow(lattice_propagated)
plt.show()

# Show binned lattice
print("Showing the likelihood distribition of pedestrians:")
plt.imshow(lattice_lklh_eval)
plt.show()

# Show expected pedestrians per cell
print("Showing the expected pedestrians per cell:")
plt.imshow(lattice_ped_eval)
plt.show()


print("done")
