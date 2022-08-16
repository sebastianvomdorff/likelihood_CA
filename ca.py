import math
import numpy as np
from cell_update import cell_update_moore, cell_update_von_neumann, cell_update_moore_without
from speed_binning import speed_binning
from eligible_propagation_speeds import eligible_speed_bins
from count_to_likelihood_mapping import count_to_likelihood
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
simulation_time = 2
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
lattice = np.zeros([rows_total, columns_total])

# Set occupation status
lattice[width, height] =  simulation_steps

# Get approximate squareroot of 2
sqrt2 = math.sqrt(2)

print(bins)


for step in range(simulation_steps + 1):
    print("iteration ", step, " of ", simulation_steps +1)
    # Copy lattice for a temporary snapshot
    lattice_frozen = lattice.copy()
    lattice_diag = lattice.copy()

    # Move through the lattice

    if ((step % (sqrt2+1)) < 1):
        for row in range(rows_total):
            for column in range(columns_total):
                lattice[row, column] = cell_update_moore(row, column, rows_total, columns_total, neighbors, lattice_frozen)
    else:
        for row in range(rows_total):
            for column in range(columns_total):        
                lattice[row, column] = cell_update_von_neumann(row, column, rows_total, columns_total, neighbors, lattice_frozen)


#lattice = np.sum(lattice, axis=2)
lattice_evaluation = np.zeros([rows_total, columns_total, np.shape(bins)[0]])

print(count_to_likelihood(bins, simulation_steps))
# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds")

plt.imshow(lattice)
plt.show()

print("done")
