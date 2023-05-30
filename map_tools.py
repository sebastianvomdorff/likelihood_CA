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
        print(
            "Showing initialized map with field of view before extrapolation. Ego position has the value sim_steps/2."
        )
        plot_lattice = lattice.copy()
        plot_lattice[ego_y, ego_x] = config.sim_steps / 2
        plt.imshow(plot_lattice)
        plt.show()

    return lattice


def slice_map(lattice, ego_x, ego_y):
    """Cuts out the relevant map area. Limits the considered map by the time
    the fastest human could travel over the projection horizon"""
    relevant_range = int(
        round(
            (config.fastest_person + config.v_vehicle)
            * config.simulation_horizon
            * config.t_atomic
            / config.cell_size
        )
    )
    top = max(ego_y - relevant_range + 1, 0)
    bottom = min(ego_y + relevant_range + 1, lattice.shape[0])
    left = max(ego_x - relevant_range + 1, 0)
    right = min(ego_x + relevant_range + 1, lattice.shape[1])

    slice = lattice[top:bottom, left:right]
    adjusted_x = ego_x - left
    adjusted_y = ego_y - top
    if config.output:
        print("Adjusted coordinates for map slice: ", adjusted_x, adjusted_y)
    if config.show_map_slice:
        print("Showing the relevant map map slice for the extrapolation:")
        plt.imshow(slice)
        plt.show()
    return slice, adjusted_x, adjusted_y, top, bottom, left, right


def slice_map_fov(lattice, ego_x, ego_y):
    """Cuts out the area of interest around the ego position of the map"""
    # Find all indices that are in the field of view
    fov_indices = np.argwhere(lattice == config.cell_empty)
    # for x in fov_indices:
    #
    #     print(x)
    # print("fov_indices :", fov_indices)

    # determines boundaries of the fov in a rectanle
    top = np.min(fov_indices[:, 0])
    bottom = np.max(fov_indices[:, 0])
    left = np.min(fov_indices[:, 1])
    right = np.max(fov_indices[:, 1])
    if config.output:
        print(
            "Slice boarders: left: ",
            left,
            "right: ",
            right,
            "top: ",
            top,
            "bottom: ",
            bottom,
        )

    # slice out the field of view rectangle from the original lattice
    slice = lattice[top:bottom, left:right]
    if config.show_map_slice:
        print("Showing the relevant map map slice for the extrapolation:")
        plt.imshow(slice)
        plt.show()

    return slice, top, bottom, left, right


def restore_map(lattice, map_slice, top, bottom, left, right):
    lattice[top:bottom, left:right] = map_slice
    return lattice


def merge_memory_map(lattice, memory):
    """Merges the field-of-view map with the memory map of the last iteration"""
    new_lattice = np.where(lattice == 0, 0, memory)
    if config.show_memory_merge:
        print(
            "Showing the merged map of the current FoV and the memory from previous iteration:"
        )
        plt.imshow(new_lattice)
        plt.show()
    return new_lattice


def footprint_lookup(path, trajectory, time):
    """returns the vehicles latest entered cells at a given time"""
    length = np.shape(trajectory)[1]
    latest = 0
    for i in (0, length):
        if trajectory[i, 1] > time:
            latest = i - 1
            break
    path_index = trajectory[latest, 0]
    ego_cells = np.where(path == path_index)
    return ego_cells
