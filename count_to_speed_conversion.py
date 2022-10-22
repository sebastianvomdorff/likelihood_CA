import numpy as np
# import math
# create look up table that maps counting values to speeds and further to
# cumulative likelihoods


def count_to_speed(time_steps, cell_size, simulation_time):

    # set up look up table that map count so speed
    count_mapping = np.zeros([time_steps, 2])

    # Calculate the minimum counting index  representing a quantisized speed
    for i in range(time_steps):
        count_mapping[i, 0] = i+1
        count_mapping[i, 1] = cell_size * (time_steps - i) / simulation_time

    return count_mapping
