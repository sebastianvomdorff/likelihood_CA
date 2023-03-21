import numpy as np
from likelihood_binning import likelihood_binning
from count_to_speed_conversion import count_to_speed
from drive_path import drive_path
import matplotlib.pyplot as plt
import time
import config


def path_import(file):
    """ This function imports a CSV file and
    interprets values >=1 as numbered waypoints.
    The coordinates of each waypoint are stored in the path array.
    It matches the patter, [waypoint_number, y, x]"""

    csv = np.loadtxt(file, delimiter=';')
    last_waypoint = int(np.max(csv))
    path = np.zeros([last_waypoint, 3])

    for i in range(0, last_waypoint):
        path[i, 0] = i+1
        path[i, 1:3] = np.where(csv == i+1)
    return path


# Import map data
lattice = np.load(config.map_location)
lattice = lattice.astype(int)

# Get total number of rows and columns in lattice
[rows_total, columns_total] = lattice.shape

# Show imported map
print("Show empty, static map:")
plt.imshow(lattice)
plt.show()

# Import path
path = path_import(config.path_location)
# print("path: ", path)
# print("path shape: ", path.shape)

# Calculate cell-speed of vehicle
cell_speed = config.v_vehicle / config.cell_size  # cells per second

# Calculate pedestrian density for map
pedestrians_dens_cell = config.pedestrians_per_sqm * config.cell_size * config.cell_size
ped_density_dist = np.ones([rows_total, columns_total]) * pedestrians_dens_cell

# Begin tasks #
# Record start time
start = time.time()

# Calculate speed equivalents to count
speed_list = count_to_speed()
# print("the speed list: ", speed_list)

# Calculate likelihood bins
likelihhood_bins = likelihood_binning(speed_list)

# safety_violations = 0
path_result = drive_path(likelihhood_bins, ped_density_dist, lattice, path, cell_speed)

# print("The safety requirements have been violated in ", safety_violations, " cases.")
"""
safety_threshold = 10e-7
collisions_per_hour = collisions_per_second * 3600

safety_evaluation = "unsafe"
if collisions_per_hour < safety_threshold:
    safety_evaluation = "safe"

# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds")


print("Total estimated collisions: ", total_collisions, " in ", simulation_horizon, "seconds.")
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
"""
end = time.time()
print("Time elapsed: ", end - start, " seconds.")
print("done")