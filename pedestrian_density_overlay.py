import numpy as np
import config

def ped_density_overlay(likelihood_map, density_map):
    if likelihood_map.shape != density_map.shape:
        print("Density map does not match with CDF lattice dimensions!")
        return likelihood_map
    else:
        pedestrian_expectancy_map = np.zeros(likelihood_map.shape)
        for i in range(likelihood_map.shape[0]):
            for k in range(likelihood_map.shape[1]):
                if (likelihood_map[i, k] == config.cell_blocked):
                    pedestrian_expectancy_map[i, k] = likelihood_map[i, k] * 0.01
                elif (likelihood_map[i, k] > 1):
                    pedestrian_expectancy_map[i, k] = likelihood_map[i, k]
                else:
                    pedestrian_expectancy_map[i, k] = density_map[i, k] * likelihood_map[i, k]
        return pedestrian_expectancy_map
