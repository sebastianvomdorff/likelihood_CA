import math
import numpy as np
from cell_update import cell_update_moore, cell_update_von_neumann


def cellular_automaton(simulation_steps, lattice, neighborhood_range):

    # determine all cells distances in the range
    neighbors = np.arange(-neighborhood_range, neighborhood_range + 1)

    # Extract length and width of lattice
    rows_total = lattice.shape[0]
    columns_total = lattice.shape[1]

    # Get squareroot of 2
    sqrt2 = math.sqrt(2)

    for step in range(simulation_steps + 1):
        lattice_frozen = lattice.copy()

        # Move through the lattice
        if ((step % (sqrt2+1)) < 1):
            for row in range(rows_total):
                for column in range(columns_total):
                    lattice[row, column] = cell_update_moore(row, column, rows_total, columns_total, neighbors, lattice_frozen)
        else:
            for row in range(rows_total):
                for column in range(columns_total):
                    lattice[row, column] = cell_update_von_neumann(row, column, rows_total, columns_total, neighbors, lattice_frozen)

    return lattice
