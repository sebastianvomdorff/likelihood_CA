import numpy as np


def likelihood_mapping(likelihhood_bins, ca_map):
    """ create look up table that maps counted values to speeds and further
    to cumulative likelihoods """

    ca_map_converted = ca_map.astype(float)

    for i in range(np.shape(ca_map)[0]):
        for k in range(np.shape(ca_map)[1]):
            index_value = ca_map[i, k]
            if index_value == 0:
                ca_map_converted[i, k] = 0
            elif index_value == -1:
                ca_map_converted[i, k] = -1
            else:
                ca_map_converted[i, k] = likelihhood_bins[index_value - 1, 1]

    return ca_map_converted
