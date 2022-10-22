import numpy as np
from scipy.stats import norm


def likelihood_binning(count_to_speed, time_steps, mean, std_dev):
    # np.random.normal(mean, std_dev)
    likelihood_bins = np.zeros([time_steps, 2])

    for k in range(time_steps):
        likelihood_bins[k, 0] = k+1

    # Calculate inv. CDF (1-CDF) likelihood for bin and store in third column
    for i in range(time_steps):
        likelihood_bins[i, 1] = norm.sf(count_to_speed[i, 1], mean, std_dev)

    return likelihood_bins
