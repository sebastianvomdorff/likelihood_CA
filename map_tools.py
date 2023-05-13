import numpy as np
import matplotlib.pyplot as plt
from raycast import ray_cast
import config

def init_map(lattice, ego_x, ego_y):
    """This function calculates the field of view from a given position
    and initializes the blocked and empty cells.Cells outside the field
    of view that are not statically blocked are considered as occupied."""

    # Caluclate field of view in map from given ego positon
    fov_map = ray_cast(lattice, ego_x, ego_y)

    # Mark cells that are not blocked but outside of field of view as occupied
    lattice[lattice == config.cell_empty] = config.cell_occupied

    # Mark all cells within the FOV as empty
    lattice[fov_map == 1] = config.cell_empty

    if config.show_map_init:
        print("Showing initialized map with field of view before extrapolation. Ego position has the value sim_steps/2.")
        plot_lattice = lattice.copy()
        plot_lattice[ego_y, ego_x] = config.sim_steps/2
        plt.imshow(plot_lattice)
        plt.show()

    return lattice


def slice_map(lattice, ego_x, ego_y):
    """Cuts out the relevant map area. Limits the considered map by the time
    the fastest human could travel over the projection horizon"""
    relevant_range = int(round((config.fastest_person + config.v_vehicle) * config.simulation_horizon * config.t_atomic / config.cell_size))
    top = max(ego_y - relevant_range + 1, 0)
    bottom = min(ego_y + relevant_range + 1, lattice.shape[0])
    left = max(ego_x - relevant_range + 1, 0)
    right = min(ego_x + relevant_range + 1, lattice.shape[1])

    slice = lattice[top:bottom, left:right]
    adjusted_x = ego_x - left
    adjusted_y = ego_y - top
    if config.output:
        print("Adjusted coordinates for map slice: ", adjusted_x, adjusted_y)
    return slice, adjusted_x, adjusted_y


def restore_map(map_slice, ego_x, ego_y, ego_x_adjusted, ego_y_adjusted):
    return 0

def merge_memory_map(new_lattice, memory_slice, ego_x_old, ego_y_old, ego_x_adjusted_old, ego_y_adjusted_old):
    [size_y, size_x] = memory_slice.shape

    print("sizes: ", size_y, size_x)

    start_x = ego_x_old-ego_x_adjusted_old
    end_x = start_x + size_x
    start_y = ego_y_old - ego_y_adjusted_old
    end_y = start_y + size_y
    min_lattice = np.minimum(new_lattice[start_y:end_y, start_x:end_x], memory_slice)
    new_lattice[start_y:end_y, start_x:end_x] = min_lattice

    if config.show_memory_merge:
        print("Showing merged lattice with memory data from last simulation.")
        plt.imshow(new_lattice)
        plt.show()

    return new_lattice


def footprint_lookup(path, trajectory, time):
    """ returns the vehicles latest entered cells at a given time"""

    for i in (0, np.size(trajectory)[1]):
        if trajectory[i, 1] > time:
            latest = i-1
            break
    path_index = trajectory[latest, 0]
    ego_cells = np.where(path == path_index)
    return ego_cells
