import numpy as np
from ca import cellular_automaton
from likelihood_binning import likelihood_binning
from count_to_speed_conversion import count_to_speed
from count_to_likelihood_mapping import likelihood_mapping
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

# Set time-step width in seconds, simulation time and
# calculate simulation steps
dt = 0.01
simulation_time = 2
sim_steps = int(simulation_time / dt)

# neighborhood range
neighborhood_range = 1

# Calculate speed equivalents to count
speed_list = count_to_speed(sim_steps, cell_size, simulation_time)

# Define pedestrian's speed mean value and standard deviation
ped_speed_mean = 1.5
ped_spd_std_dev = 0.25

# Calculate likelihood bins
likelihhood_bins = likelihood_binning(
                    speed_list, sim_steps, ped_speed_mean, ped_spd_std_dev)

# Create lattice from parameters
lattice = np.zeros([rows_total, columns_total])

# Set occupation status
lattice[width, height] = sim_steps
lattice[round(width / 4), round(height)] = sim_steps
lattice[round(2*width - 1), round(1.5 * height)] = sim_steps

# Propagate the occupied space with the cellular automaton
lattice = cellular_automaton(sim_steps, lattice, neighborhood_range)

# Show raw lattice
lattice_eval = likelihood_mapping(likelihhood_bins, lattice)

# Calculate elapsed time
end = time.time()
print("Time elapsed: ", end - start, " seconds")

plt.imshow(lattice)
plt.show()

# Show binned lattice
plt.imshow(lattice_eval)
plt.show()

print("done")
