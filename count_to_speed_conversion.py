import numpy as np
import config


def count_to_speed():
    """create look up table that maps counting values to speeds
    first column is count, second column is speed"""
    # set up look up table that map count so speed
    count_mapping = np.zeros([config.sim_steps, 2])

    # Calculate the minimum counting index representing a quantisized speed in m/s
    for i in range(config.sim_steps):
        count_mapping[i, 0] = i + 1
        count_mapping[i, 1] = (
            config.cell_size
            * (config.sim_steps - i)
            / (config.simulation_horizon * config.t_atomic)
        )

    return count_mapping
