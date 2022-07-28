import math
import numpy as np
import copy
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
dt = 0.02
simulation_time = 1.5
simulation_steps = int(simulation_time / dt)

# neighborhood range
neighborhood_range = [-1, 0, 1]

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
lattice[50, 50] = bins[:, 1]

print(bins)


for step in range(simulation_steps + 1):
    print("iteration: ", step)
    # Copy lattice for a temporary snapshot
    lattice_frozen = lattice.copy()

    # Determine eligible speeds for propagation in orthogonally and diagonally
    prop_speeds = np.where(eligible_speed_bins(bins, step, SoL)[:, 1] > 0, 1, 0)   
    prop_speeds_diag = np.where(eligible_speed_bins(bins, step, diagonal_SoL)[:, 1] > 0, 1, 0)
    #print(prop_speeds)
    #print(prop_speeds_diag)
    # Move through the lattice
    for row in range(rows_total):
        for column in range(columns_total):

            # Browse through neighboring cells of the Moore neighborhood
            for delta_row in neighborhood_range:
                for delta_column in neighborhood_range:
                    current_neighbor = [row + delta_row, column + delta_column]
                    # Check for boundaries of lattice
                    if (current_neighbor[0] >= 0) and (current_neighbor[0] < rows_total):
                        if (current_neighbor[1] >= 0) and (current_neighbor[1] < columns_total):
                            # select von Neumann neighborhood
                            if (current_neighbor[0]) == row or (current_neighbor[1] == column):
                                lattice[row, column] = np.maximum(lattice[row, column], np.multiply(lattice_frozen[current_neighbor[0], current_neighbor[1]], prop_speeds))
                            # select Moore neighborhood
                            if (current_neighbor[0]) != row and (current_neighbor[1] != column):
                                 lattice[row, column] = np.maximum(lattice[row, column], np.multiply(lattice_frozen[current_neighbor[0], current_neighbor[1]], prop_speeds_diag))
    sum_lattice = np.sum(lattice, axis=2)

    # plt.imshow(sum_lattice)
    # plt.show()

# Generate cumulative propabilities
# print(lattice)
print(lattice[50,60])
lattice = np.sum(lattice, axis=2)

# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end-start, " seconds")

plt.imshow(lattice)
plt.show()

print("done")
