import numpy as np
from scipy.stats import norm


def speed_binning(SoL, resolution, mean, std_dev):
    # np.random.normal(mean, std_dev)
    speed_bins = np.zeros([resolution, 3])

    # Get array length / amout of lines
    speed_bin_length = np.shape(speed_bins)[0]

    # Print line index into first array column
    speed_bins[:,0] = range(1, speed_bin_length + 1)

    # Write speed quantizations in second column
    for division in range(0, resolution):
        speed_bins[division, 1] = SoL / (division + 1)
    
    # Calculate CDF likelihood for bin and store in third column
    for i in range(speed_bin_length - 1):
        speed_bins[i, 2] = norm.cdf(speed_bins[i, 1], mean, std_dev) \
            - norm.cdf(speed_bins[i + 1, 1], mean, std_dev)
    speed_bins[speed_bin_length - 1, 2] = \
        norm.cdf(speed_bins[speed_bin_length - 1, 1], mean, std_dev)

    return speed_bins
