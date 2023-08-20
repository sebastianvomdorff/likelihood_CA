import config
import numpy as np
import matplotlib.pyplot as plt


def fixed_speed_eval(lattice, speed_list):
    row_index = (np.abs(speed_list[:, 1] - config.ped_speed_fixed)).argmin()
    new_lattice = np.where(lattice < row_index, 0, lattice)
    lattice = np.where(lattice == -1, lattice, new_lattice)
    lattice = np.where(lattice > 0, 1, lattice)
    if config.debug_fixed_speed:
        print(
            "The closest representable speed to the given value of ",
            config.ped_speed_fixed,
            "m/s is ",
            speed_list[row_index, 1],
            "m/s.",
        )
        print("Image shows the propagation of fixed speed pedestrians.")
        plt.imshow(lattice)
        plt.show()
    return lattice
