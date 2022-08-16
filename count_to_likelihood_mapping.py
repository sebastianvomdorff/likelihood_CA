import numpy as np
import math
# create look up table that maps counting values to speeds and further to cumulative likelihoods


def count_to_likelihood(speed_bins, time_steps):
    speed_bins_length = np.shape(speed_bins)[0]
    count_map = np.zeros([speed_bins_length, 2])

    # Calculate the minimum counting index  representing a quantisized speed
    for i in range(speed_bins_length):
        count_map[i,0] = math.ceil(time_steps - (time_steps / speed_bins[i, 0]))

    # Add-up the cumulative likelihood of the single bins
    count_map[0,1] = speed_bins[0,2]
    for k in range(1, speed_bins_length):
        count_map[k,1] = count_map[k-1, 1] + speed_bins[k, 1]
    
    return count_map