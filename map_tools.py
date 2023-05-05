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
        plot_lattice = lattice.copy()
        plot_lattice[lattice == config.sim_steps] = 3
        plot_lattice[ego_y, ego_x] = 2
        plt.imshow(plot_lattice)
        plt.show()

    return lattice


def slice_map(lattice, ego_x, ego_y):
    """Cuts out the relevant map area. Limits the considered map by the time
    the fastest human could travel over the projection horizon"""
    relevant_range = int(round((config.fastest_person + config.v_vehicle) * config.simulation_horizon / config.cell_size))
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


def merge_map(map_slice, lattice, ego_x, ego_y):
    return 0
