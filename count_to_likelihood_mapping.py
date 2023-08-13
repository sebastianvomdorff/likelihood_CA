import numpy as np


def likelihood_mapping(likelihhood_bins, map):
    """create look up table that maps counted values to speeds and further
    to cumulative likelihoods"""

    map_converted = map.astype(float)

    for i in range(np.shape(map)[0]):
        for k in range(np.shape(map)[1]):
            index_value = map[i, k]
            if index_value == 0:
                map_converted[i, k] = 0
            elif index_value == -1:
                map_converted[i, k] = -1
            else:
                map_converted[i, k] = likelihhood_bins[index_value - 1, 1]

    return map_converted
