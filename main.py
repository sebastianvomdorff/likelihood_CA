import numpy as np
from likelihood_binning import likelihood_binning
from count_to_speed_conversion import count_to_speed
from drive_path import drive_path
import matplotlib.pyplot as plt
import time
import config
import sys


def path_import(file):
    """This function imports a CSV file and
    interprets values >=1 as numbered waypoints.
    The coordinates of each waypoint are stored in the path array.
    It matches the patter, [waypoint_number, y, x]"""

    csv = np.loadtxt(file, delimiter=";")
    last_waypoint = int(np.max(csv))
    path = np.zeros([last_waypoint, 3])

    for i in range(0, last_waypoint):
        path[i, 0] = i + 1
        path[i, 1:3] = np.where(csv == i + 1)
    return path


def footprint_import(file):
    """This function imports a CSV file and
    interprets values >=1 as numbered footprints according to the waypoints."""

    footprint_map = np.loadtxt(file, delimiter=";")
    return footprint_map


# Value sanity check
if config.sim_steps * config.dt != config.simulation_horizon:
    print(
        "WARNING: Your chosen drive or brake time is not a multiple of your simulation resolution time.",
        "Rounding errors might occur during this simulation.",
    )

# Import map data
lattice = np.load(config.map_location)
lattice = lattice.astype(int)

# Get total number of rows and columns in lattice
[rows_total, columns_total] = lattice.shape

# Show imported map
if config.show_empty_static:
    print("Show empty, static map:")
    plt.imshow(lattice)
    plt.show()

# Import path & footprint
path = path_import(config.path_location)
footprint_map = footprint_import(config.footprint_location)
if config.show_footprint_map:
    plt.imshow(footprint_map)
    plt.show()

# print("path: ", path)
# print("path shape: ", path.shape)

# Calculate cell-speed of vehicle in cell/sim-step
cell_speed = config.v_vehicle * config.t_atomic * config.dt / config.cell_size
print("cell_speed: ", cell_speed, " cells per simulation step")
# Calculate pedestrian density for map
pedestrians_dens_cell = config.pedestrians_per_sqm * config.cell_size * config.cell_size
ped_density_dist = np.ones([rows_total, columns_total]) * pedestrians_dens_cell

# Begin tasks #
# Record start time
start = time.time()

# Calculate speed equivalents to count
speed_list = count_to_speed()
if config.output:
    print("The speeds mapped to counting values: ", speed_list)

# Calculate likelihood bins
likelihhood_bins = likelihood_binning(speed_list)
if config.output:
    print("The likelihood bins mapped töo the counting values: ", likelihhood_bins)

# safety_violations = 0
path_result = drive_path(
    likelihhood_bins,
    ped_density_dist,
    lattice,
    path,
    cell_speed,
    speed_list,
    footprint_map,
)

"""
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
# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds.")
print("done")
