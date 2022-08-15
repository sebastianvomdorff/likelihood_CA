import math
import numpy as np
from cell_update import cell_update_moore, cell_update_von_neumann, cell_update_moore_without
from speed_binning import speed_binning
from eligible_propagation_speeds import eligible_speed_bins
import matplotlib.pyplot as plt
import time

# Record start time
start = time.time()
# Provide height, width and cell sizte of the map in meters
width = 50
height = 50
cell_size = 0.5

# Calculate number of cells
columns_total = round(width / cell_size)
rows_total = round(height / cell_size)

# Set time-step width in seconds
dt = 0.05
simulation_time = 2.5
simulation_steps = int(simulation_time / dt)

# neighborhood range
neighborhood_range = 1
# determine all cells distances in the range
neighbors = np.arange(-neighborhood_range, neighborhood_range + 1)

# Calculate speed of light
SoL = cell_size / dt
diagonal_SoL = math.sqrt(2) * SoL

# Calculate likelihood bins
resolution = 100
pedestrian_speed_mean = 1.5
ped_spd_std_dev = 0.25
bins = speed_binning(SoL, resolution, pedestrian_speed_mean, ped_spd_std_dev)
# Create lattice from parameters
lattice = np.zeros([rows_total, columns_total, np.shape(bins)[0]])

# Set occupation status
lattice[width, height] =  bins[:, 1]

# Get approximate squareroot of 2
sqrt2 = math.sqrt(2)

print(bins)


for step in range(simulation_steps + 1):
    print("iteration ", step, " of ", simulation_steps +1)
    # Copy lattice for a temporary snapshot
    lattice_frozen = lattice.copy()
    lattice_diag = lattice.copy()

    # Determine eligible speeds for propagation in orthogonally and diagonally
    prop_speeds = np.where(eligible_speed_bins(bins, step, SoL*1.1)[:, 1] > 0, 1, 0)
    prop_speeds_diag = np.where(eligible_speed_bins(bins, step, diagonal_SoL)[:, 1] > 0, 1, 0)

    # Move through the lattice
    #if ((step % (sqrt2+1)) < 1):
    for row in range(rows_total):
        for column in range(columns_total):
            lattice[row, column] = cell_update_von_neumann(row, column, rows_total, columns_total, prop_speeds, neighbors, lattice_frozen)
            lattice_diag[row, column] = cell_update_moore_without(row, column, rows_total, columns_total, prop_speeds_diag, neighbors, lattice_frozen)

    lattice = np.maximum(lattice, lattice_diag)

    #else:
    #    for row in range(rows_total):
    #        for column in range(columns_total):
    #            lattice[row, column] = cell_update_von_neumann(row, column, rows_total, columns_total, prop_speeds, neighbors, lattice_frozen)

    sum_lattice = np.sum(lattice, axis=2)

    # plt.imshow(sum_lattice)
    # plt.show()

# Generate cumulative propabilities
# print(lattice)
print(lattice[50, 60])
lattice = np.sum(lattice, axis=2)

# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds")

plt.imshow(lattice)
plt.show()

print("done")
