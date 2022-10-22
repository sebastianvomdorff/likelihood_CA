import numpy as np

# create look up table that maps counted values to speeds and further to
# cumulative likelihoods


def likelihood_mapping(likelihhood_bins, ca_map):

    ca_map_converted = ca_map.copy()

    for i in range(np.shape(ca_map)[0]):
        for k in range(np.shape(ca_map)[1]):
            index_value = int(ca_map[i, k])-1
            if index_value == -1:
                ca_map_converted[i, k] = 0
            else:
                ca_map_converted[i, k] = likelihhood_bins[index_value, 1]

    return ca_map_converted
