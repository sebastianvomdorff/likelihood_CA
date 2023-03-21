import numpy as np
from scipy.stats import norm
import config

def likelihood_binning(count_to_speed):
    # np.random.normal(mean, std_dev)
    likelihood_bins = np.zeros([config.sim_steps, 2])

    for k in range(config.sim_steps):
        likelihood_bins[k, 0] = k+1

    # Calculate inv. CDF (1-CDF) likelihood for bin and store in third column
    for i in range(config.sim_steps):
        likelihood_bins[i, 1] = norm.sf(count_to_speed[i, 1],
                                        config.ped_speed_mean,
                                        config.ped_spd_std_dev)
    likelihood_bins[config.sim_steps - 1, 1] = 1

    return likelihood_bins
