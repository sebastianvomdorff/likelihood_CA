import numpy as np
from scipy.stats import norm


def speed_binning(SoL, resolution, mean, std_dev):
    # np.random.normal(mean, std_dev)
    speed_bins = np.zeros([resolution, 2])
    for division in range(0, resolution):
        speed_bins[division, 0] = SoL / (division + 1)

    speed_bin_length = np.shape(speed_bins)[0]
    for i in range(speed_bin_length - 1):
        speed_bins[i, 1] = norm.cdf(speed_bins[i, 0], mean, std_dev) \
            - norm.cdf(speed_bins[i + 1, 0], mean, std_dev)
    speed_bins[speed_bin_length - 1, 1] = \
        norm.cdf(speed_bins[speed_bin_length - 1, 0], mean, std_dev)

    return speed_bins
